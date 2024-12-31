export default function RegisterStandardFormFields(props) {
  return (
    <>
      <div className='row mb-3'>
        <div>
          <input id='lastname' type='text' placeholder='Last Name' className='form-control text-center' onChange={props.onLastNameChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <div>
          <input id='firstname' type='text' placeholder='First Name' className='form-control text-center' onChange={props.onFirstNameChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <div>
          <input id='emailaddress' type='email' placeholder='Email Address' className='form-control text-center' onChange={props.onEmailChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <div>
          <input id='password' type='password' placeholder='Password' className='form-control text-center' onChange={props.onPasswordChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <div>
          <input id='confirmpassword' type='password' placeholder='Confirm Password' className='form-control text-center' onChange={props.onConfirmPasswordChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <div>
          <input id='address' type='text' placeholder='Address' className='form-control text-center' onChange={props.onAddressChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <div>
          <input id='phonenumber' type='text' placeholder='Phone Number' className='form-control text-center' onChange={props.onPhoneNumberChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <div>
          <input id='registrationkey' type='text' placeholder='Registration Key' className='form-control text-center' onChange={props.onRegistrationKeyChange} />
        </div>
      </div>
      <div className='row mb-3'>
        <label htmlFor='birthdate' className='mb-2'>Birth Date</label>
        <div>
          <input id='birthdate' type='date' className='form-control text-center' onChange={props.onBirthDateChange} />
        </div>
      </div>
    </>
  )
}