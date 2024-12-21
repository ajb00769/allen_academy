import Cookies from 'js-cookie';

const handleLogout = () => {
	Object.keys(Cookies.get()).forEach(cookie => {
		Cookies.remove(cookie);
	})
}

function NavBar() {
	return (
		<>
			<nav className="navbar navbar-expand-md navbar-dark sticky-top bg-dark">
				<div className="container-fluid">
					<a className="navbar-brand" href="#">Allen Academy</a>
					<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"></span>
					</button>
					<div className="collapse navbar-collapse justify-content-end" id="navbarNav">
						<ul className="navbar-nav">
							<li className="nav-item">
								<a className="nav-link" href="/home">Home</a>
							</li>
							<li className="nav-item">
								<a className="nav-link" href="/enrollment">Enrollment</a>
							</li>
							<li className="nav-item">
								<a className="nav-link" href="/schedule">Schedule</a>
							</li>
							<li className="nav-item">
								<a className="nav-link text-danger" onClick={handleLogout} href="/">Logout</a>
							</li>
						</ul>
					</div>
				</div>
			</nav>
		</>
	)
}

export default NavBar