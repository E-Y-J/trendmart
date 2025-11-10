import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'

function ProductGrid(){
  return (
    <Row className='d-flex flex-row h-100 w-100 m-0 p-1 gap-1'>
      <Col xs={ 6 } md={ 4 } className="d-flex flex-column m-0 p-0 bg-info" style={{ height: '100%', maxWidth: '50%' }}>
      </Col>
      <Col xs={ 6 } md={ 2 } className='d-flex flex-column flex-grow-1 bg-success'>
        <Row xs={ 6 } id="cardContainer1" className='d-flex flex-row h-50 bg-secondary'>
        
        </Row>
        <Row xs={ 6 } id="cardContainer2" className='d-flex flex-row h-50'>
        
        </Row>
      </Col>
    </Row>
  )
}

export default ProductGrid;