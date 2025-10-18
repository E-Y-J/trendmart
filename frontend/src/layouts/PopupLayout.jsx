import Container from 'react-bootstrap/Container';

function PopupLayout({ children }) {
  return (
    <div className='w-100 h-100 d-flex justify-content-center align-items-center' >
      <Container className='bg-light border border-2 border-dark rounded-3 shadow-lg p-4 m-4' style={{maxWidth: '90vw', maxHeight: '90vh', overflowY: 'auto'}}>
        {children}
      </Container>
    </div>
  )
}

export default PopupLayout;