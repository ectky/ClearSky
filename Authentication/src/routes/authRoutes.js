const express = require('express');
const { loginUser } = require('../api/controllers/authController');
const router = express.Router();

router.post('/login', loginUser);

module.exports = router;