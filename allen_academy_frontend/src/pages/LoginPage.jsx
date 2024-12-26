import { useState } from 'react';
import { loginAPI } from '../components/constants';
import Cookies from 'js-cookie';

function LoginPage() {
  const [loginError, setLoginError] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

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
        setLoginError(null);
        Cookies.set('accessToken', data.access, { expires: 7, secure: true, sameSite: 'strict' });
        Cookies.set('refreshToken', data.refresh, { expires: 30, secure: true, sameSite: 'strict' });
        Cookies.set('userId', data.user, { secure: true, sameSite: 'strict' });
        Cookies.set('accountType', data.type, { secure: true, sameSite: 'strict' });
      } else if (data.error || data.detail) {
        setLoginError(data.error || data.detail);
      }
    }).catch(error => {
      console.error('Unexpected error: ', error);
      setLoginError('An unexpected error occured.');
    })
  }

  if (Cookies.get('accessToken')) {
    window.location.pathname = '/home';
  } else {
    return (
      <>
        <div>
          <h2 className='text-center mt-3'>Login to Allen Academy</h2>
          <div className='card card-body mx-auto my-5 w-75 card-max-width'>
            <form method='POST' onSubmit={handleLogin} id='login-form'>
              <div className='d-grid gap-2'>
                <input
                  type='text'
                  className='form-control text-center'
                  placeholder='Username'
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <input
                  type='password'
                  className='form-control text-center'
                  placeholder='Password'
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <div className='mx-auto'>
                  <button type='submit' className='btn btn-outline-primary'>Login</button>
                </div>
              </div>
              <div>
                {loginError && <p className='alert alert-danger'>{loginError}</p>}
              </div>
            </form>
            <div>
              <p>Don't have an account? Click <a href='#'>here</a> to register.</p>
            </div>
          </div>
        </div>
      </>
    )
  }
}

export default LoginPage;