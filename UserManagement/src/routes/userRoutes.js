const express = require('express');
const router = express.Router();
const { createUser, listUsers, deleteUser, getUserById, verifyCredentials } = require('../services/userService'); 

// POST /users to create a new user
router.post('/users', async (req, res) => {
  try {
    const user = await createUser(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ message: error.message });  // Simplified error handling
  }
});

// GET /users to list user
router.get('/users', async (req, res) => {
  try {
    const users = await listUsers();
    res.status(201).json(users);
  } catch (error) {
    res.status(400).json({ message: error.message });  // Simplified error handling
  }
});

// GET to get a user by id
router.get('/users/:userId', async (req, res) => {
    try {
      // Accessing userId from the URL parameter
      const { userId } = req.params;
      const result = await getUserById(userId); 
  
      res.status(200).json(result);
    } catch (error) {
      res.status(400).json({ message: error.message });
    }
  });


// Delete /users to delete a user
router.delete('/users/:userId', async (req, res) => {
    try {
      // Accessing userId from the URL parameter
      const { userId } = req.params;
      const result = await deleteUser(userId); 
  
      res.status(200).json(result);
    } catch (error) {
      res.status(400).json({ message: error.message });
    }
  });

// PATCH /users to update a user
router.patch('/users/:userId', async (req, res) => {
    const { userId } = req.params;
    const updates = req.body; // Contains the fields to be updated
  
    try {
      const updatedUser = await updateUser(userId, updates);
      if (!updatedUser) {
        return res.status(404).json({ message: "User not found" });
      }
      
      res.status(200).json(updatedUser);
    } catch (error) {
      res.status(400).json({ message: error.message });  
    }
  });

  // Endpoint to verify user credentials
  router.post('/verify-credentials', async (req, res) => {
    const { email, password } = req.body;
  
    const result = await verifyCredentials(email, password);
    
    if (result.error) {
      return res.status(result.statusCode).json({ message: result.message });
    }
    
    // Credentials are valid
    res.status(200).json({
      message: 'Credentials verified successfully',
      user: result.user
    });
  });


module.exports = router;