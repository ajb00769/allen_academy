export default function SchedulePreview(props) {
  if (props.schedule.length > 0) {
    return (
      <>
        <div>
          <div className="h3 text-center">Schedule Preview for Block {props.blockid}</div>
          <div>
            <table className="table">
              <thead>
                <tr>
                  <th scope="col">Room</th>
                  <th scope="col">Day</th>
                  <th scope="col">Start Time</th>
                  <th scope="col">End Time</th>
                </tr>
              </thead>
              <tbody>
                {
                  props.schedule.map((schedule, index) => (
                    <tr key={index}>
                      <td>{schedule.room_no}</td>
                      <td>{schedule.day_of_wk}</td>
                      <td>{schedule.start_time}</td>
                      <td>{schedule.end_time}</td>
                    </tr>
                  ))
                }
              </tbody>
            </table>
          </div>
        </div>
      </>
    )
  }
}