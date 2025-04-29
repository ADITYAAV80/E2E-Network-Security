/* eslint-disable */
import { useEffect, useState } from 'react'
import { jwtDecode } from 'jwt-decode'
import { Container, Card, Form, Button, Row, Col } from 'react-bootstrap'
import LogoutButton from './LogoutButton'

function CustomerDashboard() {
  const [username, setUsername] = useState('')
  const [predictionResult, setPredictionResult] = useState(null)
  const [loading, setLoading] = useState(false)


  useEffect(() => {
    const token = localStorage.getItem('authToken')
    if (token) {
      const decoded = jwtDecode(token)
      const email = decoded.sub
      const nameOnly = email.split('@')[0]
      setUsername(nameOnly)
    }
  }, [])

  const handleSubmit = (e) => {
  e.preventDefault()
  const formData = new FormData(e.target)

  setLoading(true)
  setPredictionResult(null)

  fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData,
  })
    .then(res => res.json())
    .then(data => {
      setPredictionResult(data.prediction)
    })
    .catch(err => console.error('Prediction failed:', err))
    .finally(() => setLoading(false))
  }


  return (
    <div style={{
      background: 'linear-gradient(to right, #74ebd5, #acb6e5)',
      minHeight: '100vh',
      padding: '30px',
      width: '100vw',
    }}>
      <LogoutButton />
      <Container>
        
        <Card className="text-center mb-4 p-4 rounded-4 shadow">
          <h1>Welcome, {username}!</h1>
          <p className="lead">We're glad to have you on board 🚀</p>
        </Card>

        <Card className="p-4 rounded-4 shadow">
          <h3 className="mb-4">Enter Features for Phishing URL Detection</h3>
          <Form onSubmit={handleSubmit}>
            <Row>
              {[
                'NumDots', 'SubdomainLevel', 'PathLevel', 'UrlLength', 'NumDash', 'NumDashInHostname', 'AtSymbol',
                'TildeSymbol', 'NumUnderscore', 'NumPercent', 'NumQueryComponents', 'NumAmpersand', 'NumHash',
                'NumNumericChars', 'NoHttps', 'RandomString', 'IpAddress', 'DomainInSubdomains', 'DomainInPaths',
                'HttpsInHostname', 'HostnameLength', 'PathLength', 'QueryLength', 'DoubleSlashInPath',
                'NumSensitiveWords', 'EmbeddedBrandName', 'PctExtHyperlinks', 'PctExtResourceUrls', 'ExtFavicon',
                'InsecureForms', 'RelativeFormAction', 'ExtFormAction', 'AbnormalFormAction',
                'PctNullSelfRedirectHyperlinks', 'FrequentDomainNameMismatch', 'FakeLinkInStatusBar',
                'RightClickDisabled', 'PopUpWindow', 'SubmitInfoToEmail', 'IframeOrFrame', 'MissingTitle',
                'ImagesOnlyInForm', 'SubdomainLevelRT', 'UrlLengthRT', 'PctExtResourceUrlsRT',
                'AbnormalExtFormActionR', 'ExtMetaScriptLinkRT', 'PctExtNullSelfRedirectHyperlinksRT'
              ].map((name, i) => (
                <Col md={6} key={i} className="mb-3">
                  <Form.Group controlId={name}>
                    <Form.Label>{name.replace(/([A-Z])/g, ' $1')}:</Form.Label>
                    <Form.Control type="number" step="any" name={name} defaultValue="0.0" required />
                  </Form.Group>
                </Col>
              ))}
            </Row>
            <Button variant="success" type="submit" className="mt-3 w-100" disabled={loading}>
                {loading ? (
                  <span>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Predicting...
                  </span>
                ) : (
                  'Predict'
                )}
            </Button>
          </Form>
          {predictionResult !== null && (
            <div className="mt-4 text-center">
              {predictionResult === 0 ? (
                <h4 style={{ color: 'green' }}> The website is legitimate</h4>
              ) : (
                <h4 style={{ color: 'red' }}> The website is phishing </h4>
              )}
            </div>
          )}
        </Card>
      </Container>
    </div>
  )
}

export default CustomerDashboard
