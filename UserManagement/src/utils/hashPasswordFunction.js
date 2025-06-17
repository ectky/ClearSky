const bcrypt = require('bcrypt');

const hashPassword = async (password) => {
    const saltRounds = 10; // Recommended value
    try {
        // Generate a salt and hash on separate function calls
        const hash = await bcrypt.hash(password, saltRounds);
        return hash;
    } catch (error) {
        throw error; 
    }
};

module.exports = hashPassword;