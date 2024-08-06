document.addEventListener('DOMContentLoaded', function() {
    // Login Form Validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const email = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (!email || !password) {
                event.preventDefault();
                alert('Please fill in all fields.');
            }
        });
    }

    // Registration Form Validation
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const dob = document.getElementById('dob').value;
            const password = document.getElementById('password').value;

            if (!name || !email || !dob || !password) {
                event.preventDefault();
                alert('Please fill in all fields.');
            }
        });
    }
});
