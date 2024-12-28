import { useEffect, useState } from 'react';
import { studentCourseAPI, enrollSubjectBlockAPI, enrollCourseAPI } from '../components/constants';
import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';
import NavBar from '../components/NavBar';
import LoggedInAs from '../components/LoggedInAs';
import EnrollmentFormOptions from '../components/EnrollmentFormOptions';

function EnrollmentPage() {
  const [courseCode, setCourseCode] = useState(null);
  const [enrollmentError, setEnrollmentError] = useState(null);
  const [enrollmentSuccess, setEnrollmentSuccess] = useState(false);
  const [selectedBlockId, setSelectedBlockId] = useState('');
  const [selectedCourseId, setSelectedCourseId] = useState('');
  const accessToken = Cookies.get('accessToken');
  const decoded = jwtDecode(Cookies.get('accessToken'));
  const accountType = decoded.account_type;

  async function fetchCourse(formData) {
    try {
      const response = await fetch(studentCourseAPI, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json();

      if (data) {
        setCourseCode(data.course_code);
      }
    } catch (error) {
      console.error('Error', error)
    }
  }

  const formData = new FormData();
  formData.append('token', accessToken);

  useEffect(() => { fetchCourse(formData) }, []);

  const handleBlockSelect = (blockId) => {
    setSelectedBlockId(blockId);
  }

  const handleCourseSelect = (courseId) => {
    setSelectedCourseId(courseId);
  }

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    if (accountType != "EMP" && courseCode == null) {
      const formData = new FormData();
      formData.append('course_code', selectedCourseId);
      formData.append('token', accessToken);
      formData.append('account_id', decoded.user_id);

      await fetch(enrollCourseAPI, {
        method: 'POST',
        body: formData,
      }).then((response) => {
        return response.json()
      }).then((data) => {
        console.log(data);
        if (data.success) {
          console.log('Enrollment to course is successful.')
          setEnrollmentSuccess(true);
          setTimeout(() => {
            window.location.pathname = "/home";
          }, 1000);
          return true;
        } else if (data.error) {
          console.log('Enrollment failure.')
          setEnrollmentError(data.error);
        }
      }).catch((error) => {
        setEnrollmentError(error)
        console.error('Error', error);
      })
    } else {
      const formData = new FormData();
      formData.append('block_id', selectedBlockId);
      formData.append('token', accessToken);

      await fetch(enrollSubjectBlockAPI, {
        method: 'POST',
        body: formData,
      }).then((response) => {
        return response.json();
      }).then((data) => {
        console.log(data)
        if (data.success) {
          console.log('Enrollment success.')
          setEnrollmentSuccess(true);
          setTimeout(() => {
            window.location.pathname = "/schedule";
          }, 1000);
          return true;
        } else if (data.error) {
          console.log('Enrollment failure.')
          setEnrollmentError(data.error);
        }
      }).catch((error) => {
        setEnrollmentError(error)
        console.error('Error', error);
      })
    }
  }

  return (
    <>
      <NavBar />
      <LoggedInAs />
      <div>
        <h2 className='text-center mt-2 mb-5'>Enrollment</h2>
        <div className='d-flex justify-content-center'>
          {enrollmentError && (
            <div className='alert alert-danger w-75'>An error occured: {enrollmentError}.</div>
          )}
          {enrollmentSuccess && (
            <div className='alert alert-success w-75'>Successfully enrolled.</div>
          )}
        </div>
        <form method='POST' id='enrollment-form' onSubmit={handleFormSubmit}>
          <div className='container d-grid gap-2 card-max-width'>
            <EnrollmentFormOptions accounttype={accountType} course={courseCode} onBlockSelect={handleBlockSelect} onCourseSelect={handleCourseSelect} />
          </div>
        </form>
      </div>
    </>
  )
}

export default EnrollmentPage;