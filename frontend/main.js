const tokenData = JSON.parse(localStorage.getItem('access_token')).token;

const API_BASE = 'http://chatbot.codernet.uz';


async function checkToken(token) {
    try {
        // Make the POST request to the login_with_token endpoint
        const response = await fetch(`${API_BASE}/auth/login_with_token`, {
            method: 'POST', // HTTP method
            headers: {
                'Content-Type': 'application/json', // Indicating JSON format
            },
            body: JSON.stringify({ "token": "htefdnb" }), // Send token in the request body
        });

        // Handle response
        if (response.ok) {
            const data = await response.json();
            console.log('Token is valid:', data); // Log the user's info
            return {
                success: true,
                data,
            };
        } else {
            const errorData = await response.json();
            console.log('Invalid token:', errorData.detail); // Log error details
            return {
                success: false,
                message: errorData.detail || 'Invalid token',
            };
        }
    } catch (error) {
        console.log('Error while checking the token:', error); // Handle network or runtime errors
        return {
            success: false,
            message: 'An error occurred while checking the token.',
        };
    }
}


checkToken(tokenData).then((result) => {
    if (result.success) {
        // Token is valid
        console.log('User Info:', result.data);
    } else {
        // Token is invalid or an error occurred
        console.log('Error:', result.message);
    }
});
console.log(tokenData);
