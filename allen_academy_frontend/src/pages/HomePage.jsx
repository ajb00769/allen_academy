import NavBar from "../components/NavBar";
import Banner from "../components/Banner";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import RegKeyCard from "../components/RegKeyCard";
import CreateDeptCard from "../components/CreateDeptCard";
import CreateCourseCard from "../components/CreateCourseCard";
import CreateSubjectCard from "../components/CreateSubjectCard";
import CreateBlockCard from "../components/CreateBlockCard";

function HomePage() {
  const accessToken = Cookies.get('accessToken');
  const decodedToken = jwtDecode(accessToken);
  const accountType = decodedToken.account_type;

  if (accessToken != null) {
    return (
      <>
        <NavBar />
        <Banner />
        {accountType == "EMP" ? <> <RegKeyCard /> <CreateDeptCard /> <CreateCourseCard /> <CreateSubjectCard /> <CreateBlockCard /> </> : null}
      </>
    )
  } else {
    window.location.pathname = "/";
  }
}

export default HomePage;