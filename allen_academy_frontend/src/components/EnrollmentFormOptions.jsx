import { useEffect, useState } from 'react';
import { getCollegeListAPI, getCourseListAPI, getSubjectListAPI, getBlockListAPI } from './constants';
import Cookies from 'js-cookie';

async function fetchCollegeList() {
  try {
    const response = await fetch(getCollegeListAPI, {
      method: 'GET',
    });
    const data = await response.json();
    return data.departments;
  } catch (error) {
    console.error(error);
    return [];
  }
}

function EnrollmentFormOptions(props) {
  // user selections
  const [selectedCollege, setSelectedCollege] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedBlock, setSelectedBlock] = useState('');
  // options fetched from db
  const [collegeOptions, setCollegeOptions] = useState([]);
  const [courseOptions, setCourseOptions] = useState([]);
  const [subjectOptions, setSubjectOptions] = useState([]);
  const [blockOptions, setBlockOptions] = useState([]);
  // cookies
  const [accessToken, setAccessToken] = useState(Cookies.get('accessToken'));
  const [refreshToken, setRefreshToken] = useState(Cookies.get('refreshToken'));

  useEffect(() => {
    let isMounted = true;
    fetchCollegeList()
      .then(data => {
        if (isMounted) {
          setCollegeOptions(data);
        }
      })
      .catch(error => console.error('Error fetching college list:', error));

    return () => {
      isMounted = false;
    };
  }, []);

  const handleEnrollmentChange = (event) => {
    const selectId = event.target.id;

    switch (selectId) {
      case "college":
        setSelectedCollege(event.target.value);
        let isMounted = true;

        const formData = new FormData();
        formData.append("token", accessToken);
        formData.append("dept_id", selectedCollege);

        async function fetchCourseOptions() {
          try {
            const response = await fetch(getCourseListAPI, {
              method: 'POST',
              body: formData,
            });
            const data = response.json();
            if (isMounted) {
              setCourseOptions(data.courses);
            }
          } catch (error) {
            console.error(error);
          }

          return () => {
            isMounted = false;
          }
        }

        fetchCourseOptions();

        break;
      case "course":
        setSelectedCourse(event.target.value);
        break;
      case "subject":
        setSelectedSubject(event.target.value);
        break;
      case "block":
        setSelectedBlock(event.target.value);
        break;
      default:
        break;
    }
  }

  if (collegeOptions == undefined) {
    return (
      <>
        <div className='h3 text-center text-danger'>No Colleges or Departments have been created yet by the administrator.</div>
        <div className='h5 text-center text-danger'>Please contact the site admin for assistance.</div>
      </>
    )
  } else if (props.accounttype == 'EMP') {
    return (
      <>
        <div className="container-fluid d-grid gap-1 text-center">
          College:
          <select value={selectedCollege} onChange={handleEnrollmentChange} id="college" className="mb-2">
            <option value="" disabled>Select an option</option>
            {
              Object.entries(collegeOptions).map(([, value], key) => (
                <option key={key} value={Object.keys(value)}>
                  {value[Object.keys(value)]}
                </option>
              ))
            }
          </select>
          Course:
          <select value={selectedCourse} onChange={handleEnrollmentChange} id="course" className="mb-2">
            <option value="" disabled>Select an option</option>
            {
              Object.entries(courseOptions).map(([, value], key) => (
                <option key={key} value={Object.keys(value)}>
                  {value[Object.keys(value)]}
                </option>
              ))
            }
          </select>
          Subject:
          <select value={selectedSubject} id="subject" className="mb-2">
            <option value="" disabled>Select an option</option>
          </select>
          Block:
          <select value={selectedBlock} id="block" className="mb-2">
            <option value="" disabled >Select an option</option>
          </select>
        </div>
        <div>
          <button type="submit" className="btn btn-outline-primary" id="enrollment-submit-btn">Submit</button>
        </div>
      </>
    )
  } else if (props.accounttype == 'STU') {
    return (
      <>
        <div>
          Subject:
          <select value={selectedSubject} id="subject">
            <option value="" disabled>Select an option</option>
          </select>
        </div>
        <div>
          Block:
          <select value={selectedBlock} id="block">
            <option value="" disabled>Select an option</option>
          </select>
        </div>
        <div>
          <button type="submit" className="btn btn-outline-primary" id="enrollment-submit-btn">Submit</button>
        </div>
      </>
    )
  }
}

export default EnrollmentFormOptions