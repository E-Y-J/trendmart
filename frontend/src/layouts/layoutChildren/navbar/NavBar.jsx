import LoginRegister from '../../../loginRegister/LoginRegister';
import logoUrl from '/logo.svg?url';
import { useNavigate } from 'react-router-dom';

function NavBar() {
  const navigate = useNavigate()

  const LoginRegisterButton = () => {
    return (
      <div
        id="logRegContainer"
        style={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#fffffb'
        }}
      >
        <button
          id="toLoginButton"
          onClick={() => navigate("/login")}
          style={{
            position: 'relative',
            width: '7rem',
            height: '3rem',
            fontSize: '1.3rem',
            fontWeight: 600,
            color: '#0a1f44',
            backgroundColor: 'transparent',
            border: 'none',
            overflow: 'hidden',
            cursor: 'pointer',
          }}
        >
          Login
        </button>
      </div>
    )
  }

  return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        height: '100%',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      {/* Left container */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-start',
          height: '100%',
        }}
      >
        <img
          src={logoUrl}
          alt="Logo"
          style={{ height: '100%', objectFit: 'contain' }}
        />
        <h1
        id="title"
        style={{
          color: '#0a1f44',
          marginLeft: '1rem'
        }}
        >
          TrendMart</h1>
      </div>
      {/* Right container */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          alignContent: 'flex-end',
          height: '100%',
        }}
      >
        <LoginRegisterButton />
      </div>
    </div>
  );
}

export default NavBar;
