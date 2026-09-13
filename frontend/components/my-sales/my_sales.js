/**
 * Agri Link — My Sales Module Component Logic
 * Component: /components/my-sales/my_sales.js
 * Manages Sales Summary stats, Revenue Overview chart, Crop-wise breakdown,
 * searchable/filterable Transaction History table, pagination, CSV/PDF export,
 * and Transaction Details modal.
 */

(function () {
    'use strict';

    // =========================================================================
    // SAMPLE / MOCK SALES DATA (Structured matching marketplace orders API)
    // =========================================================================
    const SAMPLE_SALES_DATA = [
        {
            order_id: 'ORD-2026-9412',
            date: '2026-09-10',
            crop_name: 'Paddy (Sona Masoori)',
            buyer_name: 'Kaveri Agri Trading Co.',
            buyer_phone: '+91 98421 55670',
            buyer_location: 'Erode Mandi, Tamil Nadu',
            quantity: 25,
            unit: 'Quintal',
            unit_price: 2600,
            total_amount: 65000,
            status: 'Paid',
            payment_method: 'Direct Bank Transfer (NEFT)',
            delivery_status: 'Delivered',
            notes: 'Grade A premium harvest inspected and verified at farm gate.'
        },
        {
            order_id: 'ORD-2026-9388',
            date: '2026-09-08',
            crop_name: 'Sugarcane (Co 86032)',
            buyer_name: 'Bannari Amman Sugar Mills',
            buyer_phone: '+91 97500 22340',
            buyer_location: 'Alathukombai, Sathyamangalam',
            quantity: 14,
            unit: 'Ton',
            unit_price: 3000,
            total_amount: 42000,
            status: 'Paid',
            payment_method: 'Direct Sugar Factory Account Credit',
            delivery_status: 'Delivered',
            notes: 'High sucrose recovery cane delivered via transport trailer.'
        },
        {
            order_id: 'ORD-2026-9351',
            date: '2026-09-05',
            crop_name: 'Country Tomato (Hybrid)',
            buyer_name: 'FreshDirect Organics Ltd.',
            buyer_phone: '+91 94432 11980',
            buyer_location: 'Ukkadam Wholesale Market, Coimbatore',
            quantity: 50,
            unit: 'Crate (25kg)',
            unit_price: 370,
            total_amount: 18500,
            status: 'Paid',
            payment_method: 'UPI Instant Settlement (GPay)',
            delivery_status: 'Delivered',
            notes: 'Firm ripe tomatoes collected in ventilated plastic crates.'
        },
        {
            order_id: 'ORD-2026-9290',
            date: '2026-09-03',
            crop_name: 'Organic Wheat (Sharbati)',
            buyer_name: 'Pachaiyappa Agro Products',
            buyer_phone: '+91 98940 33451',
            buyer_location: 'Salem APMC Yard, Tamil Nadu',
            quantity: 8,
            unit: 'Quintal',
            unit_price: 2750,
            total_amount: 22000,
            status: 'Pending',
            payment_method: 'Cheque on Gate Weighment',
            delivery_status: 'In Transit',
            notes: 'Awaiting weighbridge slip confirmation for final release.'
        },
        {
            order_id: 'ORD-2026-9244',
            date: '2026-08-28',
            crop_name: 'White Cotton (MCU 5)',
            buyer_name: 'Lakshmi Cotton Ginning Mills',
            buyer_phone: '+91 94862 88410',
            buyer_location: 'Tiruppur Textile Belt',
            quantity: 3,
            unit: 'Candy (356kg)',
            unit_price: 5000,
            total_amount: 15000,
            status: 'Paid',
            payment_method: 'RTGS / Bank Transfer',
            delivery_status: 'Delivered',
            notes: 'Moisture content tested at 7.5%. Passed ginning parameters.'
        },
        {
            order_id: 'ORD-2026-9195',
            date: '2026-08-24',
            crop_name: 'Yellow Corn / Maize',
            buyer_name: 'Suguna Poultry Feeds Ltd.',
            buyer_phone: '+91 97890 66230',
            buyer_location: 'Palladam, Tiruppur',
            quantity: 4,
            unit: 'Ton',
            unit_price: 2400,
            total_amount: 9600,
            status: 'Paid',
            payment_method: 'IMPS Direct Settlement',
            delivery_status: 'Delivered',
            notes: 'Clean dried poultry grade grain with moisture below 12%.'
        },
        {
            order_id: 'ORD-2026-9122',
            date: '2026-08-19',
            crop_name: 'Red Onion (Bellary)',
            buyer_name: 'Selvam Vegetable Traders',
            buyer_phone: '+91 99420 55190',
            buyer_location: 'Gandhi Market, Trichy',
            quantity: 16,
            unit: 'Bag (50kg)',
            unit_price: 400,
            total_amount: 6400,
            status: 'Pending',
            payment_method: 'Cash on Delivery (COD)',
            delivery_status: 'Awaiting Pickup',
            notes: 'Medium sized cured onions packed in mesh bags.'
        },
        {
            order_id: 'ORD-2026-9071',
            date: '2026-08-14',
            crop_name: 'Fresh Green Chilli',
            buyer_name: 'Annapoorna Spices & Exports',
            buyer_phone: '+91 98433 77120',
            buyer_location: 'Pollachi Road, Coimbatore',
            quantity: 8,
            unit: 'Bag (25kg)',
            unit_price: 400,
            total_amount: 3200,
            status: 'Failed',
            payment_method: 'Online NetBanking',
            delivery_status: 'Cancelled',
            notes: 'Payment gateway timed out during buyer checkout. Order cancelled.'
        }
    ];

    // Module State
    let salesTransactions = [...SAMPLE_SALES_DATA];
    let filteredTransactions = [...SAMPLE_SALES_DATA];
    let currentPage = 1;
    const pageSize = 5;

    // Charts instances
    let revenueChartInstance = null;
    let cropBreakdownChartInstance = null;

    // Helper: Toast notification
    function showSalesToast(title, message, type = 'success') {
        let toastEl = document.getElementById('sales-toast');
        if (!toastEl) {
            toastEl = document.createElement('div');
            toastEl.id = 'sales-toast';
            toastEl.className = 'sales-toast';
            document.body.appendChild(toastEl);
        }

        toastEl.className = `sales-toast ${type === 'error' ? 'toast-error' : ''}`;
        const iconClass = type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-check-circle-fill';

        toastEl.innerHTML = `
            <div class="sales-toast-icon"><i class="bi ${iconClass}"></i></div>
            <div class="sales-toast-body">
                <div class="sales-toast-title">${escapeHtml(title)}</div>
                <div class="sales-toast-msg">${escapeHtml(message)}</div>
            </div>
            <button type="button" class="sales-toast-close" onclick="this.parentElement.classList.remove('show')">&times;</button>
        `;

        void toastEl.offsetWidth;
        toastEl.classList.add('show');

        clearTimeout(toastEl._timer);
        toastEl._timer = setTimeout(() => {
            toastEl.classList.remove('show');
        }, 4000);
    }

    // Helper: Format INR currency
    function formatINR(amount) {
        return '₹ ' + Number(amount).toLocaleString('en-IN');
    }

    // Helper: HTML escape
    function escapeHtml(str) {
        if (!str) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return String(str).replace(/[&<>"']/g, m => map[m]);
    }

    // =========================================================================
    // 1. RENDER SALES SUMMARY STATS
    // =========================================================================
    function renderSummaryStats() {
        let totalRevenue = 0;
        let pendingAmount = 0;
        let paidCount = 0;
        let cropCounts = {};

        salesTransactions.forEach(item => {
            const amt = Number(item.total_amount) || 0;
            if (item.status === 'Paid') {
                totalRevenue += amt;
                paidCount++;
                const crop = item.crop_name.split('(')[0].trim();
                cropCounts[crop] = (cropCounts[crop] || 0) + (Number(item.quantity) || 1);
            } else if (item.status === 'Pending') {
                pendingAmount += amt;
            }
        });

        // Top Selling Crop
        let topCrop = 'Paddy';
        let topQty = 0;
        for (const [crop, qty] of Object.entries(cropCounts)) {
            if (qty > topQty) {
                topQty = qty;
                topCrop = crop;
            }
        }

        const revEl = document.getElementById('stat-sales-revenue');
        const ordersEl = document.getElementById('stat-sales-orders');
        const pendingEl = document.getElementById('stat-sales-pending');
        const topCropEl = document.getElementById('stat-sales-topcrop');
        const topCropSubEl = document.getElementById('stat-sales-topcrop-sub');
        const ordersSubEl = document.getElementById('stat-sales-orders-sub');

        if (revEl) revEl.textContent = formatINR(totalRevenue);
        if (ordersEl) ordersEl.textContent = salesTransactions.length;
        if (ordersSubEl) ordersSubEl.textContent = `${paidCount} Completed, ${salesTransactions.length - paidCount} Pending`;
        if (pendingEl) pendingEl.textContent = formatINR(pendingAmount);
        if (topCropEl) topCropEl.textContent = topCrop;
        if (topCropSubEl) topCropSubEl.textContent = `${topQty} units sold this season`;
    }

    // =========================================================================
    // 2. REVENUE OVERVIEW CHART (Chart.js)
    // =========================================================================
    const CHART_DATASETS = {
        monthly: {
            labels: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
            data: [65000, 78000, 92000, 84000, 110000, 128000, 105000, 142000, 136000, 158000, 151000, 172100]
        },
        weekly: {
            labels: ['Week 32', 'Week 33', 'Week 34', 'Week 35', 'Week 36', 'Week 37'],
            data: [28000, 34500, 41200, 38000, 46500, 65000]
        },
        yearly: {
            labels: ['2023', '2024', '2025', '2026 (YTD)'],
            data: [485000, 720000, 940000, 1180000]
        }
    };

    function initRevenueChart(period = 'monthly') {
        const canvas = document.getElementById('revenueChart');
        if (!canvas || typeof Chart === 'undefined') return;

        const ctx = canvas.getContext('2d');
        const ds = CHART_DATASETS[period] || CHART_DATASETS.monthly;

        if (revenueChartInstance) {
            revenueChartInstance.destroy();
        }

        // Gradient for line fill
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(46, 125, 50, 0.28)');
        gradient.addColorStop(1, 'rgba(46, 125, 50, 0.0)');

        revenueChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ds.labels,
                datasets: [{
                    label: 'Earnings (₹)',
                    data: ds.data,
                    borderColor: '#2e7d32',
                    backgroundColor: gradient,
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: '#1b5e20',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1b5e20',
                        titleFont: { size: 12, weight: 'bold' },
                        bodyFont: { size: 13 },
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: function (context) {
                                return 'Revenue: ' + formatINR(context.raw);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#64748b', font: { size: 11 } }
                    },
                    y: {
                        border: { dash: [4, 4] },
                        grid: { color: '#f1f5f9' },
                        ticks: {
                            color: '#64748b',
                            font: { size: 11 },
                            callback: function (val) {
                                return '₹ ' + (val >= 1000 ? (val / 1000) + 'k' : val);
                            }
                        }
                    }
                }
            }
        });
    }

    // Bind time tabs (Weekly / Monthly / Yearly)
    function bindTimeTabs() {
        const tabs = document.querySelectorAll('.time-tab-btn');
        tabs.forEach(btn => {
            btn.addEventListener('click', () => {
                tabs.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const period = btn.getAttribute('data-period');
                initRevenueChart(period);
            });
        });
    }

    // =========================================================================
    // 3. CROP-WISE SALES BREAKDOWN (Donut Chart & Progress List)
    // =========================================================================
    const CROP_BREAKDOWN_DATA = [
        { name: 'Paddy', amount: 65000, share: 38, color: '#2e7d32' },
        { name: 'Sugarcane', amount: 42000, share: 24, color: '#16a34a' },
        { name: 'Wheat', amount: 22000, share: 13, color: '#4ade80' },
        { name: 'Tomato', amount: 18500, share: 11, color: '#a3e635' },
        { name: 'Cotton', amount: 15000, share: 9, color: '#f59e0b' },
        { name: 'Maize & Others', amount: 9600, share: 5, color: '#94a3b8' }
    ];

    function initCropBreakdownChart() {
        const canvas = document.getElementById('cropBreakdownChart');
        if (!canvas || typeof Chart === 'undefined') return;

        const ctx = canvas.getContext('2d');

        if (cropBreakdownChartInstance) {
            cropBreakdownChartInstance.destroy();
        }

        cropBreakdownChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: CROP_BREAKDOWN_DATA.map(d => d.name),
                datasets: [{
                    data: CROP_BREAKDOWN_DATA.map(d => d.share),
                    backgroundColor: CROP_BREAKDOWN_DATA.map(d => d.color),
                    borderWidth: 2,
                    borderColor: '#ffffff',
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1b5e20',
                        padding: 10,
                        cornerRadius: 8,
                        callbacks: {
                            label: function (context) {
                                const item = CROP_BREAKDOWN_DATA[context.dataIndex];
                                return ` ${item.name}: ${item.share}% (${formatINR(item.amount)})`;
                            }
                        }
                    }
                },
                cutout: '72%'
            }
        });

        // Render progress bars list on the right
        const listContainer = document.getElementById('crop-breakdown-list');
        if (listContainer) {
            listContainer.innerHTML = CROP_BREAKDOWN_DATA.map(item => `
                <div class="crop-progress-item">
                    <div class="crop-progress-header">
                        <div class="crop-name-label">
                            <span class="crop-color-dot" style="background: ${item.color};"></span>
                            <span>${escapeHtml(item.name)}</span>
                        </div>
                        <div>
                            <span class="crop-amount-stat">${formatINR(item.amount)}</span>
                            <span class="crop-pct-share">(${item.share}%)</span>
                        </div>
                    </div>
                    <div class="crop-progress-bar-bg">
                        <div class="crop-progress-fill" style="width: ${item.share}%; background: ${item.color};"></div>
                    </div>
                </div>
            `).join('');
        }
    }

    // =========================================================================
    // 4. TRANSACTION HISTORY TABLE & FILTERING
    // =========================================================================
    function renderTransactionTable() {
        const tbody = document.getElementById('sales-transactions-tbody');
        const emptyState = document.getElementById('sales-empty-state');
        const tableWrap = document.getElementById('sales-table-wrapper');
        const paginationWrap = document.getElementById('sales-pagination-wrapper');
        const totalCountEl = document.getElementById('sales-total-count');
        const showingInfoEl = document.getElementById('sales-showing-info');
        const pageIndicatorEl = document.getElementById('sales-page-indicator');
        const prevBtn = document.getElementById('btn-sales-prev');
        const nextBtn = document.getElementById('btn-sales-next');

        if (!tbody) return;

        const total = filteredTransactions.length;
        if (totalCountEl) totalCountEl.textContent = total;

        if (total === 0) {
            if (tableWrap) tableWrap.classList.add('d-none');
            if (paginationWrap) paginationWrap.classList.add('d-none');
            if (emptyState) emptyState.classList.remove('d-none');
            return;
        }

        if (tableWrap) tableWrap.classList.remove('d-none');
        if (paginationWrap) paginationWrap.classList.remove('d-none');
        if (emptyState) emptyState.classList.add('d-none');

        const totalPages = Math.ceil(total / pageSize) || 1;
        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        const startIdx = (currentPage - 1) * pageSize;
        const endIdx = Math.min(startIdx + pageSize, total);
        const pageItems = filteredTransactions.slice(startIdx, endIdx);

        if (showingInfoEl) {
            showingInfoEl.textContent = (window.currentLanguage === 'ta')
                ? `${total} பரிவர்த்தனைகளில் ${startIdx + 1}–${endIdx} காட்டப்படுகிறது`
                : `Showing ${startIdx + 1}–${endIdx} of ${total} transactions`;
        }

        if (pageIndicatorEl) {
            pageIndicatorEl.textContent = (window.currentLanguage === 'ta')
                ? `பக்கம் ${currentPage} / ${totalPages}`
                : `Page ${currentPage} of ${totalPages}`;
        }
        if (prevBtn) prevBtn.disabled = (currentPage <= 1);
        if (nextBtn) nextBtn.disabled = (currentPage >= totalPages);

        tbody.innerHTML = pageItems.map(item => {
            let statusBadge = '';
            const st = (item.status || 'Pending').toLowerCase();
            if (st === 'paid') {
                const txt = (typeof window.t === 'function') ? window.t('bookings.status_completed', 'Paid') : 'Paid';
                statusBadge = `<span class="badge-status-paid"><i class="bi bi-check2-circle"></i> ${txt}</span>`;
            } else if (st === 'failed') {
                const txt = (typeof window.t === 'function') ? window.t('bookings.status_cancelled', 'Failed') : 'Failed';
                statusBadge = `<span class="badge-status-failed"><i class="bi bi-x-circle"></i> ${txt}</span>`;
            } else {
                const txt = (typeof window.t === 'function') ? window.t('bookings.status_pending', 'Pending') : 'Pending';
                statusBadge = `<span class="badge-status-pending"><i class="bi bi-hourglass-split"></i> ${txt}</span>`;
            }

            const detailsLabel = (typeof window.t === 'function') ? window.t('common.view', 'Details') : 'Details';

            return `
                <tr>
                    <td class="text-muted small">${formatDate(item.date)}</td>
                    <td>
                        <div class="fw-semibold text-dark">${escapeHtml(item.crop_name)}</div>
                    </td>
                    <td>
                        <span class="text-secondary">${escapeHtml(item.buyer_name)}</span>
                    </td>
                    <td>${item.quantity} ${escapeHtml(item.unit)}</td>
                    <td class="text-muted">₹ ${Number(item.unit_price).toLocaleString('en-IN')}</td>
                    <td class="fw-bold text-success">${formatINR(item.total_amount)}</td>
                    <td>${statusBadge}</td>
                    <td><span class="order-id-pill">${escapeHtml(item.order_id)}</span></td>
                    <td>
                        <button type="button" class="btn-view-sale" data-order-id="${escapeHtml(item.order_id)}" title="View transaction receipt">
                            <i class="bi bi-receipt"></i> ${detailsLabel}
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

        // Bind View Details buttons
        tbody.querySelectorAll('.btn-view-sale').forEach(btn => {
            btn.addEventListener('click', () => {
                const oId = btn.getAttribute('data-order-id');
                viewSaleDetails(oId);
            });
        });
    }

    // Filter handling
    function filterTransactions() {
        const searchVal = (document.getElementById('sales-search-input')?.value || '').toLowerCase().trim();
        const cropVal = (document.getElementById('sales-crop-filter')?.value || 'all').toLowerCase();
        const statusVal = (document.getElementById('sales-status-filter')?.value || 'all').toLowerCase();

        filteredTransactions = salesTransactions.filter(item => {
            const matchesSearch = !searchVal ||
                item.order_id.toLowerCase().includes(searchVal) ||
                item.crop_name.toLowerCase().includes(searchVal) ||
                item.buyer_name.toLowerCase().includes(searchVal);

            const matchesCrop = (cropVal === 'all') ||
                item.crop_name.toLowerCase().includes(cropVal);

            const matchesStatus = (statusVal === 'all') ||
                item.status.toLowerCase() === statusVal;

            return matchesSearch && matchesCrop && matchesStatus;
        });

        currentPage = 1;
        renderTransactionTable();
    }

    // Bind search, filter & pagination inputs
    function bindTableControls() {
        const searchInput = document.getElementById('sales-search-input');
        const cropFilter = document.getElementById('sales-crop-filter');
        const statusFilter = document.getElementById('sales-status-filter');
        const prevBtn = document.getElementById('btn-sales-prev');
        const nextBtn = document.getElementById('btn-sales-next');

        if (searchInput) searchInput.addEventListener('input', filterTransactions);
        if (cropFilter) cropFilter.addEventListener('change', filterTransactions);
        if (statusFilter) statusFilter.addEventListener('change', filterTransactions);

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (currentPage > 1) {
                    currentPage--;
                    renderTransactionTable();
                }
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                const totalPages = Math.ceil(filteredTransactions.length / pageSize) || 1;
                if (currentPage < totalPages) {
                    currentPage++;
                    renderTransactionTable();
                }
            });
        }
    }

    // =========================================================================
    // 5. VIEW TRANSACTION DETAILS MODAL
    // =========================================================================
    function viewSaleDetails(orderId) {
        const order = salesTransactions.find(o => o.order_id === orderId);
        if (!order) return;

        const idEl = document.getElementById('modal-sale-order-id');
        const dateEl = document.getElementById('modal-sale-date');
        const cropEl = document.getElementById('modal-sale-crop');
        const buyerEl = document.getElementById('modal-sale-buyer');
        const phoneEl = document.getElementById('modal-sale-phone');
        const locEl = document.getElementById('modal-sale-location');
        const qtyEl = document.getElementById('modal-sale-qty');
        const unitPriceEl = document.getElementById('modal-sale-unit-price');
        const totalEl = document.getElementById('modal-sale-total');
        const statusEl = document.getElementById('modal-sale-status');
        const payMethodEl = document.getElementById('modal-sale-paymethod');
        const notesEl = document.getElementById('modal-sale-notes');

        if (idEl) idEl.textContent = order.order_id;
        if (dateEl) dateEl.textContent = formatDate(order.date);
        if (cropEl) cropEl.textContent = order.crop_name;
        if (buyerEl) buyerEl.textContent = order.buyer_name;
        if (phoneEl) phoneEl.textContent = order.buyer_phone || 'N/A';
        if (locEl) locEl.textContent = order.buyer_location || 'Local Mandi';
        if (qtyEl) qtyEl.textContent = `${order.quantity} ${order.unit}`;
        if (unitPriceEl) unitPriceEl.textContent = `₹ ${Number(order.unit_price).toLocaleString('en-IN')}`;
        if (totalEl) totalEl.textContent = formatINR(order.total_amount);
        if (payMethodEl) payMethodEl.textContent = order.payment_method || 'Direct Bank Settlement';
        if (notesEl) notesEl.textContent = order.notes || 'No special order notes.';

        if (statusEl) {
            const st = (order.status || 'Pending').toLowerCase();
            if (st === 'paid') {
                statusEl.className = 'badge-status-paid';
                statusEl.innerHTML = '<i class="bi bi-check2-circle"></i> Paid';
            } else if (st === 'failed') {
                statusEl.className = 'badge-status-failed';
                statusEl.innerHTML = '<i class="bi bi-x-circle"></i> Failed';
            } else {
                statusEl.className = 'badge-status-pending';
                statusEl.innerHTML = '<i class="bi bi-hourglass-split"></i> Pending';
            }
        }

        const modalEl = document.getElementById('modal-sale-details');
        if (modalEl && window.bootstrap) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.show();
        }
    }

    // =========================================================================
    // 6. EXPORT ACTIONS (CSV & PDF)
    // =========================================================================
    function handleExportCSV() {
        if (!filteredTransactions || filteredTransactions.length === 0) {
            showSalesToast('Export Notice', 'No sales transactions available to export.', 'error');
            return;
        }

        const headers = ['Order ID', 'Date', 'Crop Name', 'Buyer', 'Quantity', 'Unit', 'Unit Price (INR)', 'Total Amount (INR)', 'Payment Status', 'Payment Method'];
        const rows = filteredTransactions.map(item => [
            `"${item.order_id}"`,
            `"${item.date}"`,
            `"${item.crop_name.replace(/"/g, '""')}"`,
            `"${item.buyer_name.replace(/"/g, '""')}"`,
            item.quantity,
            `"${item.unit}"`,
            item.unit_price,
            item.total_amount,
            `"${item.status}"`,
            `"${(item.payment_method || '').replace(/"/g, '""')}"`
        ]);

        const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\r\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `agrilink_sales_report_${new Date().toISOString().split('T')[0]}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        showSalesToast('Export Successful', 'Your sales report CSV has been downloaded.');
    }

    function handleExportPDF() {
        showSalesToast('Preparing PDF Report', 'Opening browser print/save preview for sales statement...');
        setTimeout(() => {
            window.print();
        }, 500);
    }

    function bindExportButtons() {
        const csvBtn = document.getElementById('btn-export-csv');
        const pdfBtn = document.getElementById('btn-export-pdf');

        if (csvBtn) csvBtn.addEventListener('click', handleExportCSV);
        if (pdfBtn) pdfBtn.addEventListener('click', handleExportPDF);
    }

    // Helper: Date format
    function formatDate(dateStr) {
        if (!dateStr) return '--';
        try {
            const d = new Date(dateStr);
            if (isNaN(d.getTime())) return dateStr;
            const options = { day: '2-digit', month: 'short', year: 'numeric' };
            return d.toLocaleDateString('en-IN', options);
        } catch (e) {
            return dateStr;
        }
    }

    // =========================================================================
    // 7. INITIALIZE MODULE
    // =========================================================================
    async function initSalesModule() {
        const salesPanel = document.getElementById('panel-sales');
        if (!salesPanel) return;

        // Attempt API fetch if authenticated, otherwise use sample data
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const resp = await fetch('/api/v1/marketplace/orders/?role=farmer', {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                if (resp.ok) {
                    const data = await resp.json();
                    const results = data.results || data.data || [];
                    if (results.length > 0) {
                        salesTransactions = results.map(o => ({
                            order_id: `ORD-${o.id.substring(0, 8).toUpperCase()}`,
                            date: o.created_at ? o.created_at.split('T')[0] : '2026-09-10',
                            crop_name: o.product?.crop_name || 'Marketplace Crop',
                            buyer_name: o.buyer?.name || 'Verified Buyer',
                            buyer_phone: o.buyer?.phone || '+91 98765 43210',
                            buyer_location: o.product?.location || 'Tamil Nadu',
                            quantity: o.quantity || 1,
                            unit: o.product?.unit || 'Kg',
                            unit_price: o.product?.price || 100,
                            total_amount: o.total_price || (o.quantity * (o.product?.price || 100)),
                            status: o.status === 'delivered' ? 'Paid' : (o.status === 'cancelled' ? 'Failed' : 'Pending'),
                            payment_method: 'Agri Link Escrow Bank Settlement',
                            delivery_status: o.status,
                            notes: 'Order placed via Agri Link Marketplace.'
                        }));
                        filteredTransactions = [...salesTransactions];
                    }
                }
            } catch (err) {
                console.warn('Marketplace orders fetch notice (using sample records):', err);
            }
        }

        renderSummaryStats();
        initRevenueChart('monthly');
        bindTimeTabs();
        initCropBreakdownChart();
        renderTransactionTable();
        bindTableControls();
        bindExportButtons();

        window.addEventListener('languageChanged', () => {
            renderTransactionTable();
        });
    }

    // Global Expose
    window.initSalesModule = initSalesModule;

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSalesModule);
    } else {
        initSalesModule();
    }
})();
