const { DataTypes, Model } = require('sequelize');
const sequelize = require('../utils/database');

class User extends Model {}

User.init({
  // Assuming ID is auto-managed by Sequelize
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  usertype: {
    type: DataTypes.ENUM('InstitutionRepresentative', 'Instructor', 'Student'),
    allowNull: false,
  },
  studentid: {
    type: DataTypes.STRING,
    allowNull: true,
  },
}, {
  sequelize, // The sequelize instance
  modelName: 'user', // Name of the model
  timestamps: false,
});

module.exports = User;