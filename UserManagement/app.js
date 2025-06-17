const express = require('express');
const userRoutes = require('./src/routes/userRoutes');  // Adjust the path as needed

const app = express();
app.use(express.json());  // For parsing application/json

// Use the user routes
app.use(userRoutes);

const port = 3000;
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));