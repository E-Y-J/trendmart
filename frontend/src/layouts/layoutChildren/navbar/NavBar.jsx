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
            position: 'relative',
            width: '7rem',
            height: '3rem',
            fontSize: '1.3rem',
            fontWeight: 600,
            color: '#fffffb',
            backgroundColor: '#0a1f44',
            borderRadius: '12rem',
            border: '.3rem groove #00aef0',
            overflow: 'hidden',
            cursor: 'pointer',
          }}
        >
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '7rem',
              height: '3rem',
              backgroundColor: '#fffffb55',
              filter: 'blur(8r)',
              backdropFilter: 'blur(5px)',
              borderRadius: '12rem 12rem',
              zIndex: 1,
              pointerEvents: 'none',
            }}
          />
          <div
            style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              zIndex: 2,
              color: '#fffffb',
            }}
          >
            Login
          </div>
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
