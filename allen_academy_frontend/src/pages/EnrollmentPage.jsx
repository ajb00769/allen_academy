import NavBar from "../components/NavBar";
import LoggedInAs from "../components/LoggedInAs";
import EnrollmentFormOptions from "../components/EnrollmentFormOptions";
import Cookies from 'js-cookie';

function EnrollmentPage(props) {
  return (
    <>
      <NavBar />
      <LoggedInAs />
      <div>
        <h2 className="text-center mt-2">Enrollment</h2>
        <form method="POST" id="enrollment-form">
          <div className="d-grid gap-2">
            <EnrollmentFormOptions accounttype={Cookies.get('accountType')} college={props.college} />
            <button type="submit" className="btn btn-outline-success">Submit</button>
          </div>
        </form>
      </div>
    </>
  )
}

export default EnrollmentPage;