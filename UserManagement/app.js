require('dotenv').config();
const { Sequelize } = require('sequelize');
const express = require('express');
const userRoutes = require('./src/routes/userRoutes');  // Adjust the path as needed
const cors = require('cors');
const User = require('./src/models/user');

const app = express();
app.use(express.json());  // For parsing application/json
app.use(cors());
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

sequelize.sync()
  .then(result => {
    console.log('Database synced!')
  })
  .catch(err => {
    console.log(err);
  });

  User.sync({ force: false })  // 'force: true' will drop the table if it already exists
  .then(() => {
    console.log('User table has been successfully created');
  })
  .catch(error => {
    console.error('This error occured', error);
  });

// Add a root route for health check or friendly message
app.get('/', (req, res) => {
  res.send('UserManagement service is running!');
});

// Use the user routes
app.use(userRoutes);

const port = 8002;
app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));