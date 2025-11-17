import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import Navbar from 'react-bootstrap/Navbar';
import LoginRegister from '@children/popupLayoutChildren/loginRegister/LoginRegister';
import { useTheme } from '@styles/themeContext';
import logoUrl from '/logo.svg?url';

function NavBar({ setPopup }) {
  const { theme } = useTheme();

  const LogRegLinkBtn = () => (
    <Col
      className="d-flex flex-column flex-grow-0 w-100 justify-content-end"
      style={{ minWidth: '10rem', }}
    >
      <Button
        className="align-text-center h-100"
        onClick={() => setPopup(<LoginRegister setPopup={setPopup} />)}
        style={{ ...theme.schemes.contrast }}
      >
        Login / Signup
      </Button>
    </Col>
  );

  return (
    <Navbar
      expand="lg"
      className="h-100 w-100 m-0 p-0"
      style={{ ...theme.schemes.emphasis, }}
    >
      <Col className="d-flex align-items-center flex-grow-1">
        <Image
          src={logoUrl}
          alt="Logo"
          style={{ height: '100%', maxHeight: '3rem', objectFit: 'cover' }}
        />
        <h1
          id="title"
          className="ms-3 d-none d-sm-flex text-dark mb-0"
          style={{ height: '100%' }}
        >
          TrendMart
        </h1>
      </Col>
      <LogRegLinkBtn />
    </Navbar>
  );
}

export default NavBar;
