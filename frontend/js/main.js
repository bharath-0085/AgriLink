/**
 * Agri Link — Premium Vanilla JavaScript Interactivity
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize authentication check & lock states
    initAuthentication();

    // Initialize scrolling effect on Navbar
    initNavbarScroll();

    // Initialize Scroll Animations
    initScrollReveal();

    // Initialize Animated Counters
    initCounters();

    // Initialize Crop Disease Image Upload & Analysis
    initDiseaseDetection();

    // Initialize Crop Recommendation
    initCropRecommendation();

    // Initialize Marketplace Search & Filtering
    initMarketplaceFilter();

    // Initialize Forms Validation
    initFormValidation();

    // Initialize Booking Modal simulation
    initBookingWorkflow();
});

/**
 * Navbar scroll behavior
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar-custom');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Auto-close mobile navbar on clicking nav links
    const navCollapse = document.getElementById('navbarNav');
    if (navCollapse) {
        const navLinks = navCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navCollapse.classList.contains('show') && window.bootstrap && window.bootstrap.Collapse) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navCollapse) || new bootstrap.Collapse(navCollapse, { toggle: false });
                    bsCollapse.hide();
                }
            });
        });
    }

    // Smooth scrolling for anchor links with dynamic navbar offset
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (!targetId || targetId === '#') return;
            const targetElem = document.querySelector(targetId);
            if (targetElem) {
                e.preventDefault();
                const navHeight = navbar ? navbar.offsetHeight : 130;
                const elementPosition = targetElem.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - navHeight - 10;

                window.scrollTo({
                    top: Math.max(0, offsetPosition),
                    behavior: 'smooth'
                });

                // Update active link state
                document.querySelectorAll('.navbar-nav .nav-link').forEach(nl => nl.classList.remove('active'));
                const matchedNav = document.querySelector(`.navbar-nav .nav-link[href="${targetId}"]`);
                if (matchedNav) matchedNav.classList.add('active');

                if (history.pushState) {
                    history.pushState(null, null, targetId);
                }
            }
        });
    });

    // ScrollSpy: highlight active navbar item on scroll
    const sections = ['home', 'about', 'services', 'how-it-works', 'contact'];
    window.addEventListener('scroll', () => {
        const navHeight = navbar ? navbar.offsetHeight : 130;
        const scrollPos = window.scrollY + navHeight + 50;
        let currentSection = '';

        for (const secId of sections) {
            const sec = document.getElementById(secId);
            if (sec) {
                const top = sec.offsetTop;
                const height = sec.offsetHeight;
                if (scrollPos >= top && scrollPos < top + height) {
                    currentSection = secId;
                }
            }
        }

        if (currentSection) {
            document.querySelectorAll('.navbar-nav .nav-link').forEach(nl => {
                const href = nl.getAttribute('href');
                if (href === `#${currentSection}`) {
                    nl.classList.add('active');
                } else if (href && href.startsWith('#')) {
                    nl.classList.remove('active');
                }
            });
        }
    });
}

/**
 * Statistics counters - Kept strictly static as requested (3,410 / 8,525 / 1,705 / 5,115 / 98%)
 */
function initCounters() {
    // Intentionally kept static: values are fixed in HTML and never continuously recalculated
}

/**
 * Drag-and-drop crop disease upload & prediction simulation
 */
function initDiseaseDetection() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('leaf-image-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const placeholderText = document.getElementById('placeholder-text');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultCard = document.getElementById('result-card');
    const skeletonLoader = document.getElementById('skeleton-loader');

    if (!dropZone || !fileInput) return;

    // Handle drag events
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        }, false);
    });

    // Handle drop files
    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    // Handle zone click
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle input change
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        const file = files[0];

        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewContainer.classList.remove('d-none');
                placeholderText.classList.add('d-none');
                analyzeBtn.removeAttribute('disabled');
                
                // Hide past results
                resultCard.classList.add('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            alert('Please upload a valid image file of a leaf (JPEG/PNG).');
        }
    }

    // Diagnose Prediction Simulation
    analyzeBtn.addEventListener('click', () => {
        // Show Skeleton Loader
        skeletonLoader.classList.remove('d-none');
        resultCard.classList.add('d-none');
        analyzeBtn.setAttribute('disabled', 'true');

        // Simulated AI API delay (1.5 seconds)
        setTimeout(() => {
            skeletonLoader.classList.add('d-none');
            resultCard.classList.remove('d-none');
            analyzeBtn.removeAttribute('disabled');

            // Set result data
            document.getElementById('res-disease').innerText = 'Apple Black Rot';
            document.getElementById('res-confidence').innerText = '94.8%';
            document.getElementById('res-treatment').innerText = 'Prune out dead wood, mummified fruit, and cankers. Apply protective fungicides containing captan or thiophanate-methyl during early blossom period.';
            document.getElementById('res-prevention').innerText = 'Rake and destroy fallen leaves and debris from the orchard in autumn. Keep tree canopy open with regular pruning to maximize air circulation.';
            
            // Scroll to results
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 1500);
    });
}

