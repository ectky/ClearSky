import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container } from '@mui/material';

const CreateUserForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userType, setUserType] = useState('');
  const [studentId, setStudentId] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(`Creating user with name: ${name}, email: ${email}, password: ${password}, userType: ${userType}, studentId: ${studentId}`);

    try {
        const response = await fetch('http://localhost:8002/users', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name, email, password, usertype: userType, studentid: studentId })
        });
  
        if (!response.ok) {
          throw new Error('User creation failed');
        }
  
        const data = await response.json();
        console.log(`Created user: ${data}`);
      } catch (error) {
        console.error(`Error: ${error.message}`);
        // Handle the error (e.g., show a message to the user)
      }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
        component="form"
        onSubmit={handleSubmit}
        noValidate
      >
        <Typography component="h1" variant="h5">
          Create User
        </Typography>
        <TextField
          margin="normal"
          required
          fullWidth
          id="name"
          label="Name"
          name="name"
          autoFocus
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          id="email"
          label="Email Address"
          name="email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          name="password"
          label="Password"
          type="password"
          id="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          id="userType"
          label="User Type"
          name="userType"
          value={userType}
          onChange={(e) => setUserType(e.target.value)}
        />
        <TextField
          margin="normal"
          fullWidth
          id="studentId"
          label="Student ID"
          name="studentId"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
        >
          Create User
        </Button>
      </Box>
    </Container>
  );
};

export default CreateUserForm;