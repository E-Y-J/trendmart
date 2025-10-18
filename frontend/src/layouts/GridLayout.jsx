import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ProductCategories from '../products/ProductCategories.jsx';
import FeaturedProducts from '../products/FeaturedProducts.jsx';
import RecommendedProducts from '../products/RecommendedProducts.jsx';

function GridLayout() {
  return (
    <div className='w-100 m-0' >
      <Row className='w-100 bg-primary justify-content-between m-0 p-0' style={{minHeight: '75vh'}} >
        <Col id='category' md={2} className='bg-info alignjustify-content-evenly gap-2 m-0 p-0'>
          <ProductCategories />
        </Col>
        <Col id='products' md={10} className='bg-secondary align-content-stretch m-0 p-0'>
          <Row className='bg-warning m-0 p-0 d-flex justify-content-center align-items-center'>
            <Col md={4} className='mx-2 p-0 bg-white' style={{height: '10%'}}>SearchBar</Col>
            <Col className='bg-black text-white'>
              <h1 className='float-end'>
                Current Category Title
              </h1>
            </Col>
          </Row>
          <Row id='featured' className='bg-danger m-0 p-0' style={{height: '60%'}}>
            <FeaturedProducts />
          </Row>
          <Row id='recommended' className='bg-success m-0 p-0' style={{height: '30%'}}>
            <RecommendedProducts />
          </Row>
        </Col>
      </Row>
    </div>
  )
}

export default GridLayout;