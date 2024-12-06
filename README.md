# Chat-Bot-API Documentation

## Overview
Chat-Bot-API is a robust **FastAPI-based chatbot service** designed to provide users with an interactive AI-powered chat experience. This project integrates **Retrieval-Augmented Generation (RAG)** with OpenAI models, allowing seamless interactions with documents and custom models. Additionally, the project incorporates the free-to-use **LLAMA model**, making advanced AI technology accessible to all.

The service is modular, scalable, and open source, aiming to deliver efficient AI-driven solutions to users while ensuring flexibility and extensibility.

---

## What is the Focus?
The primary goal of Chat-Bot-API is to:
- **Simplify AI model interaction**: By integrating document retrieval and conversational AI.
- **Enhance user engagement**: With personalized chatbots for every user.
- **Democratize AI access**: Through open-source implementation and free-to-use models.
- **Promote collaboration**: By offering a customizable and modular codebase for contributors.

---

## Features
1. **User Authentication**:
   - Token-based secure login and registration.
   - Persistent session management.

2. **Chatbot Interaction**:
   - Personalized chat experiences for users.
   - Support for both OpenAI models and free LLAMA models.
   - Integration of document-based queries via RAG.

3. **Model Management**:
   - Upload custom models with metadata and visibility options.
   - Delete and manage existing models.

4. **Dynamic Chat History**:
   - Save, retrieve, and manage chat messages.
   - Efficient handling of large conversations.

5. **CORS Middleware**:
   - Configured for cross-origin resource sharing to enable broader API usage.

6. **Open Source**:
   - Fully transparent and modifiable for developers and organizations.

---

## Installation

### Prerequisites
1. **Python**: Ensure you have Python 3.10 or above installed.
2. **MySQL**: Set up a MySQL database.
3. **Git**: Clone the repository.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/UznetDev/Chat-Bot-API.git
   cd Chat-Bot-API
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # For Linux/Mac
   env\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Environment Variables**:
   - Create a `.env` file in the `data` directory and add:
     ```env
     MYSQL_HOST=<Your MySQL Host>
     MYSQL_USER=<Your MySQL User>
     MYSQL_PASSWORD=<Your MySQL Password>
     MYSQL_DATABASE=<Your Database Name>
     REPLECATE_API=<Your Replicate API Key>
     ```

5. **Run the Application**:
   ```bash
   fastapi dev main.py
   ```

6. **Access the API**:
   Open `http://127.0.0.1:8000/docs` in your browser for interactive API documentation.

---

## How It Works
1. **User Workflow**:
   - Users authenticate using tokens.
   - They can interact with chatbots linked to their accounts.
   - Chatbots process user queries and retrieve AI-generated answers.

2. **Model Integration**:
   - OpenAI models and LLAMA models are used for RAG and general conversational tasks.
   - Users can upload custom models for tailored experiences.

3. **Database Management**:
   - Stores user data, chat history, and model metadata in MySQL.

4. **CORS Middleware**:
   - Enables seamless API access from different domains.

---

## Project Structure
```
Chat-Bot-API/
│
├── data/               # Configuration and environment files
│   ├── config.py
│
├── db/                 # Database connection and utility scripts
│   ├── database.py
│
├── models/             # Language model handling
│   ├── llm.py
│
├── routes/             # FastAPI route definitions
│   ├── auth.py
│   ├── promts.py
│   ├── user_page.py
│
├── functions/          # Utility functions
│   ├── functions.py
│
├── main.py             # Entry point of the application
├── loader.py           # Initialization of core components
├── requirements.txt    # Python dependencies
├── README.md           # Documentation (this file)
│
└── .env                # Environment configuration file
```

---

## Project Motivation
Chat-Bot-API was developed to address the need for a flexible, scalable, and open-source chatbot service. By integrating RAG and open AI models, it provides users with a robust system for interacting with documents and conversational models. It aims to democratize AI technology by offering free-to-use models and enabling collaboration in the open-source community.

---

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make changes and commit:
   ```bash
   git commit -m "Added a new feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request to the `main` branch.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contacts

If you have any questions or suggestions, please contact:
- Email: uznetdev@gmail.com
- GitHub Issues: [Issues section](https://github.com/UznetDev/Diabetes-Prediction/issues)
- GitHub Profile: [UznetDev](https://github.com/UznetDev/)
- Telegram: [UZNet_Dev](https://t.me/UZNet_Dev)
- Linkedin: [Abdurakhmon Niyozaliev](https://www.linkedin.com/in/uznetdev/)


### <i>Thank you for your interest in the project!</i>
