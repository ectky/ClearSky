import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container } from '@mui/material';

const LoginForm = () => {
  // States for email and password
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Handling form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(`Logging in with email: ${email} and password: ${password}`);
  
    try {
      const response = await fetch('http://localhost:8001/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
  
      if (!response.ok) {
        throw new Error('Authentication failed');
      }
  
      const data = await response.json();
      const token = data.token;
  
      console.log(`Received token: ${token}`);
      // Store the token in localStorage
      localStorage.setItem('token', token);
  
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
          Sign In
        </Typography>
        <TextField
          margin="normal"
          required
          fullWidth
          id="email"
          label="Email Address"
          name="email"
          autoComplete="email"
          autoFocus
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
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
        >
          Sign In
        </Button>
      </Box>
    </Container>
  );
};

export default LoginForm;