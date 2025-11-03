import LoginRegister from '../../../loginRegister/LoginRegister';
import logoUrl from '/logo.svg?url';
import { useNavigate } from 'react-router-dom';



function NavBar() {
  const navigate = useNavigate()

  const LoginRegisterButton = () => {
    return (
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '80vh'
        }}
      >
        <button
          onClick={() => navigate("/login")}
          style={{
            padding: '0.5rem 1rem',
            cursor: 'pointer'
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
        backgroundColor: '#797975',
      }}
    >
      {/* Left container */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'flex-start',
          height: '100%',
          padding: '1%',
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
          justifyContent: 'flex-end',
          height: '100%',
          paddingRight: '3rem', 
        }}
      >
        <LoginRegisterButton />
      </div>
    </div>
  );
}

export default NavBar;
