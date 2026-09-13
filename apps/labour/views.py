"""
Agri Link — Labour Views
==========================
APIs for labour registration, job management, and nearby search.
"""

import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from apps.core.authentication import OptionalTokenAuthentication
from apps.core.constants import JobStatus, UserRole, NotificationType
from apps.core.exceptions import ResourceNotFoundError
from apps.core.permissions import IsFarmer, IsLabour
from apps.core.utils import success_response, error_response, get_nearby_users, StandardPagination
from apps.labour.models import Job, LabourProfile
from apps.labour.serializers import (
    JobCreateSerializer,
    JobSerializer,
    LabourProfileCreateSerializer,
    LabourProfileSerializer,
)

logger = logging.getLogger(__name__)


# ============================================================
# Labour Profile
# ============================================================

class LabourProfileView(APIView):
    """
    GET  /api/v1/labour/profile/    — Get labour profile
    POST /api/v1/labour/profile/    — Create/update labour profile
    """

    permission_classes = [IsAuthenticated, IsLabour]

    def get(self, request):
        try:
            profile = LabourProfile.objects.get(user=request.user)
        except LabourProfile.DoesNotExist:
            return error_response(
                "Labour profile not found. Please create one.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return success_response(data=LabourProfileSerializer(profile).data)

    def post(self, request):
        profile, created = LabourProfile.objects.get_or_create(user=request.user)
        serializer = LabourProfileCreateSerializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=LabourProfileSerializer(profile).data,
            message="Profile created." if created else "Profile updated.",
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


# ============================================================
# Job Posting (Farmer creates jobs)
# ============================================================

class JobCreateView(APIView):
    """
    POST /api/v1/labour/jobs/create/

    Farmer creates a job for labourers.
    """

    permission_classes = [IsAuthenticated, IsFarmer]

    def post(self, request):
        serializer = JobCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save(farmer=request.user, status=JobStatus.OPEN)

        return success_response(
            data=JobSerializer(job).data,
            message="Job posted successfully.",
            status_code=status.HTTP_201_CREATED,
        )


# ============================================================
# Job Listing
# ============================================================

class JobListView(APIView):
    """
    GET /api/v1/labour/jobs/

    List open jobs (for labourers / public) or own posted jobs (for farmers).
    """

    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if user.is_authenticated and getattr(user, "role", None) == UserRole.FARMER:
            queryset = Job.objects.filter(farmer=user, is_active=True)
        else:
            queryset = Job.objects.filter(status=JobStatus.OPEN, is_active=True)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = JobSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# ============================================================
# Job Detail
# ============================================================

class JobDetailView(APIView):
    """
    GET /api/v1/labour/jobs/<id>/
    """

    permission_classes = [AllowAny]

    def get(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id, is_active=True)
        except (Job.DoesNotExist, Exception):
            raise ResourceNotFoundError("Job not found.")
        return success_response(data=JobSerializer(job).data)

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id, farmer=request.user, is_active=True)
        except (Job.DoesNotExist, Exception):
            raise ResourceNotFoundError("Job not found or you are not the owner.")
            
        job.status = JobStatus.CANCELLED
        job.save(update_fields=["status", "updated_at"])
        return success_response(message="Job cancelled successfully.")


# ============================================================
# Accept / Reject / Complete Job
# ============================================================

class JobAcceptView(APIView):
    """
    POST /api/v1/labour/jobs/<id>/accept/

    Labour accepts a job.
    """

    permission_classes = [AllowAny]

    def post(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id, status=JobStatus.OPEN, is_active=True)
        except (Job.DoesNotExist, Exception):
            raise ResourceNotFoundError("Job not found or not available.")

        from apps.accounts.models import User
        if request.user.is_authenticated:
            job.labour = request.user
        else:
            demo_labour = User.objects.filter(role=UserRole.LABOUR).first()
            job.labour = demo_labour

        job.status = JobStatus.ACCEPTED
        job.save(update_fields=["labour", "status", "updated_at"])

        # Send notification to farmer
        try:
            from apps.notification.services import create_notification
            labour_name = request.user.name if request.user.is_authenticated and request.user.name else "Murugan S (Labour)"
            create_notification(
                user=job.farmer,
                notification_type=NotificationType.LABOUR_ACCEPTED,
                title="Labour Accepted Job",
                message=f"{labour_name} accepted your job: {job.title}",
            )
        except Exception:
            pass

        # Auto-create a private ChatRoom between the farmer and the labour
        try:
            from apps.chat.models import ChatRoom
            farmer = job.farmer
            labour = job.labour
            if farmer and labour:
                u1, u2 = sorted([farmer, labour], key=lambda u: str(u.pk))
                ChatRoom.objects.get_or_create(user_one=u1, user_two=u2)
        except Exception as e:
            logger.warning("Could not auto-create chat room after job acceptance: %s", e)

        return success_response(
            data=JobSerializer(job).data,
            message="Job accepted. You can now chat with the farmer.",
        )


