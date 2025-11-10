import { useNavigate } from 'react-router-dom';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import Navbar from 'react-bootstrap/Navbar';
import NavLink from 'react-bootstrap/NavLink';
import Row from 'react-bootstrap/Row';
import logoUrl from '/logo.svg?url';


function NavBar() {
  const navigate = useNavigate();

  const LogRegLinkCol = () => (
    <Col 
      className="d-flex flex-column flex-grow-0 w-100 justify-content-end" 
      style={{ minWidth: '10rem' }}
    >
      <NavLink 
        className="bg-white align-t h-100"
        onClick={() => navigate("/login")}
      >
        Login
      </NavLink>
    </Col>
  );

  return (
    <Navbar bg="secondary" expand="lg" className="h-100 w-100 m-0 p-0">
        <Col className="d-flex align-items-center flex-grow-1">
          <Image src={ logoUrl } alt="Logo" style={{ height: '100%', maxHeight: '3rem', objectFit: 'contain' }} />
          <h1 id="title" className="ms-3 d-none d-sm-flex text-dark mb-0" style={{ height: '100%' }}>TrendMart</h1>
        </Col>
        <LogRegLinkCol />
    </Navbar>
  );
}

export default NavBar;