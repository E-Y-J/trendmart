import { Routes, Route } from 'react-router-dom';
import logoUrl from '/favicon.svg?url';
import navBackground from '/nebula-9900ff.png?url';

function NavBar() {
  return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        height: '10vh',
        backgroundImage: `url(${navBackground})`,
        
        backgroundSize: '100% 100%',
        marginBottom: '1.5rem', 
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
          paddingLeft: '1rem',
          paddingRight: '1rem',
        }}
      >
        <img
          src={logoUrl}
          alt="Logo"
          style={{ height: '100%', marginLeft: '20px', objectFit: 'contain' }}
        />
        <h1 style={{ color: 'white', marginLeft: '1rem' }}>TrendMart</h1>
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
        <button
          style={{
            
            color: 'black',
            border: '1px solid rgba(0,0,0,0.2)',
            borderRadius: '0.375rem',
            padding: '0.375rem 0.75rem',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: 500,
            transition: 'background-color 0.2s ease',
          }}
        >
          Login
        </button>
      </div>
    </div>
  );
}

export default NavBar;