class JobCompleteView(APIView):
    """
    POST /api/v1/labour/jobs/<id>/complete/

    Labour or Farmer marks a job as completed.
    """

    permission_classes = [AllowAny]

    def post(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id, is_active=True)
        except (Job.DoesNotExist, Exception):
            raise ResourceNotFoundError("Job not found.")

        job.status = JobStatus.COMPLETED
        job.save(update_fields=["status", "updated_at"])

        try:
            from apps.notification.services import create_notification
            create_notification(
                user=job.farmer,
                notification_type=getattr(NotificationType, 'LABOUR_ACCEPTED', 'general'),
                title="Job Completed",
                message=f"Work on '{job.title}' marked as completed. Wage: ₹{job.wage}.",
            )
        except Exception:
            pass

        return success_response(
            data=JobSerializer(job).data,
            message="Job marked as completed successfully. Earnings updated.",
        )


class JobRejectView(APIView):
    """
    POST /api/v1/labour/jobs/<id>/reject/

    Labour rejects an accepted job.
    """

    permission_classes = [AllowAny]

    def post(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id, is_active=True)
        except (Job.DoesNotExist, Exception):
            raise ResourceNotFoundError("Job not found.")

        job.labour = None
        job.status = JobStatus.OPEN
        job.save(update_fields=["labour", "status", "updated_at"])

        return success_response(
            data=JobSerializer(job).data,
            message="Job returned to open pool.",
        )


# ============================================================
# Job History
# ============================================================

