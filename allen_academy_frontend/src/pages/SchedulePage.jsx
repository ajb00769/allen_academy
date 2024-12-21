import NavBar from '../components/NavBar';
import LoggedInAs from '../components/LoggedInAs';
import ScheduleList from '../components/ScheduleList';

function SchedulePage() {
  return (
    <>
      <NavBar />
      <LoggedInAs />
      <ScheduleList />
    </>
  )
}

export default SchedulePage;