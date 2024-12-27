import { useEffect, useState } from 'react';
import { fetchCourseData } from '../common/common'
import { jwtDecode } from 'jwt-decode';
import LoggedInAs from './LoggedInAs';
import Cookies from 'js-cookie';

function Banner() {
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [isEmployee, setIsEmployee] = useState(false);
  const [collegeName, setCollegeName] = useState('');
  const [courseName, setCourseName] = useState('');
  const [bannerError, setBannerError] = useState(null);
  const decoded = jwtDecode(Cookies.get('accessToken'));
  const accountType = decoded.account_type;
  const loginTicker = <LoggedInAs userId={decoded.user_id} />;
  const accessToken = Cookies.get('accessToken');
  const [courseData, setCourseData] = useState([]);
  const formData = new FormData();
  formData.append('token', accessToken);

  useEffect(() => {
    const fetchedData = fetchCourseData(formData);
    setCourseData(fetchedData);

    if (courseData.course && window.location.pathname == "/home") {
      setIsEnrolled(true);
      setCourseName(courseData.course);
      setCollegeName(courseData.college);
    } else if (courseData.course && accountType == "STU") {
      return (courseData.course);
    } else if (accountType == "EMP") {
      setIsEmployee(true);
    } else if (courseData.warning) {
      setIsEnrolled(false);
      setBannerError(courseData.warning);
      return courseData.warning;
    } else if (courseData.error) {
      setBannerError(courseData.error);
    } else {
      setBannerError('An unexpected error occured');
    }
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