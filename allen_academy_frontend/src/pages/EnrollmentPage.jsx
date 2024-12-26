import { useEffect, useState } from 'react';
import { studentCourseAPI, enrollSubjectBlockAPI } from '../components/constants';
import NavBar from '../components/NavBar';
import LoggedInAs from '../components/LoggedInAs';
import EnrollmentFormOptions from '../components/EnrollmentFormOptions';
import Cookies from 'js-cookie';

function EnrollmentPage() {
  const [courseData, setCourseData] = useState(null);
  const [enrollmentError, setEnrollmentError] = useState(null);
  const [enrollmentSuccess, setEnrollmentSuccess] = useState(false);
  const [selectedBlockId, setSelectedBlockId] = useState('');
  const [selectedCourseId, setSelectedCourseId] = useState('');
  const accessToken = Cookies.get('accessToken');
  const accountType = Cookies.get('accountType');

  async function fetchCourse(formData) {
    try {
      const response = await fetch(studentCourseAPI, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json();

      if (data) {
        setCourseData(data.course);
      }
    } catch (error) {
      console.error('Error', error)
    }
  }

  const formData = new FormData();
  formData.append('token', accessToken);

  useEffect(() => { fetchCourse(formData) });

  const handleBlockSelect = (blockId) => {
    setSelectedBlockId(blockId);
  }

  const handleCourseSelect = (courseId) => {
    setSelectedCourseId(courseId);
  }

  const handleFormSubmit = async (e) => {
    e.preventDefault();

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
            <EnrollmentFormOptions accounttype={accountType} course={courseData} onBlockSelect={handleBlockSelect} onCourseSelect={handleCourseSelect} />
          </div>
        </form>
      </div>
    </>
  )
}

export default EnrollmentPage;