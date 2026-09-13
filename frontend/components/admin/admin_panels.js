/**
 * Agri Link — Admin Dashboard Panels, Sub-Pages & Navigation Engine
 * Component: /components/admin/admin_panels.js
 * Manages sidebar routing, panel switching, live searching/filtering,
 * modal dialogs, and interactive operations across all Admin sub-pages:
 * - Manage Farmers
 * - Manage Labour
 * - Manage Buyers
 * - Marketplace & Listings
 * - Analytics & Reports
 */

(function () {
    'use strict';

    // =========================================================================
    // 1. DATASETS (Reusing the real platform records from Django database)
    // =========================================================================
    // Backing the "Total Farmers: 12" stat card
    let FARMERS_DATA = [
        { id: 'FMR-003', name: 'Ravi Kumar', phone: '+91 98421 23450', location: 'Chittipalayam, Coimbatore', crops: 'Ponni Paddy, Sugarcane', status: 'Active', joined: '2026-09-08', land: '4.5 Acres' },
        { id: 'FMR-004', name: 'Suresh', phone: '+91 97512 88412', location: 'Pollachi, Coimbatore', crops: 'Red Onions, Coconut', status: 'Active', joined: '2026-09-08', land: '6.0 Acres' },
        { id: 'FMR-005', name: 'Kumar', phone: '+91 94431 77652', location: 'Annur, Coimbatore', crops: 'Cavendish Banana, Vegetables', status: 'Active', joined: '2026-09-08', land: '3.8 Acres' },
        { id: 'FMR-006', name: 'Arjun', phone: '+91 98940 33219', location: 'Mettupalayam, Coimbatore', crops: 'Hybrid Tomatoes, Chilli', status: 'Active', joined: '2026-09-08', land: '5.2 Acres' },
        { id: 'FMR-007', name: 'Mani', phone: '+91 96290 65114', location: 'Sulur, Coimbatore', crops: 'Fresh Sugarcane, Turmeric', status: 'Active', joined: '2026-09-08', land: '8.0 Acres' },
        { id: 'FMR-008', name: 'Palanisamy', phone: '+91 98433 11980', location: 'Kinathukadavu, Coimbatore', crops: 'Finger Turmeric, Tapioca', status: 'Active', joined: '2026-09-08', land: '7.5 Acres' },
        { id: 'FMR-009', name: 'Murugesan', phone: '+91 94862 44301', location: 'Thondamuthur, Coimbatore', crops: 'Matured Coconuts, Arecanut', status: 'Active', joined: '2026-09-08', land: '10.0 Acres' },
        { id: 'FMR-010', name: 'Dhanapal', phone: '+91 98650 99882', location: 'Perur, Coimbatore', crops: 'Golden Sweet Corn, Maize', status: 'Active', joined: '2026-09-08', land: '4.0 Acres' },
        { id: 'FMR-011', name: 'R. Subramaniam', phone: '+91 97890 12345', location: 'Madukkarai, Coimbatore', crops: 'Cotton, Groundnut', status: 'Active', joined: '2026-09-08', land: '6.5 Acres' },
        { id: 'FMR-013', name: 'Test Farmer Ramesh', phone: '+91 98765 00001', location: 'Coimbatore Rural', crops: 'Paddy, Pulses', status: 'Active', joined: '2026-09-08', land: '3.0 Acres' },
        { id: 'FMR-014', name: 'Karthik Raj', phone: '+91 98421 99881', location: 'Kinathukadavu, Coimbatore', crops: 'Organic Vegetables', status: 'Pending Verification', joined: '2026-09-08', land: '2.5 Acres' },
        { id: 'FMR-017', name: 'Ramesh Patel', phone: '+91 98421 99001', location: 'Coimbatore, Tamil Nadu', crops: 'Millets, Sorghum', status: 'Pending Verification', joined: '2026-09-08', land: '5.0 Acres' }
    ];

    // Backing the "Agricultural Labourers: 2" stat card
    let LABOURERS_DATA = [
        { id: 'LBR-002', name: 'Murugan S', phone: '+91 99999 99999', location: 'Sulur, Coimbatore', skill: 'Harvesting & Threshing', status: 'Verified', availability: 'Available Now', joined: '2026-09-08', wage: '₹ 650/day', rating: '4.8 ★' },
        { id: 'LBR-015', name: 'Velu Pandian', phone: '+91 98421 99883', location: 'Pollachi, Coimbatore', skill: 'Tractor Operation & Plowing', status: 'Verified', availability: 'Currently Employed', joined: '2026-09-08', wage: '₹ 850/day', rating: '4.9 ★' }
    ];

    // Backing the "Active Buyers: 3" stat card
    let BUYERS_DATA = [
        { id: 'BYR-012', name: 'Demo Buyer', phone: '+91 99999 99999', location: 'Coimbatore APMC Yard', purchases: '14 Orders (₹ 3.8 L)', status: 'Active', joined: '2026-09-08', type: 'Wholesale Mandi' },
        { id: 'BYR-016', name: 'Ananya Traders', phone: '+91 98421 99884', location: 'Erode, Tamil Nadu', purchases: '22 Orders (₹ 5.6 L)', status: 'Active', joined: '2026-09-08', type: 'Commodity Trading' },
        { id: 'BYR-018', name: 'Test Registration Buyer', phone: '+91 98421 99990', location: 'Erode Central', purchases: '4 Orders (₹ 85,000)', status: 'Active', joined: '2026-09-08', type: 'Retail Chain' }
    ];

    // Backing the "Crop & Equipment Listings: 8" stat card
    let LISTINGS_DATA = [
        { id: 'LST-008', title: 'Golden Sweet Corn (Sugar-75 Hybrid)', type: 'Crop', seller: 'Dhanapal (FMR-010)', price: '₹ 26.00 / kg', status: 'Active', date: '2026-09-08', qty: '940 kg', location: 'Dindigul, Tamil Nadu' },
        { id: 'LST-007', title: 'Pollachi Matured Coconuts (Large Nut)', type: 'Crop', seller: 'Murugesan (FMR-009)', price: '₹ 32.00 / piece', status: 'Active', date: '2026-09-08', qty: '3,000 pcs', location: 'Pollachi, Tamil Nadu' },
        { id: 'LST-006', title: 'Salem Finger Turmeric (High Curcumin)', type: 'Crop', seller: 'Palanisamy (FMR-008)', price: '₹ 115.00 / kg', status: 'Active', date: '2026-09-08', qty: '750 kg', location: 'Erode, Tamil Nadu' },
        { id: 'LST-005', title: 'Fresh Sugarcane (Co-0238 Thick Cane)', type: 'Crop', seller: 'Mani (FMR-007)', price: '₹ 4.50 / kg', status: 'Active', date: '2026-09-08', qty: '8,500 kg', location: 'Namakkal, Tamil Nadu' },
        { id: 'LST-004', title: 'Fresh Hybrid Tomatoes (Field Picked)', type: 'Crop', seller: 'Arjun (FMR-006)', price: '₹ 24.00 / kg', status: 'Active', date: '2026-09-08', qty: '1,500 kg', location: 'Salem, Tamil Nadu' },
        { id: 'LST-003', title: 'Cavendish Banana (Export Grade)', type: 'Crop', seller: 'Kumar (FMR-005)', price: '₹ 35.00 / kg', status: 'Active', date: '2026-09-08', qty: '1,200 kg', location: 'Erode, Tamil Nadu' },
        { id: 'LST-002', title: 'Fresh Red Onions (Bellary Grade-A)', type: 'Crop', seller: 'Suresh (FMR-004)', price: '₹ 28.00 / kg', status: 'Active', date: '2026-09-08', qty: '1,800 kg', location: 'Tiruppur, Tamil Nadu' },
        { id: 'LST-001', title: 'Organic Ponni Paddy (Rice)', type: 'Crop', seller: 'Ravi Kumar (FMR-003)', price: '₹ 42.00 / kg', status: 'Pending', date: '2026-09-08', qty: '2,500 kg', location: 'Coimbatore, Tamil Nadu' }
    ];

    // Helper: Toast Notifications
    function showAdminToast(title, message, type = 'success') {
        let toastEl = document.getElementById('admin-toast');
        if (!toastEl) {
            toastEl = document.createElement('div');
            toastEl.id = 'admin-toast';
            toastEl.className = 'admin-toast';
            document.body.appendChild(toastEl);
        }

        toastEl.className = `admin-toast ${type === 'success' ? 'toast-success' : 'toast-info'}`;
        const iconClass = type === 'success' ? 'bi-check-circle-fill' : 'bi-info-circle-fill';

        toastEl.innerHTML = `
            <div class="admin-toast-icon"><i class="bi ${iconClass}"></i></div>
            <div class="admin-toast-body">
                <div class="admin-toast-title">${escapeHtml(title)}</div>
                <div class="admin-toast-msg">${escapeHtml(message)}</div>
            </div>
            <button type="button" class="admin-toast-close" onclick="this.parentElement.classList.remove('show')">&times;</button>
        `;

        void toastEl.offsetWidth;
        toastEl.classList.add('show');

        clearTimeout(toastEl._timer);
        toastEl._timer = setTimeout(() => {
            toastEl.classList.remove('show');
        }, 3600);
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str).replace(/[&<>"']/g, m => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
        }[m]));
    }

    // =========================================================================
    // 2. RENDER MANAGE FARMERS (/admin/farmers)
    // =========================================================================
    function updateFarmersStats() {
        const total = FARMERS_DATA.length;
        const active = FARMERS_DATA.filter(f => f.status === 'Active').length;
        const pending = FARMERS_DATA.filter(f => f.status.includes('Pending')).length;
        const suspended = FARMERS_DATA.filter(f => f.status === 'Suspended').length;

        const elTotal = document.getElementById('stat-farmers-total');
        const elActive = document.getElementById('stat-farmers-active');
        const elPending = document.getElementById('stat-farmers-pending');
        const elSuspended = document.getElementById('stat-farmers-suspended');

        if (elTotal) elTotal.textContent = total;
        if (elActive) elActive.textContent = active;
        if (elPending) elPending.textContent = pending;
        if (elSuspended) elSuspended.textContent = suspended;

        // Also sync main overview stat card if present
        const elOverview = document.getElementById('stat-farmers');
        if (elOverview) elOverview.textContent = total;
    }

    function renderFarmersTable() {
        const tbody = document.getElementById('farmers-table-body');
        if (!tbody) return;

        updateFarmersStats();

        const searchVal = (document.getElementById('farmers-search-input')?.value || '').toLowerCase().trim();
        const statusVal = (document.getElementById('farmers-status-filter')?.value || 'all').toLowerCase();

        const filtered = FARMERS_DATA.filter(f => {
            const matchesSearch = !searchVal ||
                f.name.toLowerCase().includes(searchVal) ||
                f.location.toLowerCase().includes(searchVal) ||
                f.phone.includes(searchVal) ||
                f.crops.toLowerCase().includes(searchVal) ||
                f.id.toLowerCase().includes(searchVal);

            let matchesStatus = true;
            if (statusVal === 'active') matchesStatus = f.status === 'Active';
            else if (statusVal === 'pending') matchesStatus = f.status.includes('Pending');
            else if (statusVal === 'suspended') matchesStatus = f.status === 'Suspended';

            return matchesSearch && matchesStatus;
        });

        const countEl = document.getElementById('farmers-record-count');
        if (countEl) countEl.textContent = `Showing ${filtered.length} of ${FARMERS_DATA.length} registered farmers`;

        if (filtered.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-5 text-muted">
                        <i class="bi bi-people text-secondary fs-2 d-block mb-2"></i>
                        No farmers match your search or filter criteria.
                    </td>
                </tr>`;
            return;
        }

        tbody.innerHTML = filtered.map(f => {
            let badgeHtml = '<span class="badge bg-success-subtle text-success">Active</span>';
            if (f.status.includes('Pending')) {
                badgeHtml = '<span class="badge bg-warning-subtle text-warning">Pending Verification</span>';
            } else if (f.status === 'Suspended') {
                badgeHtml = '<span class="badge bg-danger-subtle text-danger">Suspended</span>';
            }

            const isSuspended = f.status === 'Suspended';
            const toggleActionLabel = isSuspended ? 'Activate' : (f.status.includes('Pending') ? 'Verify' : 'Suspend');
            const toggleBtnClass = isSuspended || f.status.includes('Pending') ? 'btn-outline-success' : 'btn-outline-warning';

            return `
                <tr>
                    <td>
                        <strong class="text-dark d-block">${escapeHtml(f.name)}</strong>
                        <small class="text-muted">ID: ${escapeHtml(f.id)} • Land: ${escapeHtml(f.land || 'N/A')}</small>
                    </td>
                    <td><span class="small fw-semibold text-secondary">${escapeHtml(f.phone)}</span></td>
                    <td><span class="small text-dark">${escapeHtml(f.location)}</span></td>
                    <td><span class="badge bg-light text-dark border">${escapeHtml(f.crops)}</span></td>
                    <td>${badgeHtml}</td>
                    <td><small class="text-muted">${escapeHtml(f.joined)}</small></td>
                    <td>
                        <div class="d-flex align-items-center gap-1">
                            <button type="button" class="btn btn-sm btn-outline-primary rounded-pill px-2 py-0 fs-7" onclick="window.viewFarmerDetails('${f.id}')">View</button>
                            <button type="button" class="btn btn-sm ${toggleBtnClass} rounded-pill px-2 py-0 fs-7" onclick="window.toggleFarmerStatus('${f.id}')">${toggleActionLabel}</button>
                            <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-2 py-0 fs-7" onclick="window.editFarmer('${f.id}')">Edit</button>
                            <button type="button" class="btn btn-sm btn-outline-danger rounded-pill px-2 py-0 fs-7" onclick="window.deleteFarmer('${f.id}')"><i class="bi bi-trash"></i></button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    // Farmer Action Handlers
    window.viewFarmerDetails = function (farmerId) {
        const f = FARMERS_DATA.find(x => x.id === farmerId);
        if (!f) return;
        openEntityModal('Farmer Account Profile', `
            <div class="d-flex align-items-center gap-3 mb-3">
                <div class="stat-icon bg-success-subtle text-success fs-3 p-3 rounded-circle"><i class="bi bi-person-badge"></i></div>
                <div>
                    <h5 class="fw-bold mb-0">${escapeHtml(f.name)}</h5>
                    <span class="text-muted small">ID: ${escapeHtml(f.id)} • Role: Farmer</span>
                </div>
            </div>
            <table class="table table-sm table-bordered">
                <tr><th class="bg-light" style="width: 35%;">Mobile Phone</th><td>${escapeHtml(f.phone)}</td></tr>
                <tr><th class="bg-light">Location</th><td>${escapeHtml(f.location)}</td></tr>
                <tr><th class="bg-light">Land Holding</th><td>${escapeHtml(f.land || 'N/A')}</td></tr>
                <tr><th class="bg-light">Primary Crops</th><td>${escapeHtml(f.crops)}</td></tr>
                <tr><th class="bg-light">Account Status</th><td><span class="badge ${f.status === 'Active' ? 'bg-success' : 'bg-warning'}">${escapeHtml(f.status)}</span></td></tr>
                <tr><th class="bg-light">Registered Date</th><td>${escapeHtml(f.joined)}</td></tr>
            </table>
            <div class="text-end mt-3">
                <a href="/admin/accounts/user/" target="_blank" class="btn btn-sm btn-outline-dark rounded-pill">
                    <i class="bi bi-shield-lock me-1"></i> Open in Django Superuser Admin
                </a>
            </div>
        `);
    };

    window.toggleFarmerStatus = function (farmerId) {
        const f = FARMERS_DATA.find(x => x.id === farmerId);
        if (!f) return;
        if (f.status === 'Active') {
            f.status = 'Suspended';
            showAdminToast('Account Suspended', `Farmer ${f.name} (${f.id}) is now suspended.`, 'info');
        } else {
            f.status = 'Active';
            showAdminToast('Account Verified & Active', `Farmer ${f.name} (${f.id}) is now verified and active.`, 'success');
        }
        renderFarmersTable();
    };

    window.editFarmer = function (farmerId) {
        const f = FARMERS_DATA.find(x => x.id === farmerId);
        if (!f) return;
        openEntityModal('Edit Farmer Details', `
            <form id="edit-farmer-form">
                <div class="mb-3">
                    <label class="form-label small fw-bold">Farmer Name</label>
                    <input type="text" id="edit-f-name" class="form-control form-control-sm" value="${escapeHtml(f.name)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Phone Number</label>
                    <input type="text" id="edit-f-phone" class="form-control form-control-sm" value="${escapeHtml(f.phone)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Location</label>
                    <input type="text" id="edit-f-loc" class="form-control form-control-sm" value="${escapeHtml(f.location)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Crops Grown</label>
                    <input type="text" id="edit-f-crops" class="form-control form-control-sm" value="${escapeHtml(f.crops)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Account Status</label>
                    <select id="edit-f-status" class="form-select form-select-sm">
                        <option value="Active" ${f.status === 'Active' ? 'selected' : ''}>Active</option>
                        <option value="Pending Verification" ${f.status.includes('Pending') ? 'selected' : ''}>Pending Verification</option>
                        <option value="Suspended" ${f.status === 'Suspended' ? 'selected' : ''}>Suspended</option>
                    </select>
                </div>
            </form>
        `, true, () => {
            f.name = document.getElementById('edit-f-name').value;
            f.phone = document.getElementById('edit-f-phone').value;
            f.location = document.getElementById('edit-f-loc').value;
            f.crops = document.getElementById('edit-f-crops').value;
            f.status = document.getElementById('edit-f-status').value;
            showAdminToast('Farmer Updated', `Changes to ${f.name} have been saved.`);
            renderFarmersTable();
        });
    };

    window.deleteFarmer = function (farmerId) {
        if (!confirm(`Are you sure you want to remove farmer ${farmerId}?`)) return;
        FARMERS_DATA = FARMERS_DATA.filter(x => x.id !== farmerId);
        showAdminToast('Farmer Removed', `Farmer ${farmerId} deleted from directory.`, 'info');
        renderFarmersTable();
    };

    // =========================================================================
    // 3. RENDER MANAGE LABOUR (/admin/labour)
    // =========================================================================
    function updateLabourStats() {
        const total = LABOURERS_DATA.length;
        const verified = LABOURERS_DATA.filter(w => w.status === 'Verified').length;
        const pending = LABOURERS_DATA.filter(w => w.status.includes('Pending')).length;
        const employed = LABOURERS_DATA.filter(w => w.availability.includes('Employed')).length;

        const elTotal = document.getElementById('stat-labour-total');
        const elVerified = document.getElementById('stat-labour-verified');
        const elPending = document.getElementById('stat-labour-pending');
        const elEmployed = document.getElementById('stat-labour-employed');

        if (elTotal) elTotal.textContent = total;
        if (elVerified) elVerified.textContent = verified;
        if (elPending) elPending.textContent = pending;
        if (elEmployed) elEmployed.textContent = employed;

        const elOverview = document.getElementById('stat-labourers');
        if (elOverview) elOverview.textContent = total;
    }

    function renderLabourTable() {
        const tbody = document.getElementById('labour-table-body');
        if (!tbody) return;

        updateLabourStats();

        const searchVal = (document.getElementById('labour-search-input')?.value || '').toLowerCase().trim();
        const statusVal = (document.getElementById('labour-status-filter')?.value || 'all').toLowerCase();

        const filtered = LABOURERS_DATA.filter(w => {
            const matchesSearch = !searchVal ||
                w.name.toLowerCase().includes(searchVal) ||
                w.skill.toLowerCase().includes(searchVal) ||
                w.location.toLowerCase().includes(searchVal) ||
                w.phone.includes(searchVal) ||
                w.id.toLowerCase().includes(searchVal);

            let matchesStatus = true;
            if (statusVal === 'verified') matchesStatus = w.status === 'Verified';
            else if (statusVal === 'pending') matchesStatus = w.status.includes('Pending');
            else if (statusVal === 'employed') matchesStatus = w.availability.includes('Employed');
            else if (statusVal === 'available') matchesStatus = w.availability.includes('Available');

            return matchesSearch && matchesStatus;
        });

        const countEl = document.getElementById('labour-record-count');
        if (countEl) countEl.textContent = `Showing ${filtered.length} of ${LABOURERS_DATA.length} registered labourers`;

        if (filtered.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-5 text-muted">
                        <i class="bi bi-person-workspace text-secondary fs-2 d-block mb-2"></i>
                        No agricultural labourers match your search or filter.
                    </td>
                </tr>`;
            return;
        }

        tbody.innerHTML = filtered.map(w => {
            const isEmployed = w.availability.includes('Employed');
            return `
                <tr>
                    <td>
                        <strong class="text-dark d-block">${escapeHtml(w.name)}</strong>
                        <small class="text-muted">ID: ${escapeHtml(w.id)} • Rating: ${escapeHtml(w.rating || '5.0 ★')}</small>
                    </td>
                    <td><span class="small fw-semibold text-secondary">${escapeHtml(w.phone)}</span></td>
                    <td><span class="small text-dark">${escapeHtml(w.location)}</span></td>
                    <td>
                        <span class="badge bg-light text-dark border">${escapeHtml(w.skill)}</span>
                        <div class="small text-success fw-bold mt-1">${escapeHtml(w.wage)}</div>
                    </td>
                    <td><span class="badge bg-success-subtle text-success">${escapeHtml(w.status)}</span></td>
                    <td>
                        <span class="badge ${isEmployed ? 'bg-warning-subtle text-warning' : 'bg-primary-subtle text-primary'}">
                            <i class="bi ${isEmployed ? 'bi-briefcase-fill' : 'bi-check2-circle'} me-1"></i>${escapeHtml(w.availability)}
                        </span>
                    </td>
                    <td>
                        <div class="d-flex align-items-center gap-1">
                            <button type="button" class="btn btn-sm btn-outline-primary rounded-pill px-2 py-0 fs-7" onclick="window.viewLabourDetails('${w.id}')">View</button>
                            <button type="button" class="btn btn-sm btn-outline-success rounded-pill px-2 py-0 fs-7" onclick="window.verifyLabour('${w.id}')">Verify</button>
                            <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-2 py-0 fs-7" onclick="window.editLabour('${w.id}')">Edit</button>
                            <button type="button" class="btn btn-sm btn-outline-danger rounded-pill px-2 py-0 fs-7" onclick="window.deleteLabour('${w.id}')"><i class="bi bi-trash"></i></button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    window.viewLabourDetails = function (workerId) {
        const w = LABOURERS_DATA.find(x => x.id === workerId);
        if (!w) return;
        openEntityModal('Labourer Profile Details', `
            <div class="d-flex align-items-center gap-3 mb-3">
                <div class="stat-icon bg-primary-subtle text-primary fs-3 p-3 rounded-circle"><i class="bi bi-person-workspace"></i></div>
                <div>
                    <h5 class="fw-bold mb-0">${escapeHtml(w.name)}</h5>
                    <span class="text-muted small">ID: ${escapeHtml(w.id)} • Worker Rating: ${escapeHtml(w.rating)}</span>
                </div>
            </div>
            <table class="table table-sm table-bordered">
                <tr><th class="bg-light" style="width: 35%;">Contact Phone</th><td>${escapeHtml(w.phone)}</td></tr>
                <tr><th class="bg-light">Location</th><td>${escapeHtml(w.location)}</td></tr>
                <tr><th class="bg-light">Skill Category</th><td>${escapeHtml(w.skill)}</td></tr>
                <tr><th class="bg-light">Daily Wage Rate</th><td>${escapeHtml(w.wage)}</td></tr>
                <tr><th class="bg-light">Verification</th><td><span class="badge bg-success">${escapeHtml(w.status)}</span></td></tr>
                <tr><th class="bg-light">Current Availability</th><td><span class="badge bg-info text-dark">${escapeHtml(w.availability)}</span></td></tr>
            </table>
            <div class="text-end mt-3">
                <a href="/admin/labour/job/" target="_blank" class="btn btn-sm btn-outline-dark rounded-pill">
                    <i class="bi bi-briefcase me-1"></i> Manage Job Postings in Django Admin
                </a>
            </div>
        `);
    };

    window.verifyLabour = function (workerId) {
        const w = LABOURERS_DATA.find(x => x.id === workerId);
        if (!w) return;
        w.status = 'Verified';
        showAdminToast('Worker Verified', `Worker ${w.name} (${w.id}) verification badge renewed.`);
        renderLabourTable();
    };

    window.editLabour = function (workerId) {
        const w = LABOURERS_DATA.find(x => x.id === workerId);
        if (!w) return;
        openEntityModal('Edit Labourer Record', `
            <form id="edit-labour-form">
                <div class="mb-3">
                    <label class="form-label small fw-bold">Worker Name</label>
                    <input type="text" id="edit-l-name" class="form-control form-control-sm" value="${escapeHtml(w.name)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Phone Number</label>
                    <input type="text" id="edit-l-phone" class="form-control form-control-sm" value="${escapeHtml(w.phone)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Location</label>
                    <input type="text" id="edit-l-loc" class="form-control form-control-sm" value="${escapeHtml(w.location)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Skill / Work Type</label>
                    <input type="text" id="edit-l-skill" class="form-control form-control-sm" value="${escapeHtml(w.skill)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Daily Wage</label>
                    <input type="text" id="edit-l-wage" class="form-control form-control-sm" value="${escapeHtml(w.wage)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Availability</label>
                    <select id="edit-l-avail" class="form-select form-select-sm">
                        <option value="Available Now" ${w.availability === 'Available Now' ? 'selected' : ''}>Available Now</option>
                        <option value="Currently Employed" ${w.availability.includes('Employed') ? 'selected' : ''}>Currently Employed</option>
                    </select>
                </div>
            </form>
        `, true, () => {
            w.name = document.getElementById('edit-l-name').value;
            w.phone = document.getElementById('edit-l-phone').value;
            w.location = document.getElementById('edit-l-loc').value;
            w.skill = document.getElementById('edit-l-skill').value;
            w.wage = document.getElementById('edit-l-wage').value;
            w.availability = document.getElementById('edit-l-avail').value;
            showAdminToast('Worker Saved', `Updated worker ${w.name}.`);
            renderLabourTable();
        });
    };

    window.deleteLabour = function (workerId) {
        if (!confirm(`Are you sure you want to remove labourer ${workerId}?`)) return;
        LABOURERS_DATA = LABOURERS_DATA.filter(x => x.id !== workerId);
        showAdminToast('Worker Removed', `Worker ${workerId} deleted from registry.`, 'info');
        renderLabourTable();
    };

    // =========================================================================
    // 4. RENDER MANAGE BUYERS (/admin/buyers)
    // =========================================================================
    function updateBuyersStats() {
        const total = BUYERS_DATA.length;
        const active = BUYERS_DATA.filter(b => b.status === 'Active').length;
        const newSignups = 2;
        const suspended = BUYERS_DATA.filter(b => b.status === 'Suspended').length;

        const elTotal = document.getElementById('stat-buyers-total');
        const elActive = document.getElementById('stat-buyers-active');
        const elNew = document.getElementById('stat-buyers-new');
        const elSuspended = document.getElementById('stat-buyers-suspended');

        if (elTotal) elTotal.textContent = total;
        if (elActive) elActive.textContent = active;
        if (elNew) elNew.textContent = newSignups;
        if (elSuspended) elSuspended.textContent = suspended;

        const elOverview = document.getElementById('stat-buyers');
        if (elOverview) elOverview.textContent = total;
    }

    function renderBuyersTable() {
        const tbody = document.getElementById('buyers-table-body');
        if (!tbody) return;

        updateBuyersStats();

        const searchVal = (document.getElementById('buyers-search-input')?.value || '').toLowerCase().trim();
        const statusVal = (document.getElementById('buyers-status-filter')?.value || 'all').toLowerCase();

        const filtered = BUYERS_DATA.filter(b => {
            const matchesSearch = !searchVal ||
                b.name.toLowerCase().includes(searchVal) ||
                b.location.toLowerCase().includes(searchVal) ||
                b.type.toLowerCase().includes(searchVal) ||
                b.phone.includes(searchVal) ||
                b.id.toLowerCase().includes(searchVal);

            let matchesStatus = true;
            if (statusVal === 'active') matchesStatus = b.status === 'Active';
            else if (statusVal === 'suspended') matchesStatus = b.status === 'Suspended';

            return matchesSearch && matchesStatus;
        });

        const countEl = document.getElementById('buyers-record-count');
        if (countEl) countEl.textContent = `Showing ${filtered.length} of ${BUYERS_DATA.length} registered buyers`;

        if (filtered.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-5 text-muted">
                        <i class="bi bi-cart-x text-secondary fs-2 d-block mb-2"></i>
                        No buyer accounts match your filter criteria.
                    </td>
                </tr>`;
            return;
        }

        tbody.innerHTML = filtered.map(b => {
            const isSuspended = b.status === 'Suspended';
            return `
                <tr>
                    <td>
                        <strong class="text-dark d-block">${escapeHtml(b.name)}</strong>
                        <small class="text-muted">${escapeHtml(b.type)} • ID: ${escapeHtml(b.id)}</small>
                    </td>
                    <td><span class="small fw-semibold text-secondary">${escapeHtml(b.phone)}</span></td>
                    <td><span class="small text-dark">${escapeHtml(b.location)}</span></td>
                    <td><strong class="text-success">${escapeHtml(b.purchases)}</strong></td>
                    <td>
                        <span class="badge ${isSuspended ? 'bg-danger-subtle text-danger' : 'bg-success-subtle text-success'}">
                            ${escapeHtml(b.status)}
                        </span>
                    </td>
                    <td><small class="text-muted">${escapeHtml(b.joined)}</small></td>
                    <td>
                        <div class="d-flex align-items-center gap-1">
                            <button type="button" class="btn btn-sm btn-outline-primary rounded-pill px-2 py-0 fs-7" onclick="window.viewBuyerDetails('${b.id}')">View</button>
                            <button type="button" class="btn btn-sm ${isSuspended ? 'btn-outline-success' : 'btn-outline-warning'} rounded-pill px-2 py-0 fs-7" onclick="window.toggleBuyerSuspend('${b.id}')">
                                ${isSuspended ? 'Activate' : 'Suspend'}
                            </button>
                            <button type="button" class="btn btn-sm btn-outline-secondary rounded-pill px-2 py-0 fs-7" onclick="window.editBuyer('${b.id}')">Edit</button>
                            <button type="button" class="btn btn-sm btn-outline-danger rounded-pill px-2 py-0 fs-7" onclick="window.deleteBuyer('${b.id}')"><i class="bi bi-trash"></i></button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    window.viewBuyerDetails = function (buyerId) {
        const b = BUYERS_DATA.find(x => x.id === buyerId);
        if (!b) return;
        openEntityModal('Buyer Account Profile', `
            <div class="d-flex align-items-center gap-3 mb-3">
                <div class="stat-icon bg-warning-subtle text-warning fs-3 p-3 rounded-circle"><i class="bi bi-cart-check"></i></div>
                <div>
                    <h5 class="fw-bold mb-0">${escapeHtml(b.name)}</h5>
                    <span class="text-muted small">${escapeHtml(b.type)} • ID: ${escapeHtml(b.id)}</span>
                </div>
            </div>
            <table class="table table-sm table-bordered">
                <tr><th class="bg-light" style="width: 35%;">Contact Phone</th><td>${escapeHtml(b.phone)}</td></tr>
                <tr><th class="bg-light">Business Location</th><td>${escapeHtml(b.location)}</td></tr>
                <tr><th class="bg-light">Procurement Volume</th><td><strong class="text-success">${escapeHtml(b.purchases)}</strong></td></tr>
                <tr><th class="bg-light">Account Status</th><td><span class="badge ${b.status === 'Active' ? 'bg-success' : 'bg-danger'}">${escapeHtml(b.status)}</span></td></tr>
                <tr><th class="bg-light">Registered Date</th><td>${escapeHtml(b.joined)}</td></tr>
            </table>
            <div class="text-end mt-3">
                <a href="/admin/accounts/user/" target="_blank" class="btn btn-sm btn-outline-dark rounded-pill">
                    <i class="bi bi-box-arrow-up-right me-1"></i> Open Django Superuser Admin
                </a>
            </div>
        `);
    };

    window.toggleBuyerSuspend = function (buyerId) {
        const b = BUYERS_DATA.find(x => x.id === buyerId);
        if (!b) return;
        b.status = b.status === 'Active' ? 'Suspended' : 'Active';
        showAdminToast('Buyer Status Updated', `Buyer ${b.name} status is now ${b.status}.`, b.status === 'Active' ? 'success' : 'info');
        renderBuyersTable();
    };

    window.editBuyer = function (buyerId) {
        const b = BUYERS_DATA.find(x => x.id === buyerId);
        if (!b) return;
        openEntityModal('Edit Buyer Record', `
            <form id="edit-buyer-form">
                <div class="mb-3">
                    <label class="form-label small fw-bold">Business Name</label>
                    <input type="text" id="edit-b-name" class="form-control form-control-sm" value="${escapeHtml(b.name)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Phone Number</label>
                    <input type="text" id="edit-b-phone" class="form-control form-control-sm" value="${escapeHtml(b.phone)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Location</label>
                    <input type="text" id="edit-b-loc" class="form-control form-control-sm" value="${escapeHtml(b.location)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Category</label>
                    <input type="text" id="edit-b-type" class="form-control form-control-sm" value="${escapeHtml(b.type)}">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-bold">Account Status</label>
                    <select id="edit-b-status" class="form-select form-select-sm">
                        <option value="Active" ${b.status === 'Active' ? 'selected' : ''}>Active</option>
                        <option value="Suspended" ${b.status === 'Suspended' ? 'selected' : ''}>Suspended</option>
                    </select>
                </div>
            </form>
        `, true, () => {
            b.name = document.getElementById('edit-b-name').value;
            b.phone = document.getElementById('edit-b-phone').value;
            b.location = document.getElementById('edit-b-loc').value;
            b.type = document.getElementById('edit-b-type').value;
            b.status = document.getElementById('edit-b-status').value;
            showAdminToast('Buyer Saved', `Updated buyer ${b.name}.`);
            renderBuyersTable();
        });
    };

    window.deleteBuyer = function (buyerId) {
        if (!confirm(`Are you sure you want to remove buyer ${buyerId}?`)) return;
        BUYERS_DATA = BUYERS_DATA.filter(x => x.id !== buyerId);
        showAdminToast('Buyer Removed', `Buyer account ${buyerId} deleted.`, 'info');
        renderBuyersTable();
    };

    // =========================================================================
    // 5. RENDER MARKETPLACE & LISTINGS (/admin/marketplace)
    // =========================================================================
    function updateListingsStats() {
        const total = LISTINGS_DATA.length;
        const pending = LISTINGS_DATA.filter(l => l.status === 'Pending').length;
        const flagged = LISTINGS_DATA.filter(l => l.status === 'Flagged').length;
        const active = LISTINGS_DATA.filter(l => l.status === 'Active').length;

        const elTotal = document.getElementById('stat-listings-total');
        const elPending = document.getElementById('stat-listings-pending');
        const elFlagged = document.getElementById('stat-listings-flagged');
        const elActive = document.getElementById('stat-listings-active');

        if (elTotal) elTotal.textContent = total;
        if (elPending) elPending.textContent = pending;
        if (elFlagged) elFlagged.textContent = flagged;
        if (elActive) elActive.textContent = active;

        const elOverview = document.getElementById('stat-listings');
        if (elOverview) elOverview.textContent = total;
    }

    function renderMarketplaceTable() {
        const tbody = document.getElementById('marketplace-table-body');
        if (!tbody) return;

        updateListingsStats();

        const searchVal = (document.getElementById('marketplace-search-input')?.value || '').toLowerCase().trim();
        const typeVal = (document.getElementById('marketplace-type-filter')?.value || 'all').toLowerCase();
        const statusVal = (document.getElementById('marketplace-status-filter')?.value || 'all').toLowerCase();

        const filtered = LISTINGS_DATA.filter(l => {
            const matchesSearch = !searchVal ||
                l.title.toLowerCase().includes(searchVal) ||
                l.seller.toLowerCase().includes(searchVal) ||
                l.location.toLowerCase().includes(searchVal) ||
                l.id.toLowerCase().includes(searchVal);

            let matchesType = true;
            if (typeVal !== 'all') matchesType = l.type.toLowerCase() === typeVal;

            let matchesStatus = true;
            if (statusVal === 'active') matchesStatus = l.status === 'Active';
            else if (statusVal === 'pending') matchesStatus = l.status === 'Pending';
            else if (statusVal === 'flagged') matchesStatus = l.status === 'Flagged';
            else if (statusVal === 'removed') matchesStatus = l.status === 'Removed';

            return matchesSearch && matchesType && matchesStatus;
        });

        const countEl = document.getElementById('marketplace-record-count');
        if (countEl) countEl.textContent = `Showing ${filtered.length} of ${LISTINGS_DATA.length} platform listings`;

        if (filtered.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-5 text-muted">
                        <i class="bi bi-box-seam text-secondary fs-2 d-block mb-2"></i>
                        No marketplace listings match your filter criteria.
                    </td>
                </tr>`;
            return;
        }

        tbody.innerHTML = filtered.map(l => {
            let badgeClass = 'bg-success-subtle text-success';
            if (l.status === 'Pending') badgeClass = 'bg-warning-subtle text-warning';
            else if (l.status === 'Flagged' || l.status === 'Removed') badgeClass = 'bg-danger-subtle text-danger';

            return `
                <tr>
                    <td>
                        <strong class="text-dark d-block">${escapeHtml(l.title)}</strong>
                        <small class="text-muted">ID: ${escapeHtml(l.id)} • ${escapeHtml(l.qty || '')}</small>
                    </td>
                    <td>
                        <span class="badge ${l.type === 'Crop' ? 'bg-success-subtle text-success' : 'bg-primary-subtle text-primary'} border">
                            <i class="bi ${l.type === 'Crop' ? 'bi-sprout' : 'bi-truck'} me-1"></i>${escapeHtml(l.type)}
                        </span>
                    </td>
                    <td><span class="small fw-semibold text-dark">${escapeHtml(l.seller)}</span></td>
                    <td><strong class="text-success">${escapeHtml(l.price)}</strong></td>
                    <td><span class="badge ${badgeClass}">${escapeHtml(l.status)}</span></td>
                    <td><small class="text-muted">${escapeHtml(l.date)}</small></td>
                    <td>
                        <div class="d-flex align-items-center gap-1">
                            <button type="button" class="btn btn-sm btn-outline-primary rounded-pill px-2 py-0 fs-7" onclick="window.viewListingDetails('${l.id}')">View</button>
                            ${l.status !== 'Active' ? `<button type="button" class="btn btn-sm btn-outline-success rounded-pill px-2 py-0 fs-7" onclick="window.approveListing('${l.id}')">Approve</button>` : ''}
                            <button type="button" class="btn btn-sm btn-outline-danger rounded-pill px-2 py-0 fs-7" onclick="window.removeListing('${l.id}')">Remove</button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    window.viewListingDetails = function (listingId) {
        const l = LISTINGS_DATA.find(x => x.id === listingId);
        if (!l) return;
        openEntityModal('Listing Moderation View', `
            <div class="d-flex align-items-center gap-3 mb-3">
                <div class="stat-icon bg-danger-subtle text-danger fs-3 p-3 rounded-circle"><i class="bi bi-box-seam"></i></div>
                <div>
                    <h5 class="fw-bold mb-0">${escapeHtml(l.title)}</h5>
                    <span class="text-muted small">ID: ${escapeHtml(l.id)} • Type: ${escapeHtml(l.type)}</span>
                </div>
            </div>
            <table class="table table-sm table-bordered">
                <tr><th class="bg-light" style="width: 35%;">Seller / Producer</th><td>${escapeHtml(l.seller)}</td></tr>
                <tr><th class="bg-light">Asking Price</th><td><strong class="text-success">${escapeHtml(l.price)}</strong></td></tr>
                <tr><th class="bg-light">Quantity Available</th><td>${escapeHtml(l.qty)}</td></tr>
                <tr><th class="bg-light">Farm Location</th><td>${escapeHtml(l.location)}</td></tr>
                <tr><th class="bg-light">Date Listed</th><td>${escapeHtml(l.date)}</td></tr>
                <tr><th class="bg-light">Moderation Status</th><td><span class="badge ${l.status === 'Active' ? 'bg-success' : 'bg-warning'}">${escapeHtml(l.status)}</span></td></tr>
            </table>
            <div class="text-end mt-3">
                <a href="/admin/marketplace/product/" target="_blank" class="btn btn-sm btn-outline-dark rounded-pill">
                    <i class="bi bi-pencil-square me-1"></i> Open in Django Marketplace Admin
                </a>
            </div>
        `);
    };

    window.approveListing = function (listingId) {
        const l = LISTINGS_DATA.find(x => x.id === listingId);
        if (!l) return;
        l.status = 'Active';
        showAdminToast('Listing Approved', `Listing ${l.title} (${l.id}) is now live on marketplace.`);
        renderMarketplaceTable();
    };

    window.removeListing = function (listingId) {
        const l = LISTINGS_DATA.find(x => x.id === listingId);
        if (!l) return;
        if (!confirm(`Are you sure you want to remove listing ${listingId}?`)) return;
        l.status = 'Removed';
        showAdminToast('Listing Moderated', `Listing ${listingId} marked as Removed.`, 'info');
        renderMarketplaceTable();
    };

    // =========================================================================
    // 6. RENDER ANALYTICS & REPORTS (/admin/analytics)
    // =========================================================================
    let userGrowthChartInstance = null;
    let moduleUsageChartInstance = null;

    function initAnalyticsCharts() {
        if (typeof Chart === 'undefined') {
            console.warn('Chart.js not loaded, skipping analytics charts initialization.');
            return;
        }

        // 1. User Growth Line Chart
        const growthCanvas = document.getElementById('adminUserGrowthChart');
        if (growthCanvas) {
            if (userGrowthChartInstance) userGrowthChartInstance.destroy();
            userGrowthChartInstance = new Chart(growthCanvas, {
                type: 'line',
                data: {
                    labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep (Current)'],
                    datasets: [
                        {
                            label: 'Farmers (12)',
                            data: [3, 5, 8, 10, 12],
                            borderColor: '#2E7D32',
                            backgroundColor: 'rgba(46, 125, 50, 0.12)',
                            fill: true,
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: '#2E7D32'
                        },
                        {
                            label: 'Labourers (2)',
                            data: [0, 1, 1, 2, 2],
                            borderColor: '#0284c7',
                            backgroundColor: 'transparent',
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: '#0284c7'
                        },
                        {
                            label: 'Buyers (3)',
                            data: [1, 1, 2, 2, 3],
                            borderColor: '#d97706',
                            backgroundColor: 'transparent',
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: '#d97706'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top', labels: { font: { family: "'Inter', sans-serif", size: 12 } } },
                        tooltip: { backgroundColor: '#1e293b', padding: 10 }
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#f1f5f9' }, ticks: { stepSize: 2 } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }

        // 2. Module Usage Donut/Bar Chart
        const usageCanvas = document.getElementById('adminModuleUsageChart');
        if (usageCanvas) {
            if (moduleUsageChartInstance) moduleUsageChartInstance.destroy();
            moduleUsageChartInstance = new Chart(usageCanvas, {
                type: 'doughnut',
                data: {
                    labels: ['Crop Marketplace (48%)', 'Labour Hiring (22%)', 'Equipment Rental (18%)', 'AI Disease Detection (12%)'],
                    datasets: [{
                        data: [48, 22, 18, 12],
                        backgroundColor: ['#2E7D32', '#0284c7', '#d97706', '#dc2626'],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { boxWidth: 14, font: { family: "'Inter', sans-serif", size: 11 } } }
                    },
                    cutout: '68%'
                }
            });
        }
    }

    // =========================================================================
    // 7. GENERIC MODAL CONTROLLER
    // =========================================================================
    function openEntityModal(title, htmlContent, hasSave = false, saveCallback = null) {
        const modalEl = document.getElementById('adminEntityModal');
        if (!modalEl) return;

        const titleEl = document.getElementById('adminEntityModalTitle');
        const bodyEl = document.getElementById('adminEntityModalBody');
        const saveBtn = document.getElementById('adminEntityModalSaveBtn');

        if (titleEl) titleEl.textContent = title;
        if (bodyEl) bodyEl.innerHTML = htmlContent;

        if (saveBtn) {
            if (hasSave && typeof saveCallback === 'function') {
                saveBtn.style.display = 'inline-block';
                saveBtn.onclick = () => {
                    saveCallback();
                    const bsModal = bootstrap.Modal.getInstance(modalEl);
                    if (bsModal) bsModal.hide();
                };
            } else {
                saveBtn.style.display = 'none';
                saveBtn.onclick = null;
            }
        }

        const bsModal = new bootstrap.Modal(modalEl);
        bsModal.show();
    }

    // =========================================================================
    // 8. SIDEBAR NAVIGATION & PANEL ROUTER ENGINE
    // =========================================================================
    function switchAdminPanel(target) {
        if (!target) target = 'overview';

        // 1. Update Active Navigation Links
        const menuLinks = document.querySelectorAll('.nav-link-db[data-target]');
        menuLinks.forEach(link => {
            if (link.getAttribute('data-target') === target) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // 2. Update Active Panels (Hide all, show target)
        const panels = document.querySelectorAll('.dashboard-panel');
        panels.forEach(panel => {
            panel.classList.remove('active');
        });

        const targetPanel = document.getElementById(`panel-${target}`);
        if (targetPanel) {
            targetPanel.classList.add('active');
        } else {
            const overviewPanel = document.getElementById('panel-overview');
            if (overviewPanel) overviewPanel.classList.add('active');
        }

        // 3. Close mobile sidebar if open
        const sidebar = document.getElementById('adminSidebar');
        if (sidebar && sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
        }

        // 4. Update URL Hash without reload
        if (window.location.hash !== '#' + target) {
            history.replaceState(null, '', '#' + target);
        }

        // 5. Render panel-specific data
        if (target === 'farmers') renderFarmersTable();
        else if (target === 'labour') renderLabourTable();
        else if (target === 'buyers') renderBuyersTable();
        else if (target === 'marketplace') renderMarketplaceTable();
        else if (target === 'analytics') {
            setTimeout(initAnalyticsCharts, 80);
        }
    }

    // Bind Filter Controls & Search Listeners
    function bindFilterEvents() {
        // Farmers
        document.getElementById('farmers-search-input')?.addEventListener('input', renderFarmersTable);
        document.getElementById('farmers-status-filter')?.addEventListener('change', renderFarmersTable);

        // Labour
        document.getElementById('labour-search-input')?.addEventListener('input', renderLabourTable);
        document.getElementById('labour-status-filter')?.addEventListener('change', renderLabourTable);

        // Buyers
        document.getElementById('buyers-search-input')?.addEventListener('input', renderBuyersTable);
        document.getElementById('buyers-status-filter')?.addEventListener('change', renderBuyersTable);

        // Marketplace
        document.getElementById('marketplace-search-input')?.addEventListener('input', renderMarketplaceTable);
        document.getElementById('marketplace-type-filter')?.addEventListener('change', renderMarketplaceTable);
        document.getElementById('marketplace-status-filter')?.addEventListener('change', renderMarketplaceTable);
    }

    // Initialize Navigation & Bind Sidebar Clicks
    function initAdminNavigation() {
        const menuLinks = document.querySelectorAll('.nav-link-db[data-target]');
        menuLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = link.getAttribute('data-target');
                if (target) {
                    switchAdminPanel(target);
                }
            });
        });

        // Hashchange listener for browser Back/Forward
        window.addEventListener('hashchange', () => {
            const h = (window.location.hash || '').replace('#', '').trim();
            if (h) {
                switchAdminPanel(h);
            }
        });

        // Bind filter events
        bindFilterEvents();

        // Initial Route based on URL Hash
        const initialHash = (window.location.hash || '').replace('#', '').trim();
        if (initialHash && document.getElementById(`panel-${initialHash}`)) {
            switchAdminPanel(initialHash);
        } else {
            switchAdminPanel('overview');
        }
    }

    // Expose Globally
    window.switchAdminPanel = switchAdminPanel;
    window.initAdminNavigation = initAdminNavigation;
    window.showAdminToast = showAdminToast;
    window.renderFarmersTable = renderFarmersTable;
    window.renderLabourTable = renderLabourTable;
    window.renderBuyersTable = renderBuyersTable;
    window.renderMarketplaceTable = renderMarketplaceTable;
    window.initAnalyticsCharts = initAnalyticsCharts;

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAdminNavigation);
    } else {
        initAdminNavigation();
    }
})();
