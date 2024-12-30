import NavBar from "../components/NavBar";
import Banner from "../components/Banner";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import RegKeyCard from "../components/RegKeyCard";

function HomePage() {
  const accessToken = Cookies.get('accessToken');
  const decodedToken = jwtDecode(accessToken);
  const accountType = decodedToken.account_type;

  if (accessToken != null) {
    return (
      <>
        <NavBar />
        <Banner />
        {accountType == "EMP" ? <> <RegKeyCard /> </> : null}
      </>
    )
  } else {
    window.location.pathname = "/";
  }
}

export default HomePage;