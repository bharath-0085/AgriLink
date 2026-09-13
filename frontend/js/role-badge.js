/**
 * Agri Link — Reusable DashboardRoleBadge Web Component
 * =======================================================
 * Automatically renders a consistent role identification badge
 * directly beneath the Agri Link branding in the dashboard sidebar.
 *
 * Usage:
 *   <dashboard-role-badge role="farmer"></dashboard-role-badge>
 *   <dashboard-role-badge role="labour"></dashboard-role-badge>
 *   <dashboard-role-badge role="buyer"></dashboard-role-badge>
 *   <dashboard-role-badge role="admin"></dashboard-role-badge>
 */

(function () {
    const ROLE_CONFIGS = {
        farmer: {
            icon: '🌱',
            label: 'FARMER DASHBOARD',
            className: 'sidebar-role-badge--farmer'
        },
        labour: {
            icon: '👷',
            label: 'LABOUR DASHBOARD',
            className: 'sidebar-role-badge--labour'
        },
        buyer: {
            icon: '🛒',
            label: 'BUYER DASHBOARD',
            className: 'sidebar-role-badge--buyer'
        },
        admin: {
            icon: '👨‍💼',
            label: 'ADMIN DASHBOARD',
            className: 'sidebar-role-badge--admin'
        }
    };

    function getRoleConfig(role) {
        const key = (role || 'farmer').toString().toLowerCase().trim();
        return ROLE_CONFIGS[key] || ROLE_CONFIGS.farmer;
    }

    function generateBadgeHTML(role) {
        const config = getRoleConfig(role);
        return `<span class="sidebar-role-badge ${config.className}" role="status" aria-label="${config.label}">
            <span class="role-badge-icon" aria-hidden="true">${config.icon}</span>
            <span class="role-badge-text">${config.label}</span>
        </span>`;
    }

    class DashboardRoleBadge extends HTMLElement {
        static get observedAttributes() {
            return ['role'];
        }

        connectedCallback() {
            this.render();
        }

        attributeChangedCallback(name, oldValue, newValue) {
            if (name === 'role' && oldValue !== newValue) {
                this.render();
            }
        }

        render() {
            const role = this.getAttribute('role') || 'farmer';
            this.innerHTML = generateBadgeHTML(role);
        }
    }

    if (typeof customElements !== 'undefined' && !customElements.get('dashboard-role-badge')) {
        customElements.define('dashboard-role-badge', DashboardRoleBadge);
    }

    // Expose helper globally
    window.generateRoleBadgeHTML = generateBadgeHTML;
    window.DashboardRoleBadge = DashboardRoleBadge;
})();
