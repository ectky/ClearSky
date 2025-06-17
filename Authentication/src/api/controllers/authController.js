const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { verifyCredentials } = require('../../services/authService');

const loginUser = async (req, res) => {
  const { email, password } = req.body;

  try {
    const verificationResult = await verifyCredentials(email, password);
    if (!verificationResult.success) {
        // Handle failed verification
        return res.status(401).json({ message: "Authentication failed" });
    }

    const user = verificationResult.data?.user;
    const token = jwt.sign(
      { userId: user.id, email: user.email, userType: user.userType },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );

    res.json({ token });
  } catch (error) {
    res.status(401).json({ message: error.message });
  }
};

module.exports = { loginUser };