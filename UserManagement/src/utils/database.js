const { Sequelize } = require('sequelize');

// Alternative approach: breaking the connection string into parameters
const sequelize = new Sequelize('clear-sky-users', 'postgres', 'root', {
  host: 'localhost',
  dialect: 'postgres',
  port: 5432,
  logging: false, 
});

// Test the connection
async function testDatabaseConnection() {
  try {
    await sequelize.authenticate();
    console.log('Connection to the database has been established successfully.');
  } catch (error) {
    console.error('Unable to connect to the database:', error);
  }
}

testDatabaseConnection();

module.exports = sequelize;