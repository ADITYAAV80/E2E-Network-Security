/* eslint-disable */
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Button, Form, Container, Row, Col, Card } from 'react-bootstrap'
import { appConfig } from '../config/appConfig';


function Login() {
    
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('');
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()

    try {
      // Send login request to FastAPI
      console.log("Calling backend at:", appConfig.backendURL);
      const res = await axios.post(`${appConfig.backendURL}/login`, { email, password })
      
      // Extract the token from the response
      const { access_token } = res.data
      localStorage.setItem('authToken', access_token)  // Store JWT in localStorage

      // Decode JWT to check role
      const decodedToken = JSON.parse(atob(access_token.split('.')[1]))
      const role = decodedToken.role

      if (role === 'developer') navigate('/developer')
      else if (role === 'customer') navigate('/customer')

    } catch (err) {

      if (err.response && err.response.status === 401) {
        setError('Wrong Credentials.');
      } else {
        setError('An error occurred during login. Please try after sometime.');
      }
      
    }
  }

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
        display:'flex',
        justifyContent: 'center',
        height: '100vh',
        width: '100vw',
      }}
    >
      <Container fluid className="d-flex justify-content-center align-items-center">
        <Row className="justify-content-center">
          <Col xs={12} sm={8} md={6} lg={4}></Col>
          <Card className="p-5 rounded-4" style={{ opacity: 0.9 }}>
            <h2 className="text-center mb-4">Login</h2>
            <Form onSubmit={handleLogin}>
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
                Login
              </Button>
            </Form>
        </Card>
        </Row>
      </Container>
      </div>
    </div>
  )
}

export default Login
