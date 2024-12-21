import Cookies from 'js-cookie';

function LoggedInAs() {
  return (
    <>
      <div className="d-flex justify-content-end me-2">
        <p><small>Logged in as <a href="#">{Cookies.get('userId')}</a></small></p>
      </div>
    </>
  )
}

export default LoggedInAs