/**
 * Filter crops dynamically in the marketplace section
 */
function initMarketplaceFilter() {
    const searchInput = document.getElementById('crop-search');
    const cropCards = document.querySelectorAll('.crop-item');

    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();

        cropCards.forEach(card => {
            const cropName = card.querySelector('.crop-title').innerText.toLowerCase();
            const location = card.querySelector('.crop-location').innerText.toLowerCase();

            if (cropName.includes(query) || location.includes(query)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

/**
 * Simple form validation for contact and auth modal forms
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation-custom');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            let isValid = true;
            const inputs = form.querySelectorAll('input, textarea, select');

            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (isValid) {
                // Mock Success Submission
                const submitBtn = form.querySelector('[type="submit"]');
                const prevText = submitBtn.innerText;
                submitBtn.innerText = 'Submitting...';
                submitBtn.setAttribute('disabled', 'true');

                setTimeout(() => {
                    submitBtn.innerText = 'Success!';
                    submitBtn.classList.remove('btn-primary-custom');
                    submitBtn.classList.add('btn-success');
                    
                    alert('Thank you! Your information has been processed.');
                    form.reset();

                    setTimeout(() => {
                        submitBtn.innerText = prevText;
                        submitBtn.classList.add('btn-primary-custom');
                        submitBtn.classList.remove('btn-success');
                        submitBtn.removeAttribute('disabled');
                    }, 2000);
                }, 1200);
            }
        });
    });
}

/**
 * Simulation workflow for modal actions (Book Now & Hire)
 */
function initBookingWorkflow() {
    const bookButtons = document.querySelectorAll('.book-equipment-btn');
    const hireButtons = document.querySelectorAll('.hire-worker-btn');
    const contactFarmerBtns = document.querySelectorAll('.contact-farmer-btn');

    bookButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const eqName = btn.getAttribute('data-eq');
            const price = btn.getAttribute('data-price');
            alert(`Equipment Booking request simulation:\n\nYou are requesting to book: ${eqName}\nRate: ${price}\n\nOur system has dispatched this request. Please log in to complete payment and view the owner's details.`);
        });
    });

    hireButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const workerName = btn.getAttribute('data-worker');
            const wage = btn.getAttribute('data-wage');
            alert(`Labour Hiring simulation:\n\nYou are requesting to hire: ${workerName}\nWage: ${wage}\n\nA notification request has been sent to the worker. Track statuses in your dashboard.`);
        });
    });

    contactFarmerBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const farmerName = btn.getAttribute('data-farmer');
            alert(`Chat Simulation:\n\nConnecting with Farmer ${farmerName}...\n\nPrivate chat room successfully initiated. Log in to send messages and crop purchase agreements.`);
        });
    });
}

/**
 * Scroll Reveal Effects
 */
