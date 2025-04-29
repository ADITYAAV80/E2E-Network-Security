import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, Form, Container, Row, Col, Card } from 'react-bootstrap';

function Signup() {
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/signup', {
        email,
        password,
        role: 'customer', // Ensure role is always 'customer' on signup
      });

      // Redirect to customer dashboard after signup
      if (response.data.success) {
        localStorage.setItem('authToken', response.data.token);
        navigate('/customer');
      }
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError('User already exists. Please try a different email.');
      } else {
        setError('An error occurred during signup. Please try again.');
      }
    }
  };

  return (
    <div 
      style={{
        backgroundImage: "url('https://images.unsplash.com/photo-1597733336794-12d05021d510?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
        width: '100vw',
    }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          height: '100vh',
          width: '100vw',
        }}
      >
        <Container fluid className="d-flex justify-content-center align-items-center">
          <Row className="justify-content-center">
  
              <Card className="p-5 rounded-4" style={{ opacity: 0.9 }}>
                <h2 className="text-center mb-4">Sign Up</h2>
                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control 
                      type="email" 
                      placeholder="Enter your email" 
                      value={email} 
                      onChange={(e) => setEmail(e.target.value)} 
                      required 
                    />
                  </Form.Group>
                  <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                      type="password" 
                      placeholder="Enter your password" 
                      value={password} 
                      onChange={(e) => setPassword(e.target.value)} 
                      required 
                    />
                  </Form.Group>
                  {error && <p style={{ color: 'red' }}>{error}</p>}
                  <Button variant="primary" type="submit" className="w-100">
                    Sign Up
                  </Button>
                </Form>
              </Card>
          </Row>
        </Container>
      </div>
    </div>
  );
}

export default Signup;
