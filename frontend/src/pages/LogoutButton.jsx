/* eslint-disable */
import { Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

function LogoutButton() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('authToken')
    navigate('/login')
  }

  return (
    <div className="text-end mb-3">
      <Button variant="danger" onClick={handleLogout}>
        Logout
      </Button>
    </div>
  )
}

export default LogoutButton