function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal');

    const checkReveal = () => {
        const windowHeight = window.innerHeight;
        reveals.forEach(reveal => {
            const elementTop = reveal.getBoundingClientRect().top;
            const elementVisible = 100;

            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', checkReveal);
    // Initial check
    checkReveal();
}

/**
 * AI Crop Recommendation Form and Prediction simulation
 */
function initCropRecommendation() {
    const form = document.getElementById('crop-recommend-form');
    const autofillBtn = document.getElementById('autofill-btn');
    const resultDiv = document.getElementById('crop-result');

    if (!form) return;

    // Handle autofill click
    autofillBtn.addEventListener('click', () => {
        document.getElementById('input-n').value = 90;
        document.getElementById('input-p').value = 42;
        document.getElementById('input-k').value = 43;
        document.getElementById('input-ph').value = 6.5;
        document.getElementById('input-temp').value = 22;
        document.getElementById('input-humidity').value = 82;
        document.getElementById('input-rainfall').value = 200;
        
        // Clear past result animation
        resultDiv.classList.add('d-none');
    });

    // Handle submit
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Perform basic input validation
        const n = parseInt(document.getElementById('input-n').value, 10);
        const p = parseInt(document.getElementById('input-p').value, 10);
        const k = parseInt(document.getElementById('input-k').value, 10);
        const ph = parseFloat(document.getElementById('input-ph').value);
        const temp = parseFloat(document.getElementById('input-temp').value);
        const humidity = parseFloat(document.getElementById('input-humidity').value);
        const rainfall = parseFloat(document.getElementById('input-rainfall').value);

        const submitBtn = form.querySelector('[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Running AI Model...';
        submitBtn.setAttribute('disabled', 'true');
        resultDiv.classList.add('d-none');

        // Simulate model prediction delay (1.2s)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.removeAttribute('disabled');
            resultDiv.classList.remove('d-none');

            // Simple rules for realistic predictions matching general datasets
            let crop = 'Maize';
            let confidence = '88.7%';
            let analysis = 'The nutrients and climate metrics indicate a balanced clay-loam profile. Under these warm climate factors, Maize (corn) cultivation is highly recommended for best output.';

            if (rainfall > 170 && n > 70) {
                crop = 'Rice';
                confidence = '98.2%';
                analysis = 'High nitrogen (' + n + ' mg/kg) and abundant rainfall (' + rainfall + 'mm) are optimal for water-intensive cereals. Cultivating Basmati Rice will produce maximum output and premium market value.';
            } else if (p > 35 && temp < 20) {
                crop = 'Wheat';
                confidence = '95.6%';
                analysis = 'Cooler temperatures (' + temp + '°C) combined with high phosphorus levels (' + p + ' mg/kg) support winter seed germination. Wheat (Sharbati) is strongly suggested.';
            } else if (ph > 7.2 && k > 35) {
                crop = 'Cotton';
                confidence = '91.4%';
                analysis = 'Slightly alkaline soil (pH ' + ph + ') with rich potassium levels is the classic requirement for fiber crop stability. Black soil cotton farming is highly recommended.';
            } else if (rainfall < 70) {
                crop = 'Millets (Ragi)';
                confidence = '93.5%';
                analysis = 'Low rainfall (' + rainfall + 'mm) limits moisture for traditional crops. Drought-resistant Millets or Ragi are recommended for soil stability and water conservation.';
            }

            document.getElementById('recommended-crop-name').innerText = crop;
            document.getElementById('recommendation-confidence').innerText = confidence + ' Confidence';
            document.getElementById('recommendation-analysis-text').innerText = analysis;

            // Scroll result into view
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 1200);
    });
}

const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE = (window.location.protocol === 'file:' || (isLocalhost && window.location.port && window.location.port !== '8000')) 
    ? 'http://127.0.0.1:8000' 
    : '';

window.roleDetails = {
    'farmer': { emoji: '👨‍🌾', label: 'Farmer Login', hint: 'Enter your 10-digit mobile number to receive a verification code.', demoPhone: '9842199881' },
    'labour': { emoji: '👷', label: 'Labour Login', hint: 'Enter your 10-digit mobile number to view jobs & schedules.', demoPhone: '9842199883' },
    'buyer': { emoji: '🛒', label: 'Buyer Login', hint: 'Enter your registered email and password to access produce orders.', demoPhone: '' },
    'admin': { emoji: '👨‍💼', label: 'Admin Login', hint: 'Enter administrative credentials to access the operations portal.', demoPhone: '' }
};

window.showModalAlert = function(msg, isError = true) {
    const modalAlert = document.getElementById('modal-auth-alert');
    if (!modalAlert) return;
    modalAlert.className = isError ? 'alert alert-danger py-2 px-3 small rounded-3 mb-3' : 'alert alert-success py-2 px-3 small rounded-3 mb-3';
    modalAlert.innerHTML = msg;
    modalAlert.classList.remove('d-none');
};

window.clearModalAlert = function() {
    const modalAlert = document.getElementById('modal-auth-alert');
    if (modalAlert) {
        modalAlert.classList.add('d-none');
        modalAlert.innerHTML = '';
    }
};

