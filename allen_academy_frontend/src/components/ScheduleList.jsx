import React, { useState, useEffect } from "react";
import { userScheduleAPI } from "./constants";

function ScheduleList(props) {
  const [scheduleList, setScheduleList] = useState([]);
  const [noSchedules, setNoSchedules] = useState(false);
  const formData = new FormData();
  formData.append('token', props.access);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch(userScheduleAPI, {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();

        if (data.result.length > 0) {
          console.log(data.result);
          setScheduleList(data.result);
        } else {
          console.log("no schedules");
          setNoSchedules(true);
        }
      } catch (error) {
        console.error('Unexpected error', error);
      }
    }

    fetchData();
  }, []);

  if (noSchedules) {
    return (
      <div className="text-center">
        <div>
          <p>You are not enrolled to any subjects. Please enroll to see your schedules.</p>
        </div>
      </div>
    );
  } else {
    return (
      <>
        <div>
          <div className="h3 text-center">Here are your schedules</div>
          <div>
            <table className="table">
              <thead>
                <tr>
                  <th scope="col">Block ID</th>
                  <th scope="col">Course</th>
                  <th scope="col">Units</th>
                  <th scope="col">Year Level</th>
                  <th scope="col">Room</th>
                  <th scope="col">Subject</th>
                  <th scope="col">Day</th>
                  <th scope="col">Start Time</th>
                  <th scope="col">End Time</th>
                </tr>
              </thead>
              <tbody>
                {
                  scheduleList.map((schedule, index) => (
                    <tr key={index}>
                      <td>{schedule.block_id}</td>
                      <td>{schedule.course_code}</td>
                      <td>{schedule.subject_units}</td>
                      <td>{schedule.course_yr_lvl}</td>
                      <td>{schedule.room_no}</td>
                      <td>{schedule.subject_name}</td>
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
    );
  }
}

export default ScheduleList;
