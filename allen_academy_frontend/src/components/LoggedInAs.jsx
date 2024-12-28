import Cookies from 'js-cookie';
import { fetchUserDetails } from '../common/common';
import { useState, useEffect } from 'react';

function LoggedInAs() {
  const accessToken = Cookies.get('accessToken');
  const formData = new FormData();
  formData.append('token', accessToken);
  const [fetchedUserDetails, setFetchedUserDetails] = useState([]);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userDetails = await fetchUserDetails(formData);
        if (userDetails) {
          setFetchedUserDetails(userDetails);
        }
      } catch (error) {
        setBannerError('Failed to fetch user details');
      }
    }

    fetchUser();
  }, [accessToken]);

  return (
    <>
      <div className="d-flex justify-content-end me-2">
        <p><small>Logged in as <a href="#">{fetchedUserDetails.first_name + ' ' + fetchedUserDetails.last_name}</a></small></p>
      </div>
    </>
  )
}

export default LoggedInAs