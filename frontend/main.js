const BASE_API = 'http://chatbot.codernet.uz'
const token = localStorage.getItem('token');

document.addEventListener('DOMContentLoaded', function() {
    
    if (!token) {
        window.location.href = 'sign-up.html';
    } else {
        let api_url = `${BASE_API}/auth/login_with_token?token=` + token
        let response = fetch(api_url)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Invalid token');
            }
        })
        .then(data => {
            // document.getElementById('user-info').innerText = `Username: ${data.username}, ID: ${data.user_id}`;
        })
        .catch(error => {
            console.error(error);
            window.location.href = 'login.html';
        });
    }
});

const textarea = document.getElementById('message-input');

textarea.addEventListener('input', () => {
    textarea.style.height = 'auto'; 
    textarea.style.height = `${textarea.scrollHeight}px`;
});


const models_api = `${BASE_API}/promts/get_models?token=${token}`;
console.log(models_api)

const dropdownButton = document.getElementById('dropdownButton');
const dropdownMenu = document.getElementById('dropdownMenu');

async function fetchModels() {
    try {
        const response = await fetch(models_api);
        if (!response.ok) {
            throw new Error('Failed to fetch models');
        }
        console.log(response)
        const data = await response.json();
        console.log(data)
        if (data.status === 200 && data.models) {
            console.log('models', data.models.name)
            populateDropdown(data.models);
        } else {
            console.error('Invalid response:', data);
        }
    } catch (error) {
        console.error('Error fetching models:', error);
    }
}

// Populate dropdown with models
function populateDropdown(models) {
    models.forEach(model => {
        const button = document.createElement('button');
        button.textContent = model;
        button.addEventListener('click', () => {
            console.log(`Selected Model: ${model}`);
            dropdownMenu.style.display = 'none'; // Close dropdown after selection
            dropdownButton.textContent = model; // Update button text to selected model
        });
        dropdownMenu.appendChild(button);
    });
}

// Show or hide dropdown menu on button click
dropdownButton.addEventListener('click', () => {
    const isVisible = dropdownMenu.style.display === 'block';
    dropdownMenu.style.display = isVisible ? 'none' : 'block';
});

// Initialize
fetchModels();
