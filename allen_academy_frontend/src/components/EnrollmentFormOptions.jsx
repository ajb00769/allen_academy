import { useState } from 'react';

function EnrollmentFormOptions(props) {
  const [] = useState('');

  if (props.accounttype == 'EMP') {
    return (
      <>
        <div>
          College:
          <select name="college" id="college">
            <option value="option1college">College</option>
          </select>
        </div>
        <div>
          Course:
          <select name="course" id="course">
            <option value="option1course">Course</option>
          </select>
        </div>
        <div>
          Subject:
          <select name="subject" id="subject">
            <option value="option1subject">Subject</option>
          </select>
        </div>
        <div>
          Block:
          <select name="block" id="block">
            <option value="option1block">Block</option>
          </select>
        </div >
      </>
    )
  } else if (props.accounttype == 'STU') {
    return (
      <>
        <div>
          Subject:
          <select name="subject" id="subject">
            <option value="option1">Subject</option>
          </select>
        </div>
        <div>
          Block:
          <select name="block" id="block">
            <option value="option1block">Block</option>
          </select>
        </div>
      </>
    )
  }
}

export default EnrollmentFormOptions