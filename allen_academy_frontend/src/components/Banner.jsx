import { useState } from 'react';
import { studentCourseAPI } from './constants';
import LoggedInAs from './LoggedInAs';

function Banner(props) {
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [isEmployee, setIsEmployee] = useState(false);
  const [collegeName, setCollegeName] = useState('');
  const [courseName, setCourseName] = useState('');
  const [bannerError, setBannerError] = useState(null);
  const loginTicker = <LoggedInAs username={props.username} />;
  const formData = new FormData();
  formData.append('token', props.access);

  fetch(studentCourseAPI, {
    method: 'POST',
    body: formData,
  }).then((response) => {
    return response.json();
  }).then((data) => {
    if (data.course) {
      setIsEnrolled(true);
      setCourseName(data.course);
      setCollegeName(data.college);
    }
    else if (data.account_type == "EMP") {
      setIsEmployee(true);
      console.log(data.account_type)
    } else if (data.warning) {
      setIsEnrolled(false);
      setBannerError(data.warning);
    } else if (data.error) {
      setBannerError(data.error);
    }
  }).catch(error => {
    console.error('Unexpected error: ', error);
    setBannerError('An unexpected error occured')
  })

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
        <p className="h3">Welcome Employee {props.username}</p>
      </div>
    </>
    )
  } else if (bannerError) {
    return (
      <>
        {loginTicker}
        <div className="text-center">
          <p className="h3">You aren't enrolled to any courses.</p>
          <p className="h6">Click <a href="#">here</a> to enroll.</p>
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