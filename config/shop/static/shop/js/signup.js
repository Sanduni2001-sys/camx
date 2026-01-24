document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById('password');
    const togglePassword = document.querySelector('.toggle-password');
    const strengthBar = document.querySelector('.strength-bar');
    const strengthText = document.querySelector('.strength-text');

    if(passwordInput){
        togglePassword.addEventListener('click', () => {
            passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
        });

        passwordInput.addEventListener('input', () => {
            const val = passwordInput.value;
            let score = 0;
            if(val.length >= 6) score++;
            if(/[A-Z]/.test(val)) score++;
            if(/[0-9]/.test(val)) score++;
            if(/[@$!%*?&]/.test(val)) score++;

            let width = 0, color = 'red', text = 'Weak';
            switch(score){
                case 0: width=0; text=''; break;
                case 1: width=25; color='red'; text='Weak'; break;
                case 2: width=50; color='orange'; text='Medium'; break;
                case 3: width=75; color='blue'; text='Strong'; break;
                case 4: width=100; color='green'; text='Very Strong'; break;
            }
            strengthBar.style.width = width+'%';
            strengthBar.style.background = color;
            strengthText.textContent = text;
        });
    }

    const emailInput = document.getElementById('email');
    if(emailInput){
        const emailFeedback = document.createElement('span');
        emailFeedback.classList.add('tooltip');
        emailFeedback.textContent = 'Enter a valid email';
        emailInput.parentNode.appendChild(emailFeedback);

        emailInput.addEventListener('input', () => {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if(regex.test(emailInput.value)){
                emailFeedback.textContent = 'Valid Email';
                emailFeedback.style.background = 'green';
            } else {
                emailFeedback.textContent = 'Invalid Email';
                emailFeedback.style.background = '#DB4437';
            }
        });
    }
});