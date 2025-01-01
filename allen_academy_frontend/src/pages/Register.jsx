import { useState } from "react";
import RegisterParentFormFields from "../components/RegisterParentFormFields";
import RegisterStandardFormFields from "../components/RegisterStandardFormFields";
import { registrationAPI } from "../components/constants";

export default function Register() {
  const accountTypes = [{ 'EMP': 'Employee' }, { 'STU': 'Student' }, { 'PAR': 'Parent' }];

  const [selectedAccountType, setSelectedAccountType] = useState('');
  const handleSelectedAccountTypeChange = async (event) => {
    setSelectedAccountType(event.target.value);
    console.log(event.target.value);
  }

  const [selectedRelationship, setSelectedRelationship] = useState('');
  const handleSelectedRelationshipChange = async (e) => {
    setSelectedRelationship(e.target.value);
    console.log(e.target.value)
  }

  const [studentIdOfChild, setStudentIdOfChild] = useState('');
  const handleStudentIdChange = async (e) => {
    setStudentIdOfChild(e.target.value);
    console.log(e.target.value);
  }

  const [lastName, setLastName] = useState('');
  const handleLastNameChange = async (e) => {
    setLastName(e.target.value);
    console.log(e.target.value);
  }

  const [firstName, setFirstName] = useState('');
  const handleFirstNameChange = async (e) => {
    setFirstName(e.target.value);
    console.log(e.target.value);
  }

  const [email, setEmail] = useState('');
  const handleEmailChange = async (e) => {
    setEmail(e.target.value);
    console.log(e.target.value);
  }

  const [password, setPassword] = useState('');
  const handlePasswordChange = async (e) => {
    setPassword(e.target.value);
    console.log(e.target.value);
  }

  const [confirmPassword, setConfirmPassword] = useState('');
  const handleConfirmPasswordChange = async (e) => {
    setConfirmPassword(e.target.value);
    console.log(e.target.value);
    // check if passwords match
    if (e.target.value != password) {
      setSubmitError('Passwords do not match.')
      return
    }
    setSubmitError('');
  }

  const [address, setAddress] = useState('');
  const handleAddressChange = async (e) => {
    setAddress(e.target.value);
    console.log(e.target.value);
  }

  const [phoneNumber, setPhoneNumber] = useState('');
  const handlePhoneNumberChange = async (e) => {
    setPhoneNumber(e.target.value);
    console.log(e.target.value);
  }

  const [registrationKey, setRegistrationKey] = useState('');
  const handleRegistrationKeyChange = async (e) => {
    setRegistrationKey(e.target.value);
    console.log(e.target.value);
  }

  const [birthDate, setBirthDate] = useState('');
  const handleBirthDateChange = async (e) => {
    setBirthDate(e.target.value);
    console.log(e.target.value);
  }

  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const yearLevelOptions = [
    { "EMS1": "Elementary School 1" },
    { "EMS2": "Elementary School 2" },
    { "EMS3": "Elementary School 3" },
    { "EMS4": "Elementary School 4" },
    { "EMS5": "Elementary School 5" },
    { "EMS6": "Elementary School 6" },

    { "MDS1": "Middle School 1" },
    { "MDS2": "Middle School 2" },
    { "MDS3": "Middle School 3" },
    { "MDS4": "Middle School 4" },

    { "SHS1": "High School 1" },
    { "SHS2": "High School 2" },
    { "SHS3": "High School 3" },
    { "SHS4": "High School 4" },

    { "COL1": "College Level 1" },
    { "COL2": "College Level 2" },
    { "COL3": "College Level 3" },
    { "COL4": "College Level 4" },
    { "COL5": "College Level 5" },

    { "LAW1": "Law 1" },
    { "LAW2": "Law 2" },
    { "LAW3": "Law 3" },
    { "LAW4": "Law 4" },

    { "MST1": "Masters 1" },
    { "MST2": "Masters 2" },
    { "MST3": "Masters 3" },

    { "PHD1": "Doctorate 1" },
    { "PHD2": "Doctorate 2" },
    { "PHD3": "Doctorate 3" },
    { "PHD4": "Doctorate 4" },
    { "PHD5": "Doctorate 5" },
    { "PHD6": "Doctorate 6" },
    { "PHD7": "Doctorate 7" }
  ];
  const [selectedYearLevel, setSelectedYearLevel] = useState('');
  const handleYearLevelChange = async (e) => {
    setSelectedYearLevel(e.target.value);
  }

  const teachingYearLevelOptions = [
    { "REGS": "Regular Staff" },
    { "PHDT": "PHD Teacher" },
    { "MSTT": "Masters Teacher" },
    { "LAWT": "Law Teacher" },
    { "COLT": "College Teacher" },
    { "SHST": "High School Teacher" },
    { "MDST": "Middle School Teacher" },
    { "EMST": "Elementary School Teacher" }
  ];
  const [selectedTeachingYearLevel, setSelectedTeachingYearLevel] = useState('');
  const handleTeachingYearLevelChange = async (e) => {
    setSelectedTeachingYearLevel(e.target.value);
  }

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    if (lastName == '' || firstName == '' || password == '' || email == '' || address == '' || birthDate == '' || phoneNumber == '' || selectedAccountType == '' || registrationKey == '') {
      setSubmitError('Required field is empty.');
      return;
    }

    if (selectedAccountType == 'PAR' && (studentIdOfChild == '' || selectedRelationship == '')) {
      setSubmitError('Required field is empty.');
      return;
    }

    if (password != confirmPassword) {
      setSubmitError('Passwords do not match.');
      return;
    }

    const formData = new FormData();
    formData.append('last_name', lastName);
    formData.append('first_name', firstName);
    formData.append('password', password);
    formData.append('email', email);
    formData.append('address', address);
    formData.append('birthday', birthDate);
    formData.append('phone', phoneNumber);
    formData.append('key_type', selectedAccountType);
    formData.append('reg_key', registrationKey);

    if (selectedAccountType == "PAR") {
      formData.append('student', studentIdOfChild);
      formData.append('relationship', selectedRelationship);
    }

    if (selectedAccountType == "EMP") {
      formData.append('teaching_year_lvl', selectedTeachingYearLevel);
    }

    try {
      const response = await fetch(registrationAPI, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json();

      if (data.account_id) {
        setSubmitSuccess(true);
        setTimeout(() => {
          window.location.pathname = "/";
        }, 3000);
      } else {
        setSubmitError(data.error);
      }
    } catch (error) {
      setSubmitError('An unexpected error occured. Please contact support.');
      console.error(error);
    }
  }

  return (
    <>
      {!submitSuccess &&
        (<div className='text-center mt-3'>
          <h2>Register an Account</h2>
          {submitError && (<div className='continer mx-auto alert alert-warning text-center w-75'>{submitError}</div>)}
          <div className='container d-flex justify-content-center mx-auto my-5 card-max-width'>
            <form method='POST' id='registration-form' onSubmit={handleFormSubmit}>
              <div className='row mb-3'>
                <label htmlFor='accounttype' className='mb-3'>Select an Account Type</label>
                <div>
                  <select value={selectedAccountType} id='keytype' onChange={handleSelectedAccountTypeChange} className='form-select mb-2'>
                    <option value='' disabled>Select an option</option>
                    {
                      Object.entries(accountTypes).map(([_, value], key) => (
                        <option key={key} value={Object.keys(value)}>
                          {value[Object.keys(value)]}
                        </option>
                      ))
                    }
                  </select>
                </div>
              </div>
              <RegisterStandardFormFields onLastNameChange={handleLastNameChange} onFirstNameChange={handleFirstNameChange} onEmailChange={handleEmailChange} onPasswordChange={handlePasswordChange} onConfirmPasswordChange={handleConfirmPasswordChange} onAddressChange={handleAddressChange} onPhoneNumberChange={handlePhoneNumberChange} onRegistrationKeyChange={handleRegistrationKeyChange} onBirthDateChange={handleBirthDateChange} />
              {
                selectedAccountType == "EMP" && (
                  <div className='mb-3'>
                    <label htmlFor='teachingyearlevel' className='col-form-label'>Teaching Year Level</label>
                    <select value={selectedTeachingYearLevel} onChange={handleTeachingYearLevelChange} id='teachingyearlevel' className='form-select mb-2'>
                      <option value='' disabled>Select an option</option>
                      {
                        Object.entries(teachingYearLevelOptions).map(([_, value], key) => (
                          <option key={key} value={Object.keys(value)}>
                            {value[Object.keys(value)]}
                          </option>
                        ))
                      }
                    </select>
                  </div>
                )
              }
              {
                selectedAccountType == "PAR" && (<RegisterParentFormFields selectedRelationship={selectedRelationship} onSelectedRelationshipChange={handleSelectedRelationshipChange} onStudentIdChange={handleStudentIdChange} />)
              }
              <div className='d-flex justify-content-center'>
                <button type='submit' className='btn btn-outline-primary' id='registration-submit-btn'>Submit</button>
              </div>
            </form>
          </div>
        </div>)
      }
      {submitSuccess && (
        <div className='alert alert-success text-center w-75'>Account registration successful. You can now log in. <p className='fw-bold'>Redirecting the page...</p></div>
      )
      }
    </>
  )
}