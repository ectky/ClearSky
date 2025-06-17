require('dotenv').config(); // Loading environment variables from .env file
const express = require('express');
const authRoutes = require('./src/routes/authRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(authRoutes);

app.listen(PORT, () => console.log(`Auth Service running on port ${PORT}`));