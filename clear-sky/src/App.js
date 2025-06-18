import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { createTheme, ThemeProvider, CssBaseline } from '@mui/material';
import logo from './logo.svg';
import './App.css';
// Import the LoginPage component
import LoginPage from './pages/LoginPage'; 
import RegisterPage from './pages/RegisterPage'; 
// Create a theme instance and set the text primary color to white
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    background: {
      default: '#121212',
    },
    text: {
      primary: '#ffffff',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
    <Router>
      <div className="App">
        <header className="App-header">
          {/* Using Link component for navigation */}
          <nav>
            <Link to="/" className="App-link">Home</Link> |{" "}
            <Link to="/login" className="App-link">Login</Link> |{" "}
            <Link to="/register" className="App-link">Register</Link>
          </nav>

          {/* Routes component looks through its children Routes and
              renders the first one that matches the current URL. */}
          <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={
          <div>
            <p>Edit <code>src/App.js</code> and save to reload.</p>
            <a
              className="App-link"
              href="https://reactjs.org"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn React
            </a>
          </div>
        } />
          </Routes>
        </header>
      </div>
    </Router>
    </ThemeProvider>
  );
}

export default App;