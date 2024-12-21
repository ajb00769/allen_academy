import { useEffect, useState } from 'react';
import { studentCourseAPI } from './constants';
import LoggedInAs from './LoggedInAs';
import Cookies from 'js-cookie';

function Banner() {
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [isEmployee, setIsEmployee] = useState(false);
  const [collegeName, setCollegeName] = useState('');
  const [courseName, setCourseName] = useState('');
  const [bannerError, setBannerError] = useState(null);
  const loginTicker = <LoggedInAs />;
  const accessToken = Cookies.get('accessToken');
  const formData = new FormData();
  formData.append('token', accessToken);

  useEffect(() => {
    async function fetchCourseData() {
      try {
        const response = await fetch(studentCourseAPI, {
          'method': 'POST',
          'body': formData,
        })

        const data = await response.json();

        if (data.course) {
          setIsEnrolled(true);
          setCourseName(data.course);
          setCollegeName(data.college);
        } else if (Cookies.get('accountType') == "EMP") {
          setIsEmployee(true);
        } else if (data.warning) {
          setIsEnrolled(false);
          setBannerError(data.warning);
        } else if (data.error) {
          setBannerError(data.error);
        }
      } catch {
        console.error('Unexpected error: ', error);
        setBannerError('An unexpected error occured');
      }
    }

    fetchCourseData();
  }, []);

  if (isEnrolled) {
    return (
      <>
        {loginTicker}
        <div className="text-center">
          <p className="h2">Welcome to the college of {collegeName}</p>
          <p className="h3">You are enrolled in the {courseName} course.</p>
        </div>
      </>
    )
  } else if (isEmployee) {
    return (<>
      {loginTicker}
      <div className="text-center">
        <p className="h3">Welcome Employee {Cookies.get('userId')}</p>
      </div>
    </>
    )
  } else if (bannerError) {
    return (
      <>
        {loginTicker}
        <div className="text-center">
          <p className="h3">You aren't enrolled to any courses.</p>
          <p className="h6">Click <a href="/enrollment">here</a> to enroll.</p>
        </div>
      </>
    )
  } else {
    return (
      <>
        <div className="text-center">
          <p className="h2 text-danger">An error occured: {bannerError}</p>
        </div>
      </>
    )
  }
}

export default Banner