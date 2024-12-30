import LoginPage from './pages/LoginPage';
import EnrollmentPage from './pages/EnrollmentPage';
import SchedulePage from './pages/SchedulePage';
import HomePage from './pages/HomePage';
import RegKey from './pages/RegKey';

function App() {
  let Page;
  switch (window.location.pathname) {
    case "/":
      Page = <LoginPage />
      break;
    case "/home":
      Page = <HomePage />
      break;
    case "/enrollment":
      Page = <EnrollmentPage />
      break;
    case "/schedule":
      Page = <SchedulePage />
      break;
    case "/regkey":
      Page = <RegKey />
      break;
    default:
      Page = <LoginPage />
      break;
  }
  return (
    <>
      {Page}
    </>
  )
}

export default App