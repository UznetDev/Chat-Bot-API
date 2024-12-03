const BASE_API = 'http://127.0.0.1:8000';


const token = localStorage.getItem('token');
let model_name = 'gpt-4o-mini';
let model_id = 1;
let chat_id = false;
let chats_message = [];


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
            document.getElementById('user-info').innerText = `Welcom: ${data.username}`;
        })
        .catch(error => {
            console.error(error);
            window.location.href = 'login.html';
        });
    }
});

const user_message = document.getElementById('message-input');

user_message.addEventListener('input', () => {
    user_message.style.height = 'auto'; 
    user_message.style.height = `${user_message.scrollHeight}px`;
});


const models_api = `${BASE_API}/promts/get_models?token=${token}`;

const dropdownButton = document.getElementById('dropdownButton');
const dropdownMenu = document.getElementById('dropdownMenu');

async function fetchModels() {
    try {
        const response = await fetch(models_api);
        if (!response.ok) {
            throw new Error('Failed to fetch models');
        }
        const data = await response.json();
        if (data.status === 200 && data.models) {
            document.getElementById('description').innerText = data.models[0].description;
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
            console.log(`Selected Model: ${model.name}, ${model.id}`);
            dropdownMenu.style.display = 'none'; 
            dropdownButton.textContent = model.name;
            model_id = model.id
            model_name = model.name
            document.getElementById('description').innerText = model.description;
        });
        dropdownMenu.appendChild(button);
    });
}
dropdownButton.addEventListener('click', () => {
    const isVisible = dropdownMenu.style.display === 'block';
    dropdownMenu.style.display = isVisible ? 'none' : 'block';
});
fetchModels();



let send_button = document.getElementById('send-button');
let meassage_box = document.getElementById('meassage_box');


send_button.addEventListener('click', async () => {
    try {
        if (!chat_id) { // Check if chat_id is false or undefined
            const chat_api = `${BASE_API}/user/create_chat?token=${token}&model_id=${model_id}`;
            
            // Await response from fetch
            const response = await fetch(chat_api);
            if (!response.ok) {
                throw new Error('Invalid token');
            }

            const data = await response.json();
            chat_id = data.chat_id; // Update chat_id
            console.log("Chat ID:", chat_id);
        }

        // Send the user message
        const userMessage = user_message.value;
        const answer_api = `${BASE_API}/promts/answer?question=${encodeURIComponent(userMessage)}&chat_id=${chat_id}&token=${token}&model_id=${model_id}`;
        console.log("Answer API:", answer_api);

        const get_answer = await fetch(answer_api);
        if (!get_answer.ok) {
            throw new Error('Failed to fetch the answer');
        }

        const answerData = await get_answer.json();

        // Create user message element
        const userDiv = document.createElement("div");
        userDiv.className = "message user";
        userDiv.innerHTML = `<strong>You:</strong> ${userMessage}`;
        meassage_box.appendChild(userDiv);

        // Create bot message element
        const botDiv = document.createElement("div");
        botDiv.className = "message bot";
        botDiv.innerHTML = `<strong>Bot:</strong> ${answerData.answer}`;
        meassage_box.appendChild(botDiv);


        user_message.value = '';
    } catch (error) {
        console.error("Error:", error);
    }
});



function message_box(){
    if (chats_message = []){
        meassage_box.innerHTML = "<p id='assitant_message'>What can i do for you?<p/>"
    }
    else{

    }
}
message_box();


// Example markdown text
const markdownText = `
Here's a simple Python code to print "Hello, World!": 

\`\`\`python
print("Hello, World!")
\`\`\`

This is the standard way to output "Hello, World!" in Python. Let me know if you'd like variations or something more!
`;

// Convert Markdown to HTML
const htmlContent = marked.parse(markdownText, {
    highlight: function (code, lang) {
        const validLang = hljs.getLanguage(lang) ? lang : 'plaintext';
        return hljs.highlight(code, { language: validLang }).value;
    },
});

// Display rendered HTML in the output div
document.getElementById('markdown-output').innerHTML = htmlContent;
