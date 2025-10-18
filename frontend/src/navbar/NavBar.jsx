// import Navbar from 'react-bootstrap/Navbar';
import logoUrl from '/favicon.svg?url';
import navBackground from '/nebula-9900ff.png?url';

function NavBar() {
    return (
        <div className='mb-4' style={{width: '100vw', height: '150px', backgroundImage: `url(${navBackground})`, backgroundColor: 'transparent', backgroundSize: 'cover', display: 'flex', alignItems: 'center'}}>
            <img src={logoUrl} alt="Logo" style={{ height: '100%', marginLeft: '20px' }} />
            <h1 className='text-white'>
                TrendMart NavBar
            </h1>
        </div>
    )
}


export default NavBar;