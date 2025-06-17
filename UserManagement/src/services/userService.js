const User = require('../models/user'); 
const hashPassword = require('../utils/hashPasswordFunction');

const createUser = async (userData) => {
  try {
    // Encrypt the password before saving
    // Assuming userData contains {name, email, password, userType, studentId}
    const hashedPassword = await hashPassword(userData.password);
    const newUser = await User.create({
      ...userData,
      password: hashedPassword,
    });
    return newUser;
  } catch (error) {
    throw error; 
  }
};

const getUserById = async (userId) => {
  const user = await User.findByPk(userId);
  return user;
};

const updateUser = async (userId, updates) => {
    try {
      const user = await User.findByPk(userId);
      if (!user) {
        throw new Error('User not found');
      }
      
      const hashedPassword = await hashPassword(userData.password);
  
      const updatedUser = await user.update({
        ...updates,
        password: hashedPassword,
      });
      return updatedUser;
    } catch (error) {
      throw error;
    }
  };

  const deleteUser = async (userId) => {
    try {
      const user = await User.findByPk(userId);
      if (!user) {
        throw new Error('User not found');
      }
      
      await user.destroy();
      return { message: "User deleted successfully" };
    } catch (error) {
      throw error;
    }
  };

  const listUsers = async () => {
    try {
      const users = await User.findAll();
      return users;
    } catch (error) {
      throw error;
    }
  };


const verifyCredentials =  async (email, password) => {
    try {
      const user = await User.findOne({ where: { email } });

      if (!user) {
        // User not found
        return { error: true, statusCode: 404, message: 'User not found' };
      }
  
      // Compare the provided password with the stored hash
      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        // Passwords do not match
        return { error: true, statusCode: 401, message: 'Invalid credentials' };
      }

      // Credentials are valid
      return { 
        error: false, 
        user: { 
          id: user.id, 
          email: user.email, 
          userType: user.userType 
        } 
      };
    } catch (error) {
      console.error(error);
      return { error: true, statusCode: 500, message: 'An error occurred while verifying credentials' };
    }
  };

module.exports = {
  createUser,
  getUserById,
  updateUser,
  deleteUser,
  listUsers,
  verifyCredentials
};