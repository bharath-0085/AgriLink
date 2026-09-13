/**
 * Agri Link — Help & Support Module Component Logic
 * Component: /components/help-support/help_support.js
 * Manages Quick Contacts, Ticket Submission, My Tickets List, FAQ Accordions, and Resource Links.
 */

(function () {
    'use strict';

    const STORAGE_KEY = 'agrilink_support_tickets';

    // Default Seed Tickets (shown if farmer has no tickets in localStorage)
    const DEFAULT_TICKETS = [
        {
            id: 'AGL-7392',
            category: 'Crop Advice',
            subject: 'Tomato early blight leaf yellowing inquiry',
            description: 'Noticed dark concentric brown spots with yellow halos on lower leaves of my tomato crop. Inquiring about immediate organic bio-fungicide options.',
            status: 'Resolved',
            date: '2026-09-08',
            attachment: 'tomato_leaf_photo.jpg'
        },
        {
            id: 'AGL-8104',
            category: 'Booking Problem',
            subject: 'Tractor rental schedule adjustment request',
            description: 'Due to sudden regional rainfall yesterday, I need to reschedule the confirmed Mahindra 575 DI tractor rental from Friday morning to Saturday morning.',
            status: 'In Progress',
            date: '2026-09-10',
            attachment: null
        }
    ];

    // Helper: Toast notification
    function showHelpToast(title, message, type = 'success') {
        let toastEl = document.getElementById('help-toast');
        if (!toastEl) {
            toastEl = document.createElement('div');
            toastEl.id = 'help-toast';
            toastEl.className = 'help-toast';
            document.body.appendChild(toastEl);
        }

        toastEl.className = `help-toast ${type === 'error' ? 'toast-error' : ''}`;
        const iconClass = type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-check-circle-fill';

        toastEl.innerHTML = `
            <div class="help-toast-icon"><i class="bi ${iconClass}"></i></div>
            <div class="help-toast-body">
                <div class="help-toast-title">${title}</div>
                <div class="help-toast-msg">${message}</div>
            </div>
            <button type="button" class="help-toast-close" onclick="this.parentElement.classList.remove('show')">&times;</button>
        `;

        void toastEl.offsetWidth;
        toastEl.classList.add('show');

        clearTimeout(toastEl._timer);
        toastEl._timer = setTimeout(() => {
            toastEl.classList.remove('show');
        }, 4000);
    }

    // Get Tickets from LocalStorage
    function getStoredTickets() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) {
                // Initialize default seeds
                localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_TICKETS));
                return [...DEFAULT_TICKETS];
            }
            return JSON.parse(raw) || [];
        } catch (e) {
            console.warn('Error reading support tickets from storage:', e);
            return [...DEFAULT_TICKETS];
        }
    }

    // Save Tickets to LocalStorage
    function saveTickets(tickets) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(tickets));
        } catch (e) {
            console.error('Error saving tickets:', e);
        }
    }

    // Render My Tickets Table
    function renderTicketsTable() {
        const tableBody = document.getElementById('tickets-table-body');
        const emptyState = document.getElementById('tickets-empty-state');
        const tableWrap = document.getElementById('tickets-table-container');
        if (!tableBody) return;

        const tickets = getStoredTickets();

        if (tickets.length === 0) {
            if (tableWrap) tableWrap.classList.add('d-none');
            if (emptyState) emptyState.classList.remove('d-none');
            return;
        }

        if (tableWrap) tableWrap.classList.remove('d-none');
        if (emptyState) emptyState.classList.add('d-none');

        tableBody.innerHTML = tickets.map(ticket => {
            let statusBadge = '';
            let statusBadge = '';
            const st = (ticket.status || 'Open').toLowerCase();
            if (st === 'resolved') {
                const txt = (typeof window.t === 'function') ? window.t('bookings.status_completed', 'Resolved') : 'Resolved';
                statusBadge = `<span class="badge-status-resolved"><i class="bi bi-check2"></i> ${txt}</span>`;
            } else if (st === 'in progress' || st === 'inprogress') {
                const txt = (typeof window.t === 'function') ? window.t('overview.active_bookings', 'In Progress') : 'In Progress';
                statusBadge = `<span class="badge-status-progress"><i class="bi bi-hourglass-split"></i> ${txt}</span>`;
            } else {
                const txt = (typeof window.t === 'function') ? window.t('bookings.status_pending', 'Open') : 'Open';
                statusBadge = `<span class="badge-status-open"><i class="bi bi-clock"></i> ${txt}</span>`;
            }

            const viewLabel = (typeof window.t === 'function') ? window.t('common.view', 'View') : 'View';
            return `
                <tr>
                    <td><span class="ticket-id-pill">${ticket.id}</span></td>
                    <td><span class="fw-semibold text-secondary">${escapeHtml(ticket.category || 'General')}</span></td>
                    <td>
                        <div class="fw-semibold text-dark text-truncate" style="max-width: 280px;" title="${escapeHtml(ticket.subject)}">
                            ${escapeHtml(ticket.subject)}
                        </div>
                    </td>
                    <td>${statusBadge}</td>
                    <td class="text-muted small">${formatDate(ticket.date)}</td>
                    <td>
                        <button type="button" class="btn-view-ticket" data-ticket-id="${ticket.id}" title="View full ticket details">
                            <i class="bi bi-eye"></i> ${viewLabel}
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

        // Bind View buttons
        tableBody.querySelectorAll('.btn-view-ticket').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.getAttribute('data-ticket-id');
                viewTicketDetails(id);
            });
        });
    }

    // View Ticket Details Modal
    function viewTicketDetails(ticketId) {
        const tickets = getStoredTickets();
        const ticket = tickets.find(t => t.id === ticketId);
        if (!ticket) return;

        const idEl = document.getElementById('detail-ticket-id');
        const catEl = document.getElementById('detail-ticket-category');
        const statusEl = document.getElementById('detail-ticket-status');
        const dateEl = document.getElementById('detail-ticket-date');
        const subjEl = document.getElementById('detail-ticket-subject');
        const descEl = document.getElementById('detail-ticket-desc');
        const attachWrapEl = document.getElementById('detail-ticket-attachment-wrap');
        const attachEl = document.getElementById('detail-ticket-attachment');

        if (idEl) idEl.textContent = ticket.id;
        if (catEl) catEl.textContent = ticket.category;
        if (dateEl) dateEl.textContent = formatDate(ticket.date);
        if (subjEl) subjEl.textContent = ticket.subject;
        if (descEl) descEl.textContent = ticket.description;

        if (statusEl) {
            const st = (ticket.status || 'Open').toLowerCase();
            if (st === 'resolved') {
                statusEl.className = 'badge-status-resolved';
                statusEl.innerHTML = '<i class="bi bi-check2"></i> Resolved';
            } else if (st === 'in progress' || st === 'inprogress') {
                statusEl.className = 'badge-status-progress';
                statusEl.innerHTML = '<i class="bi bi-hourglass-split"></i> In Progress';
            } else {
                statusEl.className = 'badge-status-open';
                statusEl.innerHTML = '<i class="bi bi-clock"></i> Open';
            }
        }

        if (attachWrapEl && attachEl) {
            if (ticket.attachment) {
                attachWrapEl.classList.remove('d-none');
                attachEl.textContent = ticket.attachment;
            } else {
                attachWrapEl.classList.add('d-none');
            }
        }

        const modalEl = document.getElementById('modal-ticket-details');
        if (modalEl && window.bootstrap) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.show();
        }
    }

    // Handle Ticket Submit
    function handleTicketSubmit(e) {
        e.preventDefault();

        const categoryEl = document.getElementById('ticket-category');
        const subjectEl = document.getElementById('ticket-subject');
        const descriptionEl = document.getElementById('ticket-description');
        const fileInput = document.getElementById('ticket-attachment');
        const submitBtn = document.getElementById('btn-submit-ticket');

        const category = categoryEl ? categoryEl.value.trim() : 'General';
        const subject = subjectEl ? subjectEl.value.trim() : '';
        const description = descriptionEl ? descriptionEl.value.trim() : '';

        if (!subject || !description) {
            showHelpToast('Missing Information', 'Please fill in both the Subject and Description for your ticket.', 'error');
            return;
        }

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
        }

        setTimeout(() => {
            // Generate Realistic Ticket ID
            const randomNum = Math.floor(1000 + Math.random() * 9000);
            const ticketId = `AGL-${randomNum}`;
            const today = new Date().toISOString().split('T')[0];

            let attachmentName = null;
            if (fileInput && fileInput.files && fileInput.files[0]) {
                attachmentName = fileInput.files[0].name;
            }

            const newTicket = {
                id: ticketId,
                category: category || 'Other',
                subject: subject,
                description: description,
                status: 'Open',
                date: today,
                attachment: attachmentName
            };

            const currentTickets = getStoredTickets();
            currentTickets.unshift(newTicket);
            saveTickets(currentTickets);

            // Reset form
            document.getElementById('support-ticket-form')?.reset();
            const attachNameEl = document.getElementById('attachment-selected-name');
            if (attachNameEl) {
                attachNameEl.classList.add('d-none');
                attachNameEl.textContent = '';
            }

            // Re-render tickets table
            renderTicketsTable();

            if (submitBtn) {
                submitBtn.disabled = false;
                const btnText = (typeof window.t === 'function') ? window.t('help.btn_submit_ticket', 'Submit Ticket') : 'Submit Ticket';
                submitBtn.innerHTML = `<i class="bi bi-send-fill"></i><span>${btnText}</span>`;
            }

            // Success feedback with generated ticket ID
            const toastTitle = (typeof window.t === 'function') ? window.t('settings.toast_success', 'Ticket Submitted') : 'Ticket Submitted';
            const toastMsg = (typeof window.t === 'function') ? window.t('help.toast_ticket_submitted', `Ticket #${ticketId} submitted — we'll respond within 24 hours.`) : `Ticket #${ticketId} submitted — we'll respond within 24 hours.`;
            showHelpToast(toastTitle, toastMsg, 'success');
        }, 600);
    }

    // Bind FAQ Accordion Items
    function bindFaqAccordion() {
        const faqHeaders = document.querySelectorAll('.agri-faq-header');
        faqHeaders.forEach(header => {
            header.onclick = function (e) {
                e.preventDefault();
                const parentItem = this.closest('.agri-faq-item');
                if (!parentItem) return;

                const isAlreadyActive = parentItem.classList.contains('active');

                // Close all other items for clean single-accordion behavior
                document.querySelectorAll('.agri-faq-item').forEach(item => {
                    item.classList.remove('active');
                });

                if (!isAlreadyActive) {
                    parentItem.classList.add('active');
                }
            };
        });
    }

    // Bind File Attachment input preview
    function bindAttachmentPreview() {
        const fileInput = document.getElementById('ticket-attachment');
        const triggerBox = document.getElementById('attachment-upload-box');
        const nameDisplay = document.getElementById('attachment-selected-name');

        if (triggerBox && fileInput) {
            triggerBox.addEventListener('click', () => {
                fileInput.click();
            });
        }

        if (fileInput && nameDisplay) {
            fileInput.addEventListener('change', () => {
                if (fileInput.files && fileInput.files[0]) {
                    const fName = fileInput.files[0].name;
                    nameDisplay.innerHTML = `<i class="bi bi-paperclip"></i> Attached: ${escapeHtml(fName)}`;
                    nameDisplay.classList.remove('d-none');
                } else {
                    nameDisplay.classList.add('d-none');
                    nameDisplay.textContent = '';
                }
            });
        }
    }

    // Bind Live Chat button to redirect to AI Assistant
    function bindLiveChatRedirect() {
        const liveChatBtn = document.getElementById('btn-channel-live-chat');
        if (liveChatBtn) {
            liveChatBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (typeof window.switchPanel === 'function') {
                    window.switchPanel('assistant');
                } else {
                    window.location.hash = '#assistant';
                }
                showHelpToast('Live Chat Connected', 'Connecting to Agri Link AI Agronomist Assistant...', 'success');
            });
        }
    }

    // Helper: Date format
    function formatDate(dateStr) {
        if (!dateStr) return 'Just now';
        try {
            const d = new Date(dateStr);
            if (isNaN(d.getTime())) return dateStr;
            const options = { day: '2-digit', month: 'short', year: 'numeric' };
            return d.toLocaleDateString('en-IN', options);
        } catch (e) {
            return dateStr;
        }
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
        return str.replace(/[&<>"']/g, m => map[m]);
    }

    // Initialize Help & Support Module
    function initHelpSupportModule() {
        const helpPanel = document.getElementById('panel-help');
        if (!helpPanel) return;

        renderTicketsTable();
        bindFaqAccordion();
        bindAttachmentPreview();
        bindLiveChatRedirect();

        const form = document.getElementById('support-ticket-form');
        if (form && !form._boundSubmit) {
            form.addEventListener('submit', handleTicketSubmit);
            form._boundSubmit = true;
        }
    }

    // Global Expose
    window.initHelpSupportModule = initHelpSupportModule;

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHelpSupportModule);
    } else {
        initHelpSupportModule();
    }
})();
