import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'


function LoginPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginError, setLoginError] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedInUsername, setLoggedInUsername] = useState('');
  const loginAPI = "http://localhost:8080/api/login/"
  const [accessToken, setAccessToken] = useState('');
  const [refreshToken, setRefreshToken] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    formData.append('username', username);
    formData.append('password', password);

    fetch(loginAPI, {
      method: 'POST',
      body: formData,
    }).then((response) => {
      return response.json();
    }).then((data) => {
      if (data.access) {
        setUsername('');
        setPassword('');
        setLoggedInUsername(data.user);
        setLoginError(null);
        setIsLoggedIn(true);
        setAccessToken(data.access);
        setRefreshToken(data.refresh);
      } else if (data.error || data.detail) {
        setLoginError(data.error || data.detail);
      }
    }).catch(error => {
      console.error('Unexpected error: ', error);
      setLoginError('An unexpected error occured.');
    })
  }
  return (
    isLoggedIn ? (
      <Dashboard username={loggedInUsername} access={accessToken} refresh={refreshToken} />
    ) : (
      <>
        <div className="card">
          <h2 className="card-title">Login to Allen Academy</h2>
          <form method="POST" onSubmit={handleSubmit} id="login-form">
            <div className="card-body d-grid gap-2">
              <div>
                <input
                  type="text"
                  className="form-control text-center"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <input
                type="password"
                className="form-control text-center"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button type="submit" className="btn btn-outline-primary">Login</button>
            </div>
            <div>
              {loginError && <p className="alert alert-danger">{loginError}</p>}
            </div>
          </form>
          <div>
            <p>Don't have an account? Click <a href="#">here</a> to register.</p>
          </div>
        </div>
      </>
    )
  )
}

function Dashboard(props) {
  return (
    <>
      <nav className="navbar navbar-expand-lg bg-body-secondary fixed-top">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">Allen Academy</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <a className="nav-link active" aria-current="page" href="#">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link disabled" aria-disabled="true">Enrollment</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">Schedule</a>
              </li>
              <li className="nav-item">
                <a className="nav-link text-danger" href="#">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <div>
        Welcome {props.username}
      </div>
    </>
  )
}

function App() {
  return (
    <>
      <LoginPage />
    </>
  )
}

export default App