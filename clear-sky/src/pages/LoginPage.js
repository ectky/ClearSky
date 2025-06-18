import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container } from '@mui/material';

const LoginForm = () => {
  // States for email and password
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Handling form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    // Log or process form submission here
    console.log(`Logging in with email: ${email} and password: ${password}`);
    // Add your login logic or API call here
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