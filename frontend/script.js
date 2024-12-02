const API_BASE = 'http://chatbot.codernet.uz';

function saveToken(token) {
    const expiry = new Date();
    expiry.setDate(expiry.getDate() + 2);
    localStorage.setItem('access_token', JSON.stringify({ token: token, expiry: expiry.toISOString() }));
}

let sign_form = document.getElementById('sign_form');
let email = document.getElementById('email');
let username = document.getElementById("username");
let password = document.getElementById("password");
let confirm_password = document.getElementById('confirm_password');
let error_page = document.getElementById('error_page');

sign_form.addEventListener('submit', async (event) => {
    event.preventDefault();
    error_page.innerHTML = ""; 

    if (password.value === confirm_password.value) {
        try {
            let response = await fetch(`${API_BASE}/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username.value,
                    email: email.value,
                    password: password.value,
                }),
            });

            if (response.ok) {
                let data = await response.json();
                saveToken(data.access_token);
                window.location.href = "index.html";
            } else {
                let error = await response.json();
                error_page.style.color = 'red';
                error_page.innerHTML = error.message || 'Invalid credentials';
            }
        } catch (err) {
            console.error("Network error:", err);
            error_page.style.color = 'red';
            error_page.innerHTML = "Network error. Please try again later.";
        }
    } else {
        error_page.style.color = 'red';
        error_page.innerHTML = "Passwords do not match";
    }
});
