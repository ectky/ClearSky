require('dotenv').config();
const { Sequelize } = require('sequelize');
const express = require('express');
const userRoutes = require('./src/routes/userRoutes');  // Adjust the path as needed

const app = express();
app.use(express.json());  // For parsing application/json

const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    dialect: 'postgres'
  }
);

sequelize.authenticate()
  .then(() => console.log('Database connected!'))
  .catch(err => console.error('Unable to connect to the database:', err));

// Add a root route for health check or friendly message
app.get('/', (req, res) => {
  res.send('UserManagement service is running!');
});

// Use the user routes
app.use(userRoutes);

const port = 3000;
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));