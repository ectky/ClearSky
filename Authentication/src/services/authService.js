const axios = require('axios');
require('dotenv').config();

// Function to call verifyCredentials endpoint:
const verifyCredentials = async (email, password) => {
    const endpoint = `${process.env.USER_MANAGEMENT_SERVICE_BASE_URL}/verify-credentials`;
    try {
        const response = await axios.post(endpoint, {
            email,
            password
        });

        // Successful verification
        return {
            success: true,
            data: response.data // Contains user data or whatever the user management service responds with
        };
    } catch (error) {
        console.error('Error verifying credentials:', error.response?.data);

        // Handle failure (like invalid credentials or service error)
        return {
            success: false,
            error: error.response?.data?.message || "An error occurred while verifying credentials."
        };
    }
};

module.exports = { verifyCredentials };