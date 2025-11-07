import LoginRegister from '../popupLayoutChildren/loginRegister/LoginRegister';
import logoUrl from '/logo.svg?url';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar, Button, Image, Col } from 'react-bootstrap';
import NavLink from 'react-bootstrap/NavLink'

function NavBar() {
  const navigate = useNavigate();

  const LoginRegisterButton = () => (
    <Col className="d-flex w-100 justify-content-end">
      <NavLink className="bg-white align-t w-25 h-100" onClick={() => navigate("/login")}>
        Login
      </NavLink>
    </Col>
  );

  return (
    <Navbar bg="secondary" expand="lg" className="h-100 w-100 m-0 p-0">
      <div className="d-flex w-100 m-0 px-3 py-0 align-items-center">
        <Col className="d-flex align-items-center">
          <Image src={logoUrl} alt="Logo" style={{ height: '100%', maxHeight: '3rem', objectFit: 'contain' }} />
          <h1 id="title" className="ms-3 text-dark mb-0">TrendMart</h1>
        </Col>
        <LoginRegisterButton />
      </div>
    </Navbar>
  );
}

export default NavBar;
