import NavBar from "../components/NavBar";
import Banner from "../components/Banner";
import Cookies from "js-cookie";

function HomePage() {
  const accessToken = Cookies.get('accessToken');

  if (accessToken != null) {
    return (
      <>
        <NavBar />
        <Banner />
      </>
    )
  } else {
    window.location.pathname = "/";
  }
}

export default HomePage;