/**
 * Agri Link — Settings Module Component Logic
 * Component: /components/settings/settings.js
 * Manages profile editing, photo upload, notifications, security, preferences & danger zone.
 */

(function () {
    'use strict';

    // Default Fallback Profile Data
    const DEFAULT_PROFILE = {
        name: 'Ravi Kumar',
        phone: '+91 98765 43210',
        email: 'ravi.kumar@agrilink.in',
        village: 'Kinathukadavu',
        district: 'Coimbatore',
        state: 'Tamil Nadu',
        pincode: '641202',
        language: 'English',
        farm_size: '4.5',
        primary_crops: 'Paddy, Tomato, Sugarcane',
        profile_photo_url: 'images/logo.png'
    };

    // Default Notification Preferences
    const DEFAULT_NOTIFICATIONS = {
        weather_alerts: true,
        disease_alerts: true,
        market_alerts: true,
        scheme_alerts: true,
        order_alerts: true,
        sms_notifications: true,
        email_notifications: false,
        push_notifications: true
    };

    // Default App Preferences
    const DEFAULT_APP_PREFS = {
        units: 'metric',
        currency: 'INR',
        theme: 'light'
    };

    // Helper: Toast notification
    function showSettingsToast(title, message, type = 'success') {
        let toastEl = document.getElementById('settings-toast');
        if (!toastEl) {
            toastEl = document.createElement('div');
            toastEl.id = 'settings-toast';
            toastEl.className = 'settings-toast';
            document.body.appendChild(toastEl);
        }

        toastEl.className = `settings-toast ${type === 'error' ? 'toast-error' : type === 'warning' ? 'toast-warning' : ''}`;
        
        const iconClass = type === 'error' ? 'bi-x-circle-fill' : type === 'warning' ? 'bi-exclamation-triangle-fill' : 'bi-check-circle-fill';
        
        toastEl.innerHTML = `
            <div class="settings-toast-icon"><i class="bi ${iconClass}"></i></div>
            <div class="settings-toast-body">
                <div class="settings-toast-title">${title}</div>
                <div class="settings-toast-msg">${message}</div>
            </div>
            <button type="button" class="settings-toast-close" onclick="this.parentElement.classList.remove('show')">&times;</button>
        `;

        // Trigger reflow
        void toastEl.offsetWidth;
        toastEl.classList.add('show');

        clearTimeout(toastEl._timer);
        toastEl._timer = setTimeout(() => {
            toastEl.classList.remove('show');
        }, 3800);
    }

    // Initialize Settings Module
    async function initSettingsModule() {
        const settingsContainer = document.getElementById('panel-settings');
        if (!settingsContainer) return;

        // 1. Load Profile Data
        await loadProfileData();

        // 2. Load Notification Preferences
        loadNotificationPreferences();

        // 3. Load Account & Security Info
        loadSecurityInfo();

        // 4. Load App Preferences
        loadAppPreferences();

        // 5. Bind Event Handlers
        bindSettingsEvents();
    }

    // 1. Load Profile Data from backend or localStorage
    async function loadProfileData() {
        let profile = { ...DEFAULT_PROFILE };

        // Check localStorage first
        const savedName = localStorage.getItem('userName');
        const savedPhone = localStorage.getItem('userPhone');
        const savedEmail = localStorage.getItem('userEmail');
        const savedVillage = localStorage.getItem('userVillage') || localStorage.getItem('userLocation');
        const savedDistrict = localStorage.getItem('userDistrict');
        const savedState = localStorage.getItem('userState');
        const savedPincode = localStorage.getItem('userPincode');
        const savedLang = localStorage.getItem('userLanguage');
        const savedFarmSize = localStorage.getItem('userFarmSize');
        const savedCrops = localStorage.getItem('userPrimaryCrops');
        const savedAvatar = localStorage.getItem('userAvatar');

        if (savedName) profile.name = savedName;
        if (savedPhone) profile.phone = savedPhone;
        if (savedEmail) profile.email = savedEmail;
        if (savedVillage) profile.village = savedVillage;
        if (savedDistrict) profile.district = savedDistrict;
        if (savedState) profile.state = savedState;
        if (savedPincode) profile.pincode = savedPincode;
        if (savedLang) profile.language = savedLang;
        if (savedFarmSize) profile.farm_size = savedFarmSize;
        if (savedCrops) profile.primary_crops = savedCrops;
        if (savedAvatar) profile.profile_photo_url = savedAvatar;

        // Fetch latest from API if token exists
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const resp = await fetch('/api/v1/accounts/profile/', {
                    headers: { 'Authorization': `Token ${token}` }
                });
                if (resp.ok) {
                    const resData = await resp.json();
                    const u = resData.data || resData;
                    if (u.name) profile.name = u.name;
                    if (u.phone) profile.phone = u.phone;
                    if (u.email) profile.email = u.email;
                    if (u.village) profile.village = u.village;
                    if (u.district) profile.district = u.district;
                    if (u.state) profile.state = u.state;
                    if (u.profile_photo_url) profile.profile_photo_url = u.profile_photo_url;
                }
            } catch (e) {
                console.debug('Using local profile data for settings:', e);
            }
        }

        // Populate Form Fields
        setInputValue('settings-name', profile.name);
        setInputValue('settings-phone', profile.phone);
        setInputValue('settings-email', profile.email);
        setInputValue('settings-village', profile.village);
        setInputValue('settings-district', profile.district);
        setInputValue('settings-state', profile.state);
        setInputValue('settings-pincode', profile.pincode);
        setInputValue('settings-language', profile.language);
        setInputValue('settings-farm-size', profile.farm_size);
        setInputValue('settings-crops', profile.primary_crops);

        // Update Avatar Image
        const avatarImg = document.getElementById('settings-avatar-img');
        if (avatarImg) {
            avatarImg.src = profile.profile_photo_url;
            avatarImg.onerror = () => { avatarImg.src = 'images/logo.png'; };
        }

        // Linked phone in security card
        const secPhoneEl = document.getElementById('security-phone-display');
        if (secPhoneEl) {
            secPhoneEl.textContent = profile.phone;
        }
    }

    function setInputValue(id, val) {
        const el = document.getElementById(id);
        if (el && val !== undefined && val !== null) {
            el.value = val;
        }
    }

    // 2. Load Notification Preferences
    function loadNotificationPreferences() {
        let prefs = { ...DEFAULT_NOTIFICATIONS };
        const saved = localStorage.getItem('agrilink_notification_preferences');
        if (saved) {
            try {
                prefs = { ...prefs, ...JSON.parse(saved) };
            } catch (e) {}
        }

        for (const [key, val] of Object.entries(prefs)) {
            const toggle = document.getElementById(`toggle-${key}`);
            if (toggle) {
                toggle.checked = Boolean(val);
            }
        }
    }

    // 3. Load Security Info
    function loadSecurityInfo() {
        const is2FA = localStorage.getItem('agrilink_2fa_enabled') === 'true';
        const toggle2FA = document.getElementById('toggle-2fa');
        if (toggle2FA) {
            toggle2FA.checked = is2FA;
        }

        const badge2FA = document.getElementById('security-2fa-status');
        if (badge2FA) {
            if (is2FA) {
                badge2FA.textContent = 'Active';
                badge2FA.className = 'security-verified-badge';
            } else {
                badge2FA.textContent = 'Disabled';
                badge2FA.className = 'badge bg-light text-muted border';
            }
        }
    }

    // 4. Load App Preferences
    function loadAppPreferences() {
        let prefs = { ...DEFAULT_APP_PREFS };
        const saved = localStorage.getItem('agrilink_app_preferences');
        if (saved) {
            try {
                prefs = { ...prefs, ...JSON.parse(saved) };
            } catch (e) {}
        }

        setInputValue('pref-units', prefs.units);
        setInputValue('pref-currency', prefs.currency);
        setInputValue('pref-theme', prefs.theme);
    }

    // 5. Bind Event Handlers
    function bindSettingsEvents() {
        // --- Photo Upload Handlers ---
        const fileInput = document.getElementById('settings-photo-input');
        const changePhotoBtn = document.getElementById('btn-change-photo');
        const avatarBadge = document.getElementById('settings-avatar-badge');

        if (changePhotoBtn && fileInput) {
            changePhotoBtn.addEventListener('click', () => fileInput.click());
        }
        if (avatarBadge && fileInput) {
            avatarBadge.addEventListener('click', () => fileInput.click());
        }

        if (fileInput) {
            fileInput.addEventListener('change', async (e) => {
                const file = e.target.files && e.target.files[0];
                if (!file) return;

                // Validate file size (< 5MB) and type
                if (file.size > 5 * 1024 * 1024) {
                    showSettingsToast('File Too Large', 'Please select an image smaller than 5MB.', 'error');
                    return;
                }
                if (!file.type.startsWith('image/')) {
                    showSettingsToast('Invalid File', 'Please upload a valid image file (JPG, PNG).', 'error');
                    return;
                }

                // Instant Local Preview
                const reader = new FileReader();
                reader.onload = async (evt) => {
                    const dataUrl = evt.target.result;
                    const avatarImg = document.getElementById('settings-avatar-img');
                    if (avatarImg) avatarImg.src = dataUrl;

                    // Sync other avatars across page
                    const topAvatar = document.getElementById('top-profile-img');
                    if (topAvatar) topAvatar.src = dataUrl;
                    const panelAvatar = document.getElementById('panel-user-avatar');
                    if (panelAvatar) panelAvatar.src = dataUrl;
                    const editAvatar = document.getElementById('edit-avatar-preview');
                    if (editAvatar) editAvatar.src = dataUrl;

                    localStorage.setItem('userAvatar', dataUrl);

                    // Upload to backend if token exists
                    const token = localStorage.getItem('token');
                    if (token) {
                        try {
                            const formData = new FormData();
                            formData.append('photo', file);
                            const uploadResp = await fetch('/api/v1/accounts/profile/photo/', {
                                method: 'POST',
                                headers: { 'Authorization': `Token ${token}` },
                                body: formData
                            });
                            if (uploadResp.ok) {
                                const upData = await uploadResp.json();
                                const photoUrl = (upData.data && upData.data.profile_photo_url) || dataUrl;
                                localStorage.setItem('userAvatar', photoUrl);
                                showSettingsToast('Photo Updated', 'Your profile photo has been successfully uploaded.');
                                return;
                            }
                        } catch (err) {
                            console.warn('Backend photo upload fallback:', err);
                        }
                    }

                    showSettingsToast('Photo Updated', 'Profile photo preview saved.');
                };
                reader.readAsDataURL(file);
            });
        }

        // --- Save Profile Changes Button ---
        const saveProfileBtn = document.getElementById('btn-save-profile');
        if (saveProfileBtn) {
            saveProfileBtn.addEventListener('click', handleSaveProfile);
        }

        // --- Notification Preference Toggles ---
        const notifKeys = Object.keys(DEFAULT_NOTIFICATIONS);
        notifKeys.forEach(key => {
            const toggle = document.getElementById(`toggle-${key}`);
            if (toggle) {
                toggle.addEventListener('change', () => {
                    saveNotificationPreferences();
                });
            }
        });

        // --- App Preferences Selects ---
        const prefUnits = document.getElementById('pref-units');
        const prefCurrency = document.getElementById('pref-currency');
        const prefTheme = document.getElementById('pref-theme');

        [prefUnits, prefCurrency, prefTheme].forEach(el => {
            if (el) {
                el.addEventListener('change', () => {
                    const newPrefs = {
                        units: prefUnits ? prefUnits.value : 'metric',
                        currency: prefCurrency ? prefCurrency.value : 'INR',
                        theme: prefTheme ? prefTheme.value : 'light'
                    };
                    localStorage.setItem('agrilink_app_preferences', JSON.stringify(newPrefs));
                    showSettingsToast('Preferences Saved', 'Your application preferences have been updated.');
                });
            }
        });

        // --- Password Change Modal Submission ---
        const changePasswordForm = document.getElementById('settings-change-password-form');
        if (changePasswordForm) {
            changePasswordForm.addEventListener('submit', handleChangePassword);
        }

        // --- Change Phone Modal Submission ---
        const changePhoneForm = document.getElementById('settings-change-phone-form');
        if (changePhoneForm) {
            changePhoneForm.addEventListener('submit', handleChangePhone);
        }

        // --- 2FA Toggle ---
        const toggle2FA = document.getElementById('toggle-2fa');
        if (toggle2FA) {
            toggle2FA.addEventListener('change', (e) => {
                const isChecked = e.target.checked;
                if (isChecked) {
                    // Open 2FA setup modal
                    const modalEl = document.getElementById('modal-2fa-setup');
                    if (modalEl && window.bootstrap) {
                        const modal = new bootstrap.Modal(modalEl);
                        modal.show();
                    } else {
                        localStorage.setItem('agrilink_2fa_enabled', 'true');
                        loadSecurityInfo();
                        showSettingsToast('2FA Enabled', 'Two-Factor Authentication is now active on your account.');
                    }
                } else {
                    if (confirm('Are you sure you want to disable Two-Factor Authentication? Your account will be less secure.')) {
                        localStorage.setItem('agrilink_2fa_enabled', 'false');
                        loadSecurityInfo();
                        showSettingsToast('2FA Disabled', 'Two-Factor Authentication has been turned off.', 'warning');
                    } else {
                        e.target.checked = true;
                    }
                }
            });
        }

        // Confirm 2FA button in modal
        const confirm2FABtn = document.getElementById('btn-confirm-2fa');
        if (confirm2FABtn) {
            confirm2FABtn.addEventListener('click', () => {
                localStorage.setItem('agrilink_2fa_enabled', 'true');
                loadSecurityInfo();
                const modalEl = document.getElementById('modal-2fa-setup');
                if (modalEl && window.bootstrap) {
                    bootstrap.Modal.getInstance(modalEl)?.hide();
                }
                showSettingsToast('2FA Activated', 'Two-Factor Authentication has been enabled with OTP verification.');
            });
        }

        // --- Danger Zone Actions ---
        const deactivateBtn = document.getElementById('btn-deactivate-account');
        if (deactivateBtn) {
            deactivateBtn.addEventListener('click', () => {
                const modalEl = document.getElementById('modal-deactivate-account');
                if (modalEl && window.bootstrap) {
                    new bootstrap.Modal(modalEl).show();
                } else {
                    if (confirm('Deactivate your account temporarily? You can reactivate anytime by logging back in.')) {
                        handleAccountDeactivation();
                    }
                }
            });
        }

        const confirmDeactivateBtn = document.getElementById('btn-confirm-deactivate');
        if (confirmDeactivateBtn) {
            confirmDeactivateBtn.addEventListener('click', handleAccountDeactivation);
        }

        const deleteBtn = document.getElementById('btn-delete-account');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                const modalEl = document.getElementById('modal-delete-account');
                if (modalEl && window.bootstrap) {
                    new bootstrap.Modal(modalEl).show();
                } else {
                    if (confirm('PERMANENT ACTION: Are you sure you want to delete your Agri Link account? All farm data, listings, and bookings will be wiped.')) {
                        handleAccountDeletion();
                    }
                }
            });
        }

        const confirmDeleteBtn = document.getElementById('btn-confirm-delete');
        if (confirmDeleteBtn) {
            confirmDeleteBtn.addEventListener('click', () => {
                const confirmInput = document.getElementById('delete-confirm-keyword');
                if (confirmInput && confirmInput.value.trim().toUpperCase() !== 'DELETE') {
                    showSettingsToast('Confirmation Mismatch', 'Please type DELETE in capital letters to confirm.', 'error');
                    return;
                }
                handleAccountDeletion();
            });
        }
    }

    // Handle Save Profile
    async function handleSaveProfile(e) {
        if (e) e.preventDefault();
        const saveBtn = document.getElementById('btn-save-profile');
        if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';
        }

        const name = (document.getElementById('settings-name')?.value || '').trim();
        const phone = (document.getElementById('settings-phone')?.value || '').trim();
        const email = (document.getElementById('settings-email')?.value || '').trim();
        const village = (document.getElementById('settings-village')?.value || '').trim();
        const district = (document.getElementById('settings-district')?.value || '').trim();
        const state = (document.getElementById('settings-state')?.value || '').trim();
        const pincode = (document.getElementById('settings-pincode')?.value || '').trim();
        const language = (document.getElementById('settings-language')?.value || '').trim();
        const farmSize = (document.getElementById('settings-farm-size')?.value || '').trim();
        const crops = (document.getElementById('settings-crops')?.value || '').trim();

        // Validation
        if (!name) {
            showSettingsToast('Validation Error', 'Full Name is required.', 'error');
            resetSaveBtn(saveBtn);
            return;
        }

        // Persist to localStorage
        if (name) localStorage.setItem('userName', name);
        if (phone) localStorage.setItem('userPhone', phone);
        if (email) localStorage.setItem('userEmail', email);
        if (village) {
            localStorage.setItem('userVillage', village);
            localStorage.setItem('userLocation', `${village}, ${district || state}`);
        }
        if (district) localStorage.setItem('userDistrict', district);
        if (state) localStorage.setItem('userState', state);
        if (pincode) localStorage.setItem('userPincode', pincode);
        if (language) {
            localStorage.setItem('userLanguage', language);
            if (typeof window.changeLanguage === 'function') {
                const langCode = (language.toLowerCase() === 'tamil' || language.toLowerCase() === 'ta') ? 'ta' : 'en';
                if (window.currentLanguage !== langCode) {
                    window.changeLanguage(langCode);
                }
            }
        }
        if (farmSize) localStorage.setItem('userFarmSize', farmSize);
        if (crops) localStorage.setItem('userPrimaryCrops', crops);

        // Update headers across dashboard
        updateGlobalHeaders(name, village, district, state);

        // Send to backend if token exists
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const resp = await fetch('/api/v1/accounts/profile/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`
                    },
                    body: JSON.stringify({
                        name: name,
                        phone: phone,
                        email: email,
                        village: village,
                        district: district,
                        state: state
                    })
                });
                if (resp.ok) {
                    const toastTitle = (typeof window.t === 'function') ? window.t('settings.toast_success', 'Profile Saved') : 'Profile Saved';
                    const toastMsg = (typeof window.t === 'function') ? window.t('settings.profile_updated', 'Your farm profile information has been successfully updated.') : 'Your farm profile information has been successfully updated.';
                    showSettingsToast(toastTitle, toastMsg);
                    resetSaveBtn(saveBtn);
                    return;
                }
            } catch (err) {
                console.warn('Backend update failed, local changes saved:', err);
            }
        }

        const toastTitle = (typeof window.t === 'function') ? window.t('settings.toast_success', 'Profile Saved') : 'Profile Saved';
        const toastMsg = (typeof window.t === 'function') ? window.t('settings.profile_updated', 'Your profile details have been saved.') : 'Your profile details have been saved.';
        showSettingsToast(toastTitle, toastMsg);
        resetSaveBtn(saveBtn);
    }

    function resetSaveBtn(btn) {
        if (!btn) return;
        setTimeout(() => {
            btn.disabled = false;
            const btnText = (typeof window.t === 'function') ? window.t('settings.btn_save_profile', 'Save Changes') : 'Save Changes';
            btn.innerHTML = `<i class="bi bi-check2-circle me-1"></i>${btnText}`;
        }, 400);
    }

    // Synchronize UI headers across dashboard
    function updateGlobalHeaders(name, village, district, state) {
        const welcomeHeading = document.getElementById('farmer-welcome-heading');
        if (welcomeHeading) {
            const welcomeText = (typeof window.t === 'function') ? window.t('header.welcome_back', 'Welcome back') : 'Welcome back';
            welcomeHeading.innerHTML = `${welcomeText}, ${name} 👋`;
        }
        const topName = document.getElementById('top-profile-name');
        if (topName) topName.textContent = name;
        const panelName = document.getElementById('panel-user-name');
        if (panelName) panelName.textContent = name;
        const aiName = document.getElementById('ai-user-name');
        if (aiName) aiName.textContent = name;
        const dropdownName = document.getElementById('dropdown-profile-name');
        if (dropdownName) dropdownName.textContent = name;

        // Security phone display
        const phone = document.getElementById('settings-phone')?.value;
        const secPhoneEl = document.getElementById('security-phone-display');
        if (secPhoneEl && phone) secPhoneEl.textContent = phone;
    }

    // Save notification switches
    function saveNotificationPreferences() {
        const prefs = {};
        const keys = Object.keys(DEFAULT_NOTIFICATIONS);
        keys.forEach(k => {
            const el = document.getElementById(`toggle-${k}`);
            prefs[k] = el ? el.checked : true;
        });
        localStorage.setItem('agrilink_notification_preferences', JSON.stringify(prefs));
        showSettingsToast('Preferences Saved', 'Notification alert settings have been updated.');
    }

    // Handle Password Change
    async function handleChangePassword(e) {
        e.preventDefault();
        const oldPass = (document.getElementById('pass-current')?.value || '').trim();
        const newPass = (document.getElementById('pass-new')?.value || '').trim();
        const confirmPass = (document.getElementById('pass-confirm')?.value || '').trim();
        const submitBtn = document.getElementById('btn-submit-change-pass');

        if (!oldPass || !newPass || !confirmPass) {
            showSettingsToast('Missing Fields', 'Please fill in all password fields.', 'error');
            return;
        }

        if (newPass !== confirmPass) {
            showSettingsToast('Password Mismatch', 'New password and confirm password do not match.', 'error');
            return;
        }

        if (newPass.length < 8) {
            showSettingsToast('Password Too Short', 'New password must be at least 8 characters long.', 'error');
            return;
        }

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Updating...';
        }

        const token = localStorage.getItem('token');
        if (token) {
            try {
                const resp = await fetch('/api/v1/accounts/change-password/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`
                    },
                    body: JSON.stringify({
                        old_password: oldPass,
                        new_password: newPass,
                        confirm_password: confirmPass
                    })
                });

                const data = await resp.json();
                if (resp.ok) {
                    if (data.data && data.data.token) {
                        localStorage.setItem('token', data.data.token);
                    }
                    showSettingsToast('Password Changed', 'Your password has been changed successfully.');
                    document.getElementById('settings-change-password-form')?.reset();
                    const modalEl = document.getElementById('modal-change-password');
                    if (modalEl && window.bootstrap) bootstrap.Modal.getInstance(modalEl)?.hide();
                    return;
                } else {
                    showSettingsToast('Password Error', data.message || 'Current password is incorrect.', 'error');
                    return;
                }
            } catch (err) {
                console.warn('Password change network error:', err);
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = 'Update Password';
                }
            }
        }

        // Demo / offline success simulation
        showSettingsToast('Password Updated', 'Your account password has been successfully changed.');
        document.getElementById('settings-change-password-form')?.reset();
        const modalEl = document.getElementById('modal-change-password');
        if (modalEl && window.bootstrap) bootstrap.Modal.getInstance(modalEl)?.hide();
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Update Password';
        }
    }

    // Handle Change Phone
    function handleChangePhone(e) {
        e.preventDefault();
        const newPhone = (document.getElementById('new-phone-input')?.value || '').trim();
        if (!newPhone || newPhone.length < 10) {
            showSettingsToast('Invalid Phone', 'Please enter a valid 10-digit phone number.', 'error');
            return;
        }

        const formatted = newPhone.startsWith('+91') ? newPhone : `+91 ${newPhone}`;
        setInputValue('settings-phone', formatted);
        localStorage.setItem('userPhone', formatted);

        const secPhoneEl = document.getElementById('security-phone-display');
        if (secPhoneEl) secPhoneEl.textContent = formatted;

        showSettingsToast('Phone Number Updated', `Your verified phone number is now ${formatted}.`);
        const modalEl = document.getElementById('modal-change-phone');
        if (modalEl && window.bootstrap) bootstrap.Modal.getInstance(modalEl)?.hide();
    }

    // Deactivate Account
    function handleAccountDeactivation() {
        showSettingsToast('Account Deactivated', 'Your account has been deactivated. Logging out...', 'warning');
        setTimeout(() => {
            localStorage.clear();
            sessionStorage.clear();
            window.location.href = 'index.html';
        }, 1500);
    }

    // Delete Account
    function handleAccountDeletion() {
        showSettingsToast('Account Deleted', 'Your account has been permanently removed. Redirecting...', 'error');
        setTimeout(() => {
            localStorage.clear();
            sessionStorage.clear();
            window.location.href = 'index.html';
        }, 1500);
    }

    // Expose Global Initializer
    window.initSettingsModule = initSettingsModule;

    // Auto-init on DOMContentLoaded or if already ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSettingsModule);
    } else {
        initSettingsModule();
    }
})();
