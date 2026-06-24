// ============================================
// ابزارهای مدیریت رمز عبور
// ============================================

function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    const eyeOpen = button.querySelector('.eye-icon:not(.eye-closed)');
    const eyeClosed = button.querySelector('.eye-closed');
    
    if (input.type === 'password') {
        input.type = 'text';
        if (eyeOpen) eyeOpen.style.display = 'none';
        if (eyeClosed) eyeClosed.style.display = 'block';
    } else {
        input.type = 'password';
        if (eyeOpen) eyeOpen.style.display = 'block';
        if (eyeClosed) eyeClosed.style.display = 'none';
    }
}

// فعال‌سازی خودکار برای تمام فیلدهای رمز
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toggle-password').forEach(function(btn) {
        const inputId = btn.getAttribute('data-target') || 
                       btn.closest('.password-input-group').querySelector('input').id;
        if (inputId) {
            btn.setAttribute('onclick', `togglePassword('${inputId}', this)`);
        }
    });
});