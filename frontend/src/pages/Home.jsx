import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Container, Row, Col, Card } from 'react-bootstrap';

function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      if (decodedToken.role === 'developer') {
        navigate('/developer');
      } else if (decodedToken.role === 'customer') {
        navigate('/customer');
      }
    }
  }, [navigate]);

  return (
     <div
      style={{
        backgroundImage: "url('https://images.unsplash.com/photo-1597733336794-12d05021d510?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
        width: '100vw',
      }}
    >
    <div
      style={{
        display:'flex',
        justifyContent: 'center',
        height: '100vh',
        width: '100vw',
      }}
    >
      <Container fluid className="d-flex justify-content-center align-items-center">
        <Row className="w-100 justify-content-center">
          <Col xs={12} sm={8} md={6} lg={4}>
            <Card className="p-4" style={{ opacity: 0.9 }}>
              <h1 className="text-center">Welcome to the Network Security App</h1>
              <div className="d-flex justify-content-center mt-4">
                <Button
                  variant="primary"
                  onClick={() => navigate('/login')}
                  className="mx-2"
                  style={{ width: '120px' }}
                >
                  Login
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => navigate('/signup')}
                  className="mx-2"
                  style={{ width: '120px' }}
                >
                  Sign Up
                </Button>
              </div>
            </Card>
          </Col>
        </Row>
      </Container>
      </div>
    </div>
  );
}

export default Home;