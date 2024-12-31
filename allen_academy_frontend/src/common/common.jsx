import { studentCourseAPI, getUserDetailsAPI } from '../components/constants';

export async function fetchCourseData(formData) {
  try {
    const response = await fetch(studentCourseAPI, {
      'method': 'POST',
      'body': formData,
    })

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Unexpected error: ', error);
    return null;
  }
}

export async function fetchUserDetails(formData) {
  try {
    const response = await fetch(getUserDetailsAPI, {
      'method': 'POST',
      'body': formData,
    })

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Unexpected error: ', error)
    return null;
  }
}