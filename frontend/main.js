const BASE_API = 'http://chatbot.codernet.uz';
const token = localStorage.getItem('token');
let model_name = 'gpt-4o-mini';
let model_id = 1;

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
            populateDropdown(data.models);
        } else {
            console.error('Invalid response:', data);
        }
    } catch (error) {
        console.error('Error fetching models:', error);
    }
}

function populateDropdown(models) {
    models.forEach(model => {
        const button = document.createElement('button');
        button.textContent = model.name;
        button.addEventListener('click', () => {
            console.log(`Selected Model: ${model.name}`);
            dropdownMenu.style.display = 'none'; 
            dropdownButton.textContent = model.name;
            model_id = model.id
            model_name = model.name
        });
        dropdownMenu.appendChild(button);
    });
}

// Show or hide dropdown menu on button click
dropdownButton.addEventListener('click', () => {
    const isVisible = dropdownMenu.style.display === 'block';
    dropdownMenu.style.display = isVisible ? 'none' : 'block';
});
fetchModels();
