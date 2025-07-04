require('dotenv').config();
const express = require('express');
const cors = require('cors');
const userRoutes = require('./src/routes/authRoutes');  

const app = express();
app.use(express.json());  // For parsing application/json

app.use(cors());
// Use the user routes
app.use(userRoutes);

const port = 8001;
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));