import { useState } from "react";
import RegisterEmployeeFormFields from "../components/RegisterEmployeeFormFields";
import RegisterStudentFormFields from "../components/RegisterStudentFormFields";
import RegisterParentFormFields from "../components/RegisterParentFormFields";

export default function Register() {
  const accountTypes = [{ 'EMP': 'Employee' }, { 'STU': 'Student' }, { 'PAR': 'Parent' }];
  const [selectedAccountType, setSelectedAccountType] = useState('');

  const handleSelectedAccountTypeChange = async (event) => {
    setSelectedAccountType(event.target.value);
    console.log(event.target.value);
  }

  return (
    <>
      <div className='text-center mt-3'>
        <h2>Register an Account</h2>
        <div className='container d-flex justify-content-center mx-auto my-5 card-max-width'>
          <form>
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
            {
              selectedAccountType == "EMP" ? <RegisterEmployeeFormFields /> :
                selectedAccountType == "STU" ? <RegisterStudentFormFields /> :
                  selectedAccountType == "PAR" ? <RegisterParentFormFields /> : null
            }
          </form>
        </div>
      </div>
    </>
  )
}