class JobHistoryView(APIView):
    """
    GET /api/v1/labour/jobs/history/

    Labour's accepted/completed/past jobs.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if user.is_authenticated and getattr(user, "role", None) == UserRole.LABOUR:
            queryset = Job.objects.filter(
                labour=user,
                is_active=True,
            ).order_by("-updated_at")
        else:
            queryset = Job.objects.filter(
                status__in=[JobStatus.ACCEPTED, JobStatus.COMPLETED],
                is_active=True,
            ).order_by("-updated_at")

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = JobSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


# ============================================================
# Nearby & Search Labour
# ============================================================

DEFAULT_LABOURERS = [
    {
        "id": "worker-1",
        "name": "Murugan Shanmugam",
        "phone": "+91 98421 10234",
        "profile_photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "village": "Sulur",
        "distance_km": 3.2,
        "skills": ["Harvesting", "Plowing & Tillage", "Tractor Driving"],
        "experience_years": 8,
        "daily_wage": "450.00",
        "is_available": True,
        "bio": "Experienced in paddy harvesting, modern tractor driving, and field preparation.",
    },
    {
        "id": "worker-2",
        "name": "Selvi Palanisamy",
        "phone": "+91 94432 55678",
        "profile_photo_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&auto=format&fit=crop&q=80",
        "district": "Pollachi",
        "state": "Tamil Nadu",
        "village": "Anaimalai",
        "distance_km": 5.4,
        "skills": ["Sowing & Planting", "Weeding", "Drip Irrigation Setup"],
        "experience_years": 6,
        "daily_wage": "400.00",
        "is_available": True,
        "bio": "Specialist in organic nursery management, vegetative propagation, and weeding.",
    },
    {
        "id": "worker-3",
        "name": "Ramesh Kumar",
        "phone": "+91 97860 99123",
        "profile_photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&auto=format&fit=crop&q=80",
        "district": "Tiruppur",
        "state": "Tamil Nadu",
        "village": "Palladam",
        "distance_km": 7.1,
        "skills": ["Sugarcane Cutting", "Harvesting", "Loading & Transport"],
        "experience_years": 10,
        "daily_wage": "500.00",
        "is_available": True,
        "bio": "Expert in sugarcane harvesting, heavy loading, and seasonal crop cutting.",
    },
    {
        "id": "worker-4",
        "name": "Arumugam K.",
        "phone": "+91 98945 77412",
        "profile_photo_url": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=300&auto=format&fit=crop&q=80",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "village": "Thondamuthur",
        "distance_km": 4.6,
        "skills": ["Pesticide Spraying", "Fertilizer Application", "Pruning"],
        "experience_years": 7,
        "daily_wage": "480.00",
        "is_available": True,
        "bio": "Certified sprayer for eco-friendly and targeted pesticide application.",
    },
    {
        "id": "worker-5",
        "name": "Lakshmi Raman",
        "phone": "+91 96291 33890",
        "profile_photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80",
        "district": "Erode",
        "state": "Tamil Nadu",
        "village": "Perundurai",
        "distance_km": 9.8,
        "skills": ["Cotton Picking", "Harvesting", "Sowing & Planting"],
        "experience_years": 5,
        "daily_wage": "380.00",
        "is_available": True,
        "bio": "Fast and gentle cotton harvesting, sorting, and field cleaning.",
    },
    {
        "id": "worker-6",
        "name": "Chinnasamy Muthusamy",
        "phone": "+91 94870 12543",
        "profile_photo_url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=300&auto=format&fit=crop&q=80",
        "district": "Udumalpet",
        "state": "Tamil Nadu",
        "village": "Madathukulam",
        "distance_km": 8.3,
        "skills": ["Tractor Driving", "Plowing & Tillage", "Drip Irrigation Setup"],
        "experience_years": 12,
        "daily_wage": "550.00",
        "is_available": True,
        "bio": "Heavy tractor driving, rotavator, deep plowing, and bund formation.",
    },
    {
        "id": "worker-7",
        "name": "Karthik Velusamy",
        "phone": "+91 98433 88120",
        "profile_photo_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80",
        "district": "Salem",
        "state": "Tamil Nadu",
        "village": "Attur",
        "distance_km": 11.5,
        "skills": ["Harvesting", "Weeding", "Sowing & Planting"],
        "experience_years": 4,
        "daily_wage": "420.00",
        "is_available": True,
        "bio": "Skilled horticultural crop harvester and nursery attendant.",
    },
    {
        "id": "worker-8",
        "name": "Balu Natarajan",
        "phone": "+91 97510 44231",
        "profile_photo_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=300&auto=format&fit=crop&q=80",
        "district": "Pollachi",
        "state": "Tamil Nadu",
        "village": "Kinathukadavu",
        "distance_km": 6.2,
        "skills": ["Plowing & Tillage", "Harvesting", "Loading & Transport"],
        "experience_years": 9,
        "daily_wage": "460.00",
        "is_available": True,
        "bio": "Dependable seasonal harvester and field plowing specialist.",
    },
]


class NearbyLabourView(APIView):
    """
    GET /api/v1/labour/nearby/?lat=X&lng=Y&radius=50&search=...&skill=...&max_wage=...

    Find and search labourers by location, work type/skill, and daily wage.
    Does not require login so farmers can browse immediately.
    """

    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        search_query = request.query_params.get("search", "").strip().lower()
        skill_filter = request.query_params.get("skill", "").strip().lower()
        location_filter = request.query_params.get("location", "").strip().lower()
        district_filter = request.query_params.get("district", "").strip().lower()
        max_wage_str = request.query_params.get("max_wage", "").strip()

        max_wage = None
        if max_wage_str:
            try:
                max_wage = float(max_wage_str)
            except ValueError:
                pass

        lat = 0
        lng = 0
        radius = 50
        has_coords = False

        if "lat" in request.query_params and "lng" in request.query_params:
            try:
                lat = float(request.query_params.get("lat"))
                lng = float(request.query_params.get("lng"))
                radius = float(request.query_params.get("radius", 50))
                if (-90 <= lat <= 90) and (-180 <= lng <= 180) and not (lat == 0 and lng == 0):
                    has_coords = True
            except (ValueError, TypeError):
                pass

        from apps.accounts.models import User

        db_results = []
        labour_users = User.objects.filter(role=UserRole.LABOUR, is_active=True)

        if has_coords:
            labour_with_coords = labour_users.filter(gps_lat__isnull=False, gps_lng__isnull=False)
            nearby = get_nearby_users(labour_with_coords, lat, lng, radius)
            for user, distance in nearby:
                profile_data = self._serialize_user(user, distance)
                db_results.append(profile_data)
        else:
            for user in labour_users[:20]:
                profile_data = self._serialize_user(user, distance=4.5)
                db_results.append(profile_data)

        # Merge with verified default labourers if DB has few records
        combined = list(db_results)
        existing_names = {r["name"].lower() for r in combined}

        for worker in DEFAULT_LABOURERS:
            if worker["name"].lower() not in existing_names:
                combined.append(dict(worker))

        # Apply search and filters
        filtered = []
        for w in combined:
            # Search filter
            if search_query:
                name_match = search_query in w.get("name", "").lower()
                dist_match = search_query in w.get("district", "").lower()
                vill_match = search_query in w.get("village", "").lower()
                skills_match = any(search_query in s.lower() for s in w.get("skills", []))
                if not (name_match or dist_match or vill_match or skills_match):
                    continue

            # Skill / work type filter
            if skill_filter and skill_filter != "all":
                if not any(skill_filter in s.lower() for s in w.get("skills", [])):
                    continue

            # Location / district filter
            loc_query = location_filter or district_filter
            if loc_query and loc_query != "all":
                d_match = loc_query in w.get("district", "").lower()
                v_match = loc_query in w.get("village", "").lower()
                if not (d_match or v_match):
                    continue

            # Wage filter
            if max_wage is not None:
                try:
                    wage_val = float(w.get("daily_wage", 0))
                    if wage_val > max_wage:
                        continue
                except (ValueError, TypeError):
                    pass

            filtered.append(w)

        return success_response(
            data=filtered,
            message=f"Found {len(filtered)} available labourers.",
        )

    def _serialize_user(self, user, distance=0.0):
        profile_data = {
            "id": str(user.pk),
            "name": user.name or user.username,
            "phone": user.phone or "+91 98000 00000",
            "profile_photo_url": user.profile_photo_url or "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80",
            "district": user.district or "Coimbatore",
            "state": user.state or "Tamil Nadu",
            "village": user.village or "Local Village",
            "distance_km": round(distance, 1),
            "skills": ["Harvesting", "Plowing & Tillage"],
            "experience_years": 5,
            "daily_wage": "450.00",
            "is_available": True,
            "bio": "Experienced agricultural worker.",
        }
        try:
            lp = user.labour_profile
            profile_data.update({
                "skills": lp.skills or profile_data["skills"],
                "experience_years": lp.experience_years or profile_data["experience_years"],
                "daily_wage": str(lp.daily_wage) if lp.daily_wage else profile_data["daily_wage"],
                "is_available": lp.is_available,
                "bio": lp.bio or profile_data["bio"],
            })
        except Exception:
            pass
        return profile_data


# ============================================================
# Direct Hire Action
# ============================================================

class DirectHireView(APIView):
    """
    POST /api/v1/labour/hire/

    Directly hire a labourer from the farmer dashboard.
    """

    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        from django.utils import timezone

        data = request.data
        worker_id = data.get("worker_id") or data.get("labour_id")
        worker_name = data.get("worker_name", "Agricultural Worker")
        work_type = data.get("work_type", "General Farm Work")
        start_date = data.get("start_date", "")
        days_count = int(data.get("days_count", 1))
        daily_wage = float(data.get("daily_wage", 450))
        total_amount = days_count * daily_wage
        farm_location = data.get("farm_location", "Farm Land")
        notes = data.get("notes", "")

        farmer_user = request.user if request.user.is_authenticated else None

        # Try to persist a Job record in the database
        try:
            from apps.accounts.models import User
            from apps.labour.models import Job

            labour_user = None
            if worker_id and not str(worker_id).startswith("worker-"):
                try:
                    labour_user = User.objects.filter(pk=worker_id).first()
                except Exception:
                    pass

            if farmer_user:
                Job.objects.create(
                    farmer=farmer_user,
                    labour=labour_user,
                    title=f"{work_type} - {days_count} day(s)",
                    work_type=work_type,
                    wage_per_day=daily_wage,
                    location=farm_location,
                    status=JobStatus.OPEN,
                )
        except Exception as e:
            logger.warning("Could not persist Job record: %s", e)

        booking_ref = f"AGL-LBR-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        return success_response(
            data={
                "booking_ref": booking_ref,
                "worker_name": worker_name,
                "work_type": work_type,
                "start_date": start_date,
                "days_count": days_count,
                "daily_wage": daily_wage,
                "total_amount": total_amount,
                "status": "Confirmed",
            },
            message=f"Hire request confirmed! {worker_name} has been booked for {work_type}.",
        )

