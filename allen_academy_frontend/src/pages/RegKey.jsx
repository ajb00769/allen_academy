import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import { useState } from "react";
import NavBar from "../components/NavBar";
import LoggedInAs from "../components/LoggedInAs";
import { getAccountTypeOptionsAPI } from "../components/constants";

async function fetchKeyTypeOptions(formData) {
  try {
    const response = await fetch(getAccountTypeOptionsAPI, {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    if (data.data) {
      return data.data;
    }
  } catch (error) {
    console.error('Error fetching key type options: ', error);
  }
}

export default function RegKey() {
  const accessToken = Cookies.get('accessToken');
  const decodedToken = jwtDecode(accessToken);
  const accountType = decodedToken.account_type;

  const keyTypeOptions = [{ 'EMP': 'Employee' }, { 'STU': 'Student' }, { 'PAR': 'Parent' }];
  const [selectedKeyType, setSelectedKeyType] = useState('');
  const [accountTypeOptions, setAccountTypeOptions] = useState([]);
  const [selectedAccountTypeOption, setSelectedAccountTypeOption] = useState('');
  const [generatedFor, setGeneratedFor] = useState('');

  const handleSelectedKeyTypeChange = async (event) => {
    setSelectedKeyType(event.target.value);

    const formData = new FormData();
    formData.append('token', accessToken);
    formData.append('account_type', accountType);
    formData.append('key_type', event.target.value);

    try {
      const result = await fetchKeyTypeOptions(formData);
      setAccountTypeOptions(result);
    } catch (error) {
      console.error('Error fetching key type options: ', error);
    }
  }

  const handleRegKeyFormSubmit = (event) => {
    event.preventDefault();

    console.log(selectedKeyType);
    console.log(generatedFor);
  }

  if (accountType == "EMP") {
    return (
      <>
        <NavBar />
        <LoggedInAs />
        <div>
          <h2 className='text-center mt-2 mb-5'>Registration Key Generation</h2>
          <form method='POST' id='reg-key-form' onSubmit={handleRegKeyFormSubmit}>
            <div className='container d-grid gap-2 card-max-width'>
              <div className='row mb-3'>
                <label htmlFor='keytype' className='col-sm-2 col-form-label'>Key Type</label>
                <div className='col-sm-10'>
                  <select value={selectedKeyType} id='keytype' onChange={handleSelectedKeyTypeChange} className='form-select mb-2'>
                    <option value='' disabled>Select an option</option>
                    {
                      Object.entries(keyTypeOptions).map(([_, value], key) => (
                        <option key={key} value={Object.keys(value)}>
                          {value[Object.keys(value)]}
                        </option>
                      ))
                    }
                  </select>
                </div>
              </div>
              <div className='row mb-3'>
                <label htmlFor='accounttypeoption' className='col-sm-2 col-form-label'>Year Level/Relationship</label>
                <div className='col-sm-10'>
                  <select value={selectedAccountTypeOption} id='keytype' className='form-select mb-2' onChange={(e) => { setSelectedAccountTypeOption(e.target.value) }}>
                    <option value='' disabled>Select an option</option>
                    {
                      Object.entries(accountTypeOptions).map(([_, value], key) => (
                        <option key={key} value={Object.keys(value)}>
                          {value[Object.keys(value)]}
                        </option>
                      ))
                    }
                  </select>
                </div>
              </div>
              <div className='row mb-3'>
                <label htmlFor='generatedfor' className='col-sm-2 col-form-label'>Full Name</label>
                <div className='col-sm-10'>
                  <input id='generatedfor' type='text' className='form-control text-center' placeholder='LastName FirstName MiddleName' value={generatedFor} onChange={(e) => { setGeneratedFor(e.target.value) }} />
                </div>
              </div>
            </div>
            <div className='d-flex justify-content-center'>
              <button type='submit' className='btn btn-outline-primary' id='regkey-submit-btn'>Submit</button>
            </div>
          </form>
        </div>
      </>
    )
  } else {
    window.location.pathname = "/home";
  }
}