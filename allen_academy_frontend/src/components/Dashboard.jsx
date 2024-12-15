import NavBar from './NavBar';
import Banner from './Banner';
import ScheduleList from './ScheduleList';

function Dashboard(props) {
  return (
    <>
      <NavBar />
      <Banner username={props.username} access={props.access} />
      <ScheduleList access={props.access} />
    </>
  )
}

export default Dashboard