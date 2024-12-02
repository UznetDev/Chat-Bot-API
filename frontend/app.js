const API_BASE = 'http://chatbot.codernet.uz'; // Replace with your API base URL

// Utility to save token for 2 days
function saveToken(token) {
    const expiry = new Date();
    expiry.setDate(expiry.getDate() + 2); // Token valid for 2 days
    localStorage.setItem('access_token', JSON.stringify({ token, expiry }));
}

// Utility to check token validity
function isTokenValid() {
    const tokenData = JSON.parse(localStorage.getItem('access_token'));
    if (!tokenData) return false;
    return new Date(tokenData.expiry) > new Date(); // Check if expiry date is valid
}

// Redirect to login.html if token is invalid
if (location.pathname === '/index.html') {
    const tokenData = JSON.parse(localStorage.getItem('access_token'));
    if (!tokenData || new Date(tokenData.expiry) <= new Date()) {
        alert('Session expired or not logged in. Redirecting to Login.');
        location.href = 'login.html';
    }
}

// Handle login form submission
if (location.pathname === '/login.html') {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                saveToken(data.access_token);
                alert('Login successful!');
                location.href = 'index.html'; // Redirect to index.html on success
            } else {
                alert('Login failed: ' + data.detail || 'Invalid credentials');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

// Handle registration form submission
if (location.pathname === '/sign-up.html') {
    document.getElementById('signUpForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password }),
            });
            const data = await response.json();
            if (response.ok) {
                saveToken(data.access_token);
                alert('Registration successful!');
                location.href = 'index.html'; // Redirect to index.html on success
            } else {
                alert('Registration failed: ' + data.detail || 'Error occurred');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

// Handle logout
if (location.pathname === '/index.html') {
    document.getElementById('logout').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        alert('Logged out successfully!');
        location.href = 'login.html'; // Redirect to login.html on logout
    });
}
