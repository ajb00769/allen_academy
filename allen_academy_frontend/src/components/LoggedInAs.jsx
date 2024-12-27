function LoggedInAs(props) {
  return (
    <>
      <div className="d-flex justify-content-end me-2">
        <p><small>Logged in as <a href="#">{props.userId}</a></small></p>
      </div>
    </>
  )
}

export default LoggedInAs