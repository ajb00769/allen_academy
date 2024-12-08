import NavBar from './NavBar';
import Banner from './Banner';

function Dashboard(props) {
  return (
    <>
      <NavBar />
      <Banner username={props.username} access={props.access} />
    </>
  )
}

export default Dashboard