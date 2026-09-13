"""
Agri Link — Role-Based Permissions
====================================
Custom DRF permission classes for role-based access control.
"""

from rest_framework.permissions import BasePermission
from apps.core.constants import UserRole


class IsFarmer(BasePermission):
    """Allow access only to authenticated farmers."""

    message = "Only farmers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.FARMER
        )


class IsBuyer(BasePermission):
    """Allow access only to authenticated buyers."""

    message = "Only buyers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.BUYER
        )


class IsLabour(BasePermission):
    """Allow access only to authenticated labourers."""

    message = "Only labourers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.LABOUR
        )


class IsEquipmentOwner(BasePermission):
    """Allow access only to authenticated equipment owners."""

    message = "Only equipment owners can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.EQUIPMENT_OWNER
        )


class IsAdmin(BasePermission):
    """Allow access only to admin users."""

    message = "Only admins can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsFarmerOrBuyer(BasePermission):
    """Allow access to farmers or buyers."""

    message = "Only farmers or buyers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in {UserRole.FARMER, UserRole.BUYER}
        )


class IsFarmerOrEquipmentOwner(BasePermission):
    """Allow access to farmers or equipment owners."""

    message = "Only farmers or equipment owners can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in {UserRole.FARMER, UserRole.EQUIPMENT_OWNER}
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission: allow write only to the owner.
    Requires the object to have a `user` or `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user


class IsAuthenticatedAndActive(BasePermission):
    """Allow only authenticated and active users."""

    message = "Your account is inactive."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
