import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import logoUrl from '/favicon.svg?url';
import navBackground from '/nebula-9900ff.png?url';

function NavBar() {
  return (
    <Navbar className='d-flex w-100 mb-4' style={{ height: '10vh', backgroundImage: `url(${navBackground})`, backgroundColor: 'transparent', backgroundSize: 'cover' }} >
      <Container className='bg-primary justify-content-start align-items-center px' style={{height: '100%'}} >
        <img src={logoUrl} alt="Logo" style={{ height: '100%', marginLeft: '20px' }} />
        <h1 className='text-white'>
          TrendMart
        </h1>
      </Container>
      <Container className='d-flex h-100 bg-success pe-5 justify-content-end align-items-center' >
        <Button variant='light' >Login</Button>
      </Container>
    </Navbar>
  )
}


export default NavBar;