/**
 * CyberGuard ML - Client-side Interactive Controls & UX Enhancements
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavToggle();
    initSmsCounter();
    initQuickSamples();
    initFormClearButtons();
    initCopyButtons();
    initFormSubmitStates();
});

/**
 * Mobile Navigation Menu Toggle
 */
function initNavToggle() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('show');
            const icon = navToggle.querySelector('i');
            if (icon) {
                if (navMenu.classList.contains('show')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-xmark');
                } else {
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                }
            }
        });

        // Close on clicking outside
        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('show');
                const icon = navToggle.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }
}

/**
 * Real-time SMS Character & Word Counter
 */
function initSmsCounter() {
    const textarea = document.getElementById('smsMessage');
    const counter = document.getElementById('smsCounter');

    if (textarea && counter) {
        const updateCount = () => {
            const text = textarea.value.trim();
            const charCount = textarea.value.length;
            const wordCount = text.length > 0 ? text.split(/\s+/).length : 0;
            counter.textContent = `${charCount} characters | ${wordCount} words`;
            
            // Highlight if exceeding standard single SMS length (160 chars)
            if (charCount > 160) {
                counter.style.color = '#F59E0B'; // amber
            } else {
                counter.style.color = 'var(--text-muted)';
            }
        };

        textarea.addEventListener('input', updateCount);
        updateCount(); // Initial execution
    }
}

/**
 * Quick Test Preset Sample Fillers
 */
function initQuickSamples() {
    const sampleButtons = document.querySelectorAll('.sample-btn');
    const smsInput = document.getElementById('smsMessage');
    const urlInput = document.getElementById('urlInput');

    sampleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const sampleText = btn.getAttribute('data-text');
            if (!sampleText) return;

            if (smsInput) {
                smsInput.value = sampleText;
                smsInput.focus();
                // Trigger counter update
                smsInput.dispatchEvent(new Event('input'));
                // Flash feedback
                btn.style.transform = 'scale(0.96)';
                setTimeout(() => { btn.style.transform = 'scale(1)'; }, 150);
            } else if (urlInput) {
                urlInput.value = sampleText;
                urlInput.focus();
                btn.style.transform = 'scale(0.96)';
                setTimeout(() => { btn.style.transform = 'scale(1)'; }, 150);
            }
        });
    });
}

/**
 * Input Clear Buttons
 */
function initFormClearButtons() {
    const clearSmsBtn = document.getElementById('clearSmsBtn');
    const smsInput = document.getElementById('smsMessage');
    if (clearSmsBtn && smsInput) {
        clearSmsBtn.addEventListener('click', () => {
            smsInput.value = '';
            smsInput.focus();
            smsInput.dispatchEvent(new Event('input'));
        });
    }

    const clearUrlBtn = document.getElementById('clearUrlBtn');
    const urlInput = document.getElementById('urlInput');
    if (clearUrlBtn && urlInput) {
        clearUrlBtn.addEventListener('click', () => {
            urlInput.value = '';
            urlInput.focus();
        });
    }
}

/**
 * Copy to Clipboard with Feedback
 */
function initCopyButtons() {
    const copyBtn = document.getElementById('copyResultBtn');
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const textToCopy = copyBtn.getAttribute('data-copy');
            if (!textToCopy) return;

            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalHtml = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fa-solid fa-check text-success"></i> Copied to Clipboard!';
                copyBtn.classList.add('btn-primary');
                copyBtn.classList.remove('btn-outline');

                setTimeout(() => {
                    copyBtn.innerHTML = originalHtml;
                    copyBtn.classList.remove('btn-primary');
                    copyBtn.classList.add('btn-outline');
                }, 2500);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        });
    }
}

/**
 * Form Submit Loading State
 */
function initFormSubmitStates() {
    const smsForm = document.getElementById('smsForm');
    const predictSmsBtn = document.getElementById('predictSmsBtn');
    if (smsForm && predictSmsBtn) {
        smsForm.addEventListener('submit', () => {
            predictSmsBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Message...';
            predictSmsBtn.disabled = true;
        });
    }

    const urlForm = document.getElementById('urlForm');
    const predictUrlBtn = document.getElementById('predictUrlBtn');
    if (urlForm && predictUrlBtn) {
        urlForm.addEventListener('submit', () => {
            predictUrlBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Extracting Features...';
            predictUrlBtn.disabled = true;
        });
    }
}

