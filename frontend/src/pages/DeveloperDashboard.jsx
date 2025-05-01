import { useEffect, useState } from 'react'
import { jwtDecode } from 'jwt-decode'
import { Container, Card, Button, Spinner, Alert } from 'react-bootstrap'
import LogoutButton from './LogoutButton'
import { appConfig } from '../config/appConfig';

function DeveloperDashboard() {
  const [username, setUsername] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('authToken')
    if (token) {
      const decoded = jwtDecode(token)
      const email = decoded.sub
      const nameOnly = email.split('@')[0]
      setUsername(nameOnly)
    }
  }, [])

  const handleTrain = () => {

    setLoading(true)
    setMessage(null)

    const token = localStorage.getItem("authToken")

    fetch(`${appConfig.backendURL}/train`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => res.text())
      .then(data => {
        if (data.includes("Training started")) {
          setMessage("Training has started. You'll get an email once it's done.")
        } else {
          setMessage("Unexpected response from server.")
        }
      })
      .catch(err => {
        console.error('Training failed:', err)
        setMessage("Training failed. Check backend logs.")
      })
      .finally(() => setLoading(false))
}


  const getAlertVariant = () => {
    if (!message) return 'info'
    if (message.toLowerCase().includes("success")) return 'success'
    if (message.toLowerCase().includes("fail")) return 'danger'
    if (message.toLowerCase().includes("cancel")) return 'warning'
    return 'info'
  }

  return (
    <div style={{
      backgroundImage: 'url("https://images.unsplash.com/photo-1604964432806-254d07c11f32?q=80&w=1160&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      minHeight: '100vh',
      padding: '30px',
      width: '100vw',
      backdropFilter: 'blur(3px)',
    }}>
      <LogoutButton />
      <Container>
        <Card className="text-center mb-4 p-4 rounded-4 shadow bg-light bg-opacity-75">
          <h1>Welcome, {username} (Developer)!</h1>
          <p className="lead">Manage and monitor model training here</p>
        </Card>

        <Card className="text-center p-4 rounded-4 shadow bg-light bg-opacity-75">
          <h3 className="mb-4">Trigger Training Pipeline</h3>
          <div className="d-flex justify-content-center">
            <Button variant="success" onClick={handleTrain} disabled={loading}>
              {loading ? (
                <>
                  <Spinner animation="border" size="sm" className="me-2" />
                  Training...
                </>
              ) : (
                'Train Pipeline'
              )}
            </Button>
          </div>

          {message && (
            <Alert variant={getAlertVariant()} className="mt-4">
              {message}
            </Alert>
          )}
        </Card>
      </Container>
    </div>
  )
}

export default DeveloperDashboard
