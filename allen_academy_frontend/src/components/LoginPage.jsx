import { useState } from 'react';
import { loginAPI } from './constants';
import Dashboard from './Dashboard';

function LoginPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginError, setLoginError] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedInUsername, setLoggedInUsername] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [refreshToken, setRefreshToken] = useState('');

  const handleLogin = (e) => {
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
        console.log(data.access); // for debug remove in prod
        setRefreshToken(data.refresh);
      } else if (data.error || data.detail) {
        setLoginError(data.error || data.detail);
      }
    }).catch(error => {
      console.error('Unexpected error: ', error);
      setLoginError('An unexpected error occured.');
    })
  }

  if (isLoggedIn) {
    return (
      <>
        <Dashboard username={loggedInUsername} access={accessToken} refresh={refreshToken} />
      </>
    )
  } else {
    return (
      <>
        <div className="">
          <h2 className="">Login to Allen Academy</h2>
          <form method="POST" onSubmit={handleLogin} id="login-form">
            <div className="d-grid gap-2">
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
  }
}

export default LoginPage;