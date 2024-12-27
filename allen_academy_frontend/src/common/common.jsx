import { studentCourseAPI } from '../components/constants';

export async function fetchCourseData(formData) {
  try {
    const response = await fetch(studentCourseAPI, {
      'method': 'POST',
      'body': formData,
    })

    const data = await response.json();
    return data;
  } catch {
    console.error('Unexpected error: ', error);
  }
}

export async function fetchUserDetails(accessToken) {
  try {
    const response = await fetch()
  }
}