window.selectRole = function(roleKey) {
    window.clearModalAlert();
    const authRoleInput = document.getElementById('auth-role');
    if (authRoleInput) authRoleInput.value = roleKey;

    const info = window.roleDetails[roleKey] || window.roleDetails['farmer'];
    const activeRolePill = document.getElementById('active-role-pill');
    if (activeRolePill) {
        activeRolePill.textContent = `${info.emoji} ${info.label}`;
        if (roleKey === 'admin') {
            activeRolePill.className = 'badge bg-danger-subtle text-danger px-3 py-2 rounded-pill fw-bold';
        } else if (roleKey === 'labour') {
            activeRolePill.className = 'badge bg-primary-subtle text-primary px-3 py-2 rounded-pill fw-bold';
        } else if (roleKey === 'buyer') {
            activeRolePill.className = 'badge bg-warning-subtle text-warning-emphasis px-3 py-2 rounded-pill fw-bold';
        } else {
            activeRolePill.className = 'badge bg-success-subtle text-success px-3 py-2 rounded-pill fw-bold';
        }
    }

    const roleLoginHint = document.getElementById('role-login-hint');
    if (roleLoginHint) roleLoginHint.textContent = info.hint;

    const roleSelectView = document.getElementById('auth-role-select-view');
    const roleFormView = document.getElementById('auth-form-view');
    if (roleSelectView && roleFormView) {
        roleSelectView.classList.add('d-none');
        roleFormView.classList.remove('d-none');
    }

    const step1Form = document.getElementById('auth-step-1');
    const step2Form = document.getElementById('auth-step-2');
    const buyerForm = document.getElementById('auth-buyer-form');
    const adminForm = document.getElementById('auth-admin-form');

    if (roleKey === 'admin') {
        if (step1Form) step1Form.classList.add('d-none');
        if (step2Form) step2Form.classList.add('d-none');
        if (buyerForm) buyerForm.classList.add('d-none');
        if (adminForm) {
            adminForm.classList.remove('d-none');
            const admUser = document.getElementById('modal-admin-username');
            if (admUser && !admUser.value) admUser.value = 'admin';
            const admPass = document.getElementById('modal-admin-password');
            if (admPass && !admPass.value) admPass.value = 'AdminMaster@2026';
            if (admUser) admUser.focus();
        }
    } else if (roleKey === 'buyer') {
        if (step1Form) step1Form.classList.add('d-none');
        if (step2Form) step2Form.classList.add('d-none');
        if (adminForm) adminForm.classList.add('d-none');
        if (buyerForm) {
            buyerForm.classList.remove('d-none');
            const buyerEmail = document.getElementById('modal-buyer-email');
            if (buyerEmail && !buyerEmail.value) buyerEmail.value = 'buyer@agrilink.in';
            const buyerPass = document.getElementById('modal-buyer-password');
            if (buyerPass && !buyerPass.value) buyerPass.value = 'Buyer@2026';
            if (buyerEmail) buyerEmail.focus();
        }
    } else {
        // Farmer or Labour (Phone + OTP)
        if (adminForm) adminForm.classList.add('d-none');
        if (buyerForm) buyerForm.classList.add('d-none');
        if (step1Form) step1Form.classList.remove('d-none');
        if (step2Form) step2Form.classList.add('d-none');
        const mobileInput = document.getElementById('auth-mobile');
        if (mobileInput) {
            mobileInput.value = info.demoPhone || '9842199881';
            mobileInput.focus();
        }
        const demoHint = document.getElementById('modal-demo-num');
        if (demoHint) demoHint.textContent = info.demoPhone || '9842199881';
    }
};

window.backToRoles = function() {
    window.clearModalAlert();
    const roleSelectView = document.getElementById('auth-role-select-view');
    const roleFormView = document.getElementById('auth-form-view');
    if (roleSelectView && roleFormView) {
        roleFormView.classList.add('d-none');
        roleSelectView.classList.remove('d-none');
    }
};

/**
 * Mobile Number & OTP Verification with Dynamic Feature Access Lock
 */
