import { useEffect, useState } from 'react';
import { getCollegeListAPI, getCourseListAPI, getSubjectListAPI, getBlockListAPI, getBlockScheduleAPI } from './constants';
import Cookies from 'js-cookie';
import SchedulePreview from './SchedulePreview';

async function fetchCollegeOptions() {
  try {
    const response = await fetch(getCollegeListAPI, {
      method: 'GET',
    });
    const data = await response.json();
    if (data.departments && data.departments.length > 0) {
      return data.departments;
    } else {
      console.warn('No departments fetched.')
    }
  } catch (error) {
    console.error(error);
    return [];
  }
}

async function fetchCourseOptions(formData) {
  try {
    const response = await fetch(getCourseListAPI, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (data.courses && data.courses.length > 0) {
      return data.courses;
    } else {
      console.warn('No courses fetched.');
    }
  } catch (error) {
    console.error(error);
    return [];
  }
}

async function fetchSubjectOptions(formData) {
  try {
    const response = await fetch(getSubjectListAPI, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json()
    if (data.result && data.result.length > 0) {
      return data.result;
    } else {
      console.warn('No subjects fetched.');
    }
  } catch (error) {
    console.error(error);
    return [];
  }
}

async function fetchBlockOptions(formData) {
  try {
    const response = await fetch(getBlockListAPI, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (data.result && data.result.length > 0) {
      return data.result;
    } else {
      console.warn('No blocks fetched.');
    }
  } catch (error) {
    console.error(error);
    return [];
  }
}

async function fetchBlockSchedule(formData) {
  try {
    const response = await fetch(getBlockScheduleAPI, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (data.result && data.result.length > 0) {
      return data.result;
    } else {
      console.warn('No schedules fetched.');
    }
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
  const [blockSchedule, setBlockSchedule] = useState([]);
  // cookies
  const [accessToken, setAccessToken] = useState(Cookies.get('accessToken'));
  const [refreshToken, setRefreshToken] = useState(Cookies.get('refreshToken'));

  useEffect(() => {
    let isMounted = true;
    fetchCollegeOptions()
      .then(data => {
        if (isMounted) {
          setCollegeOptions(data);
        }
      })
      .catch(error => console.error('Error fetching college options:', error));

    return () => {
      isMounted = false;
    };
  }, []);

  const handleCollegeChange = async (event) => {
    setSelectedCollege(event.target.value);

    const formData = new FormData();
    formData.append('dept_id', event.target.value);
    formData.append('token', accessToken);

    try {
      const courseData = await fetchCourseOptions(formData);
      setCourseOptions(courseData);
    } catch (error) {
      console.error('Error fetching course options:', error);
    }
  }

  const handleCourseChange = async (event) => {
    setSelectedCourse(event.target.value);

    const formData = new FormData();
    formData.append('course_id', event.target.value);
    formData.append('token', accessToken);

    try {
      const subjectData = await fetchSubjectOptions(formData);
      setSubjectOptions(subjectData);
    } catch (error) {
      console.error('Error fetching subject options:', error);
    }
  }

  const handleSubjectChange = async (event) => {
    setSelectedSubject(event.target.value);

    const formData = new FormData();
    formData.append('subject_code', event.target.value);
    formData.append('token', accessToken);

    try {
      const blockData = await fetchBlockOptions(formData);
      setBlockOptions(blockData);
    } catch (error) {
      console.error('Error fetching block options:', error);
    }
  }

  const handleBlockChange = async (event) => {
    setSelectedBlock(event.target.value);

    const formData = new FormData();
    formData.append('block_id', event.target.value);
    formData.append('token', accessToken);

    try {
      const scheduleData = await fetchBlockSchedule(formData);
      props.onBlockSelect(event.target.value);
      setBlockSchedule(scheduleData);
    } catch (error) {
      console.error('Error fetching schedule from block:', error);
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
        <div className='row mb-3'>
          <label htmlFor='college' className='col-sm-2 col-form-label'>College</label>
          <div className='col-sm-10'>
            <select value={selectedCollege} onChange={handleCollegeChange} id='college' className='form-select mb-2'>
              <option value='' disabled>Select an option</option>
              {
                Object.entries(collegeOptions).map(([_, value], key) => (
                  <option key={key} value={Object.keys(value)}>
                    {value[Object.keys(value)]}
                  </option>
                ))
              }
            </select>
          </div>
        </div>
        <div className='row mb-3'>
          <label htmlFor='course' className='col-sm-2 col-form-label'>Course</label>
          <div className='col-sm-10'>
            <select value={selectedCourse} onChange={handleCourseChange} id='course' className='form-select mb-2'>
              <option value='' disabled>Select an option</option>
              {
                Object.entries(courseOptions).map(([_, value], key) => (
                  <option key={key} value={Object.keys(value)}>
                    {value[Object.keys(value)]}
                  </option>
                ))
              }
            </select>
          </div>
        </div>
        <div className='row mb-3'>
          <label htmlFor='subject' className='col-sm-2 col-form-label'>Subject</label>
          <div className='col-sm-10'>
            <select value={selectedSubject} onChange={handleSubjectChange} id='subject' className='form-select mb-2'>
              <option value='' disabled>Select an option</option>
              {
                Object.entries(subjectOptions).map(([_, value], key) => (
                  <option key={key} value={value['subject_code']}>
                    {value['subject_name']}
                  </option>
                ))
              }
            </select>
          </div>
        </div>
        <div className='row mb-3'>
          <label htmlFor='subject' className='col-sm-2 col-form-label'>Block</label>
          <div className='col-sm-10'>
            <select value={selectedBlock} onChange={handleBlockChange} id='block' className='form-select mb-2'>
              <option value='' disabled >Select an option</option>
              {
                Object.entries(blockOptions).map(([_, value], key) => (
                  <option key={key} value={value['block_id']}>
                    Block: {value['block_id']}
                  </option>
                ))
              }
            </select>
          </div>
        </div>
        <div className='d-flex justify-content-center'>
          <button type='submit' className='btn btn-outline-primary' id='enrollment-submit-btn'>Submit</button>
        </div>
        <div>
          <SchedulePreview schedule={blockSchedule} blockid={selectedBlock} />
        </div>

      </>
    )
  } else if (props.accounttype != 'EMP' && props.course) {
    setSelectedCourse(props.course);
    return (
      <>
        <div className='container-fluid d-grid gap-1 text-center'>
          Subject:
          <select value={selectedSubject} onChange={handleSubjectChange} id='subject' className='form-select mb-2'>
            <option value='' disabled>Select an option</option>
          </select>
          Block:
          <select value={selectedBlock} onChange={handleBlockChange} id='block' className='form-select mb-2'>
            <option value='' disabled>Select an option</option>
          </select>
        </div>
        <div className='d-flex justify-content-center'>
          <button type='submit' className='btn btn-outline-primary' id='enrollment-submit-btn'>Submit</button>
        </div>
        <div>
          <SchedulePreview schedule={blockSchedule} />
        </div>
      </>
    )
  } else {
    return (
      <>
        <div className='alert alert-warning'>You haven't enrolled to a course. Please select the college and course to enroll in.</div>
        <div className='container-fluid d-grid gap-1 text-center'>
          College:
          <select value={selectedCollege} onChange={handleCollegeChange} id='college' className='form-select mb-2'>
            <option value='' disabled>Select an option</option>
            {
              Object.entries(collegeOptions).map(([_, value], key) => (
                <option key={key} value={Object.keys(value)}>
                  {value[Object.keys(value)]}
                </option>
              ))
            }
          </select>
          Course:
          <select value={selectedCourse} onChange={handleCourseChange} id='course' className='form-select mb-2'>
            <option value='' disabled>Select an option</option>
            {
              Object.entries(courseOptions).map(([_, value], key) => (
                <option key={key} value={Object.keys(value)}>
                  {value[Object.keys(value)]}
                </option>
              ))
            }
          </select>
        </div>
        <div className='d-flex justify-content-center d-grid gap-5'>
          <button type='submit' className='btn btn-outline-primary disabled' id='enrollment-submit-btn'>Submit</button>
          <button type='submit' className='btn btn-secondary' id='cancel'>Cancel</button>
        </div>
      </>
    )
  }
}

export default EnrollmentFormOptions