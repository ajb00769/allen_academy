export default function RegisterParentFormFields(props) {
  const relationshipOptions = [
    { "F": "Father" },
    { "M": "Mother" },
    { "S": "Sibling" },
    { "R": "Relative" },
    { "G": "Legal Guardian" },
  ];

  return (
    <>
      <div className='row mb-3'>
        <div>
          <input id='studentid' type='text' placeholder='Student ID of Child' className='form-control text-center' onChange={props.onStudentIdChange} />
        </div>
      </div>
      <div className='row'></div>

      <div className='row mb-3'>
        <label htmlFor='relationship' className='mb-2'>Relationship</label>
        <div>
          <select value={props.selectedRelationship} id='keytype' onChange={props.onSelectedRelationshipChange} className='form-select mb-2'>
            <option value='' disabled>Select an option</option>
            {
              Object.entries(relationshipOptions).map(([_, value], key) => (
                <option key={key} value={Object.keys(value)}>
                  {value[Object.keys(value)]}
                </option>
              ))
            }
          </select>
        </div>
      </div>
    </>
  )
}