function initAuthentication() {
    const isUserLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const activeUserRole = localStorage.getItem('userRole');

    // 1. Navbar State Adjuster
    const navLoginBtn = document.querySelector('.navbar-custom button[data-bs-target="#loginModal"]');
    if (navLoginBtn) {
        const btnParent = navLoginBtn.parentNode;
        if (isUserLoggedIn && activeUserRole) {
            const dashLink = `${activeUserRole}_dashboard.html`;
            btnParent.innerHTML = `
                <a href="${dashLink}" class="btn btn-primary-custom px-4 me-2">
                    <i class="bi bi-grid-fill"></i> Go to Dashboard
                </a>
                <button class="btn btn-outline-danger rounded-pill px-3" id="nav-logout-btn">
                    <i class="bi bi-box-arrow-left"></i> Logout
                </button>
            `;
            const logoutBtn = document.getElementById('nav-logout-btn');
            if (logoutBtn) {
                logoutBtn.addEventListener('click', async () => {
                    const token = localStorage.getItem('token');
                    if (token) {
                        try {
                            await fetch(`${API_BASE}/api/v1/accounts/logout/`, {
                                method: 'POST',
                                headers: { 'Authorization': `Token ${token}` }
                            });
                        } catch(e) {
                            console.error("Logout error:", e);
                        }
                    }
                    localStorage.removeItem('token');
                    localStorage.removeItem('isLoggedIn');
                    localStorage.removeItem('userRole');
                    localStorage.removeItem('userName');
                    localStorage.removeItem('userMobile');
                    localStorage.removeItem('userId');
                    window.location.reload();
                });
            }
        }
    }

    // 2. Lock Overlays Toggle
    const lockOverlays = document.querySelectorAll('.locked-feature-overlay');
    if (isUserLoggedIn) {
        lockOverlays.forEach(overlay => {
            overlay.classList.add('d-none');
            const parent = overlay.parentNode;
            if (parent && parent.classList.contains('locked-feature-wrapper')) {
                parent.style.filter = 'none';
                parent.style.pointerEvents = 'auto';
            }
        });
    } else {
        lockOverlays.forEach(overlay => {
            overlay.classList.remove('d-none');
            const parent = overlay.parentNode;
            if (parent && parent.classList.contains('locked-feature-wrapper')) {
                parent.style.pointerEvents = 'none';
                overlay.style.pointerEvents = 'auto';
            }
        });
    }

    // 3. Modal role buttons & cards: Bind click events in addition to inline onclick
    document.querySelectorAll('.modal-role-quick-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const roleKey = btn.getAttribute('data-role');
            if (roleKey) window.selectRole(roleKey);
        });
    });

    document.querySelectorAll('.role-select-card, .role-grid-card').forEach(card => {
        card.addEventListener('click', () => {
            const roleKey = card.getAttribute('data-role');
            if (roleKey) window.selectRole(roleKey);
        });
    });

    const backToRolesBtn = document.getElementById('back-to-roles-btn');
    if (backToRolesBtn) {
        backToRolesBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.backToRoles();
        });
    }

    const demoNumHint = document.getElementById('modal-demo-num');
    if (demoNumHint) {
        demoNumHint.addEventListener('click', () => {
            const mob = document.getElementById('auth-mobile');
            if (mob) mob.value = demoNumHint.textContent.trim();
        });
    }

    // Reset view when modal is closed
    const loginModalEl = document.getElementById('loginModal');
    if (loginModalEl) {
        loginModalEl.addEventListener('hidden.bs.modal', () => {
            window.backToRoles();
            const step1Form = document.getElementById('auth-step-1');
            const step2Form = document.getElementById('auth-step-2');
            const buyerForm = document.getElementById('auth-buyer-form');
            const adminForm = document.getElementById('auth-admin-form');
            if (step1Form && step2Form) {
                step1Form.classList.remove('d-none');
                step2Form.classList.add('d-none');
            }
            if (buyerForm) buyerForm.classList.add('d-none');
            if (adminForm) adminForm.classList.add('d-none');
        });
    }

    // Edit mobile in Step 2
    const editMobileBtn = document.getElementById('modal-edit-mobile-btn');
    if (editMobileBtn) {
        editMobileBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const step1Form = document.getElementById('auth-step-1');
            const step2Form = document.getElementById('auth-step-2');
            if (step1Form && step2Form) {
                step2Form.classList.add('d-none');
                step1Form.classList.remove('d-none');
            }
            const mob = document.getElementById('auth-mobile');
            if (mob) mob.focus();
        });
    }

    // 4. Step 1: Submit Mobile -> Send Real OTP
    const step1Form = document.getElementById('auth-step-1');
    if (step1Form) {
        step1Form.addEventListener('submit', async (e) => {
            e.preventDefault();
            window.clearModalAlert();
            const mobileInput = document.getElementById('auth-mobile').value.trim();
            const authRoleInput = document.getElementById('auth-role');
            const roleSelect = (authRoleInput ? authRoleInput.value : 'farmer') || 'farmer';
            const sendBtn = document.getElementById('modal-send-otp-btn');
            const otpBanner = document.getElementById('modal-otp-info-banner');
            const otpMobileDisplay = document.getElementById('display-otp-mobile');
            const step2Form = document.getElementById('auth-step-2');

            if (!/^[0-9]{10}$/.test(mobileInput)) {
                window.showModalAlert("Please enter a valid 10-digit mobile number.");
                return;
            }

            const origText = sendBtn ? sendBtn.innerHTML : '';
            if (sendBtn) {
                sendBtn.disabled = true;
                sendBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Sending Secure OTP...`;
            }

            try {
                const fullPhone = mobileInput.startsWith('+91') ? mobileInput : `+91${mobileInput}`;
                const response = await fetch(`${API_BASE}/api/v1/accounts/otp/send/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone: fullPhone, role: roleSelect, purpose: 'login' })
                });
                const resData = await response.json();

                if (response.ok && resData.success) {
                    if (otpMobileDisplay) otpMobileDisplay.innerText = mobileInput;
                    const devOtp = resData.dev_otp || (resData.data && resData.data.dev_otp);
                    if (otpBanner) {
                        if (devOtp) {
                            otpBanner.innerHTML = `<i class="bi bi-shield-check me-1"></i> SMS Dispatch: Code <strong class="fs-6">${devOtp}</strong> (Valid 5 mins)<br><button type="button" class="btn btn-sm btn-outline-success py-0 px-2 mt-1" onclick="document.getElementById('auth-otp').value='${devOtp}'; document.getElementById('auth-otp').dispatchEvent(new Event('input', {bubbles:true}));">Auto-fill ${devOtp}</button>`;
                            const authOtp = document.getElementById('auth-otp');
                            if (authOtp) {
                                authOtp.value = devOtp;
                                authOtp.dispatchEvent(new Event('input', { bubbles: true }));
                                authOtp.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                        } else {
                            otpBanner.innerHTML = `<i class="bi bi-check-circle me-1"></i> 6-digit verification code sent via SMS to +91 ${mobileInput}`;
                        }
                    }
                    step1Form.classList.add('d-none');
                    if (step2Form) {
                        step2Form.classList.remove('d-none');
                        const authOtp = document.getElementById('auth-otp');
                        if (authOtp) authOtp.focus();
                    }
                } else {
                    let err = resData.message || resData.error || resData.detail || "Unable to send verification OTP.";
                    if (resData.errors) {
                        if (typeof resData.errors === 'string') {
                            err = resData.errors;
                        } else if (typeof resData.errors === 'object') {
                            const firstErr = Object.values(resData.errors).flat()[0];
                            if (firstErr) err = firstErr;
                        }
                    }
                    if (resData.requires_registration) {
                        err += ` <a href="login.html?action=register" class="fw-bold alert-link">Click here to register</a>.`;
                    }
                    window.showModalAlert(err);
                }
            } catch(err) {
                window.showModalAlert("Network error: " + err.message);
            } finally {
                if (sendBtn) {
                    sendBtn.disabled = false;
                    sendBtn.innerHTML = origText;
                }
            }
        });
    }

    // 5. Step 2: Submit OTP Verification
    const step2Form = document.getElementById('auth-step-2');
    if (step2Form) {
        step2Form.addEventListener('submit', async (e) => {
            e.preventDefault();
            window.clearModalAlert();
            const otpInput = document.getElementById('auth-otp').value.trim();
            const authRoleInput = document.getElementById('auth-role');
            const roleSelect = (authRoleInput ? authRoleInput.value : 'farmer') || 'farmer';
            const mobileInput = document.getElementById('auth-mobile').value.trim();
            const verifyBtn = document.getElementById('modal-verify-otp-btn');

            if (!/^[0-9]{6}$/.test(otpInput)) {
                window.showModalAlert("Please enter the 6-digit verification code.");
                return;
            }

            const origText = verifyBtn ? verifyBtn.innerHTML : '';
            if (verifyBtn) {
                verifyBtn.disabled = true;
                verifyBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Verifying Credentials...`;
            }

            try {
                const fullPhone = mobileInput.startsWith('+91') ? mobileInput : `+91${mobileInput}`;
                const response = await fetch(`${API_BASE}/api/v1/accounts/otp/verify/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone: fullPhone, otp: otpInput, role: roleSelect })
                });
                const resData = await response.json();
                
                if (response.ok && resData.success && resData.data && resData.data.token) {
                    // Success Login
                    localStorage.setItem('token', resData.data.token);
                    localStorage.setItem('isLoggedIn', 'true');
                    localStorage.setItem('userRole', resData.data.role);
                    localStorage.setItem('userName', resData.data.name || '');
                    localStorage.setItem('userMobile', resData.data.phone || mobileInput);
                    localStorage.setItem('userId', resData.data.user_id || '');

                    // Close login modal if open
                    const modalEl = document.getElementById('loginModal');
                    if (modalEl && window.bootstrap) {
                        const modalInstance = bootstrap.Modal.getInstance(modalEl);
                        if (modalInstance) modalInstance.hide();
                    }

                    window.showModalAlert(`<i class="bi bi-check-circle-fill me-1"></i> Verification successful! Opening dashboard...`, false);
                    setTimeout(() => {
                        window.location.href = resData.data.redirect_url || (roleSelect + "_dashboard.html");
                    }, 400);
                } else {
                    window.showModalAlert(resData.error || "Verification failed. The code may be incorrect or expired.");
                }
            } catch (err) {
                window.showModalAlert("Network error during verification: " + err.message);
            } finally {
                if (verifyBtn) {
                    verifyBtn.disabled = false;
                    verifyBtn.innerHTML = origText;
                }
            }
        });
    }

    // Admin Credentials Form Submit
    const adminForm = document.getElementById('auth-admin-form');
    if (adminForm) {
        adminForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            window.clearModalAlert();
            const username = document.getElementById('modal-admin-username').value.trim();
            const password = document.getElementById('modal-admin-password').value;
            const admBtn = document.getElementById('modal-admin-submit-btn');

            const origText = admBtn ? admBtn.innerHTML : '';
            if (admBtn) {
                admBtn.disabled = true;
                admBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Authenticating...`;
            }

            try {
                const response = await fetch(`${API_BASE}/api/v1/accounts/login/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ username: username, password: password, role: 'admin' })
                });
                const resData = await response.json();

                if (response.ok && resData.success && resData.data && resData.data.token) {
                    localStorage.setItem('token', resData.data.token);
                    localStorage.setItem('isLoggedIn', 'true');
                    localStorage.setItem('userRole', 'admin');
                    localStorage.setItem('userName', resData.data.name || 'Admin');
                    localStorage.setItem('userId', resData.data.user_id || '');

                    const modalEl = document.getElementById('loginModal');
                    if (modalEl && window.bootstrap) {
                        const modalInstance = bootstrap.Modal.getInstance(modalEl);
                        if (modalInstance) modalInstance.hide();
                    }

                    window.showModalAlert(`<i class="bi bi-shield-check me-1"></i> Admin authorization verified! Redirecting...`, false);
                    setTimeout(() => {
                        window.location.href = resData.data.redirect_url || "/admin/";
                    }, 400);
                } else {
                    window.showModalAlert(resData.error || resData.message || "Access denied: Administrator credentials required.");
                }
            } catch(err) {
                window.showModalAlert("Network error: " + err.message);
            } finally {
                if (admBtn) {
                    admBtn.disabled = false;
                    admBtn.innerHTML = origText;
                }
            }
        });
    }

    // Buyer Form Submit Handler (Email + Password)
    const buyerForm = document.getElementById('auth-buyer-form');
    if (buyerForm) {
        buyerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            window.clearModalAlert();
            const email = document.getElementById('modal-buyer-email').value.trim();
            const password = document.getElementById('modal-buyer-password').value;
            const buyerBtn = document.getElementById('modal-buyer-submit-btn');

            const origText = buyerBtn ? buyerBtn.innerHTML : '';
            if (buyerBtn) {
                buyerBtn.disabled = true;
                buyerBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Authenticating Buyer...`;
            }

            try {
                const response = await fetch(`${API_BASE}/api/v1/accounts/login/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ identifier: email, email: email, password: password, role: 'buyer' })
                });
                const resData = await response.json();

                if (response.ok && resData.success && resData.data && resData.data.token) {
                    localStorage.setItem('token', resData.data.token);
                    localStorage.setItem('isLoggedIn', 'true');
                    localStorage.setItem('userRole', 'buyer');
                    localStorage.setItem('userName', resData.data.name || 'Produce Buyer');
                    localStorage.setItem('userMobile', resData.data.phone || '');
                    localStorage.setItem('userId', resData.data.user_id || '');

                    const modalEl = document.getElementById('loginModal');
                    if (modalEl && window.bootstrap) {
                        const modalInstance = bootstrap.Modal.getInstance(modalEl);
                        if (modalInstance) modalInstance.hide();
                    }

                    window.showModalAlert(`<i class="bi bi-check-circle-fill me-1"></i> Buyer verified! Redirecting to dashboard...`, false);
                    setTimeout(() => {
                        window.location.href = resData.data.redirect_url || "buyer_dashboard.html";
                    }, 300);
                } else {
                    window.showModalAlert(resData.error || resData.message || "Buyer authentication failed. Please check your credentials.");
                }
            } catch(err) {
                window.showModalAlert("Network error: " + err.message);
            } finally {
                if (buyerBtn) {
                    buyerBtn.disabled = false;
                    buyerBtn.innerHTML = origText;
                }
            }
        });
    }

    // 6. Resend OTP trigger
    const resendBtn = document.getElementById('resend-otp-btn');
    if (resendBtn) {
        resendBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const mobileInput = document.getElementById('auth-mobile').value.trim();
            const authRoleInput = document.getElementById('auth-role');
            const roleSelect = (authRoleInput ? authRoleInput.value : 'farmer') || 'farmer';
            const otpBanner = document.getElementById('modal-otp-info-banner');
            if (otpBanner) {
                otpBanner.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Requesting new verification OTP...`;
            }

            try {
                const fullPhone = mobileInput.startsWith('+91') ? mobileInput : `+91${mobileInput}`;
                const resp = await fetch(`${API_BASE}/api/v1/accounts/otp/send/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phone: fullPhone, role: roleSelect, purpose: 'login' })
                });
                const data = await resp.json();
                const devOtp = data.dev_otp || (data.data && data.data.dev_otp);
                if (resp.ok && data.success) {
                    if (devOtp) {
                        otpBanner.innerHTML = `<i class="bi bi-shield-check me-1"></i> New OTP generated: <strong class="fs-6">${devOtp}</strong><br><button type="button" class="btn btn-sm btn-outline-success py-0 px-2 mt-1" onclick="document.getElementById('auth-otp').value='${devOtp}'; document.getElementById('auth-otp').dispatchEvent(new Event('input', {bubbles:true}));">Auto-fill ${devOtp}</button>`;
                        const authOtp = document.getElementById('auth-otp');
                        if (authOtp) {
                            authOtp.value = devOtp;
                            authOtp.dispatchEvent(new Event('input', { bubbles: true }));
                            authOtp.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    } else {
                        otpBanner.innerHTML = `<i class="bi bi-check-circle me-1"></i> A fresh verification OTP has been sent via SMS to +91 ${mobileInput}`;
                    }
                } else {
                    const err = data.message || data.error || data.detail || "Failed to resend OTP.";
                    window.showModalAlert(err);
                }
            } catch(e) {
                window.showModalAlert("Network error while resending OTP.");
            }
        });
    }
}

/**
 * Filter Marketplace Listings
 */
function filterMarketplace() {
    const searchInput = document.getElementById('marketplace-search').value.toLowerCase();
    const locationInput = document.getElementById('marketplace-location').value.toLowerCase();
    const priceInput = document.getElementById('marketplace-price').value;
    const maxPrice = priceInput ? parseFloat(priceInput) : Infinity;

    const cards = document.querySelectorAll('.market-card');
    let hasVisibleCards = false;

    cards.forEach(card => {
        const crop = (card.getAttribute('data-crop') || '').toLowerCase();
        const location = (card.getAttribute('data-location') || '').toLowerCase();
        const price = parseFloat(card.getAttribute('data-price') || '0');

        let isMatch = true;

        if (searchInput && !crop.includes(searchInput)) {
            isMatch = false;
        }
        if (locationInput && locationInput !== '' && !location.includes(locationInput)) {
            isMatch = false;
        }
        if (price > maxPrice) {
            isMatch = false;
        }

        if (isMatch) {
            card.style.display = 'block';
            hasVisibleCards = true;
        } else {
            card.style.display = 'none';
        }
    });

    const noResultsElem = document.getElementById('marketplace-no-results');
    if (noResultsElem) {
        if (!hasVisibleCards) {
            noResultsElem.classList.remove('d-none');
        } else {
            noResultsElem.classList.add('d-none');
        }
    }
}

/**
 * Open Buyer Contact Modal
 */
window.openBuyerContact = function(name, phone, crop) {
    document.getElementById('buyer-modal-name').innerText = name;
    document.getElementById('buyer-modal-phone').innerText = phone;
    document.getElementById('buyer-modal-crop').innerText = crop;
    
    const callBtn = document.getElementById('buyer-call-btn');
    callBtn.href = 'tel:' + phone.replace(/\s+/g, '');

    const modalEl = document.getElementById('contactBuyerModal');
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
};

