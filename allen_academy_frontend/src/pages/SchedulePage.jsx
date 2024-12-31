import NavBar from '../components/NavBar';
import LoggedInAs from '../components/LoggedInAs';
import ScheduleList from '../components/ScheduleList';
import Cookie from 'js-cookie';

function SchedulePage() {
  if (!Cookie.get('accessToken')) {
    window.location.pathname = '/';
  } else {
    return (
      <>
        <NavBar />
        <LoggedInAs />
        <ScheduleList />
      </>
    )
  }
}

export default SchedulePage;