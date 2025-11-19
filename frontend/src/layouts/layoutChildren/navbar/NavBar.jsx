import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import LoginRegister from '@children/popupLayoutChildren/loginRegister/LoginRegister';
import { useTheme } from '@styles/themeContext';
import Logo from '../logo/Logo';
import HoverLink from './HoverLink';



function NavBar({ setPopup }) {
  const { theme } = useTheme();
  const navigate = useNavigate(); // for testing shipping pop up navigation

  const LogRegLinkBtn = () => (
    <Button
      onClick={() => setPopup(<LoginRegister setPopup={setPopup} />)}
      className="px-3"
      style={{ ...theme.schemes.contrast, fontSize: '.9rem' }}
    >
      Login / Signup
    </Button>
  );

  return (
    <Navbar
      expand="md"
      className="d-flex w-100 h-100 m-0 p-0 px-2 d-flex align-items-center"
      style={{
        backgroundColor: theme.colors.darkBg,
        borderRadius: `${Array(2).fill(theme.props.borderRadius).join(' ')} 0 0`,
      }}
    >
      {/* LEFT: Logo + Brand */}
      <Col className="d-flex align-items-center flex-grow-1 gap-3">
        <Navbar.Brand
          className="d-flex align-items-center p-0 m-0"
          style={{ height: '8vh' }}
        >
          <Logo variant='white' />
        </Navbar.Brand>
        <h1
          id="title"
          className="mb-0 fs-3"
          style={{ fontWeight: 700, color: theme.colors.lightBg }}
        >
          TrendMart
        </h1>
      </Col>

      {/* CENTER HoverLinkS */}
      <Nav className="d-none d-md-flex gap-4 ms-auto me-4">
        <HoverLink linksTo="/" >
          Home
        </HoverLink >
        <HoverLink linksTo="/profile">Profile</HoverLink>
        <HoverLink linksTo="/contact">Contact</HoverLink>
      </Nav>

      {/* RIGHT: Login Button */}
      <LogRegLinkBtn />
      <Button
        className="ms-3"
        variant="dark"
        style={{ ...theme.buttons?.splash }}
        onClick={() => navigate('/checkout/shipping')}
      > // this button is for testing shipping pop up, will be removed later
        Checkout
      </Button>
    </Navbar>
  );
}

export default NavBar;
