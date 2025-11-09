import ProductCategories from '../layoutChildren/products/ProductCategories';
import FeaturedProducts from '../layoutChildren/products/FeaturedProducts';
import RecommendedProducts from '../layoutChildren/products/RecommendedProducts';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container';

function MasterGrid() {
  return (
    <Row className='w-100 h-100 d-flex flex-row m-0 p-0 gap-2'>
      <Col id="leftCol" className="d-flex flex-column bg-black m-0 p-0 h-100" style={{ maxWidth: '20%' }}>
        <ProductCategories categories={['Really long category', 'Short Cat...', 3, 4]} />
      </Col>
      <Col id="rightCol" className="bg-info d-flex flex-column h-100 w-100 gap-2" style={{ maxWidth: '80%' }}>
        <Row id="featuredRow" className="d-flex flex-row" style={{ height: '55%' }} >
          <FeaturedProducts />
        </Row>
        <Row className="d-flex flex-row" style={{ height: '45%' }}>
          <RecommendedProducts />
        </Row>
      </Col>
    </Row>


    // <Row className="d-flex flex-flex-grow-1 gap-2 m-0 p-0 h-100">
    //   <Col className="d-flex flex-column h-100 justify-content-start" style={{ width: '20%' }}>
    //     <ProductCategories categories={['Really long category', 'Short Category', 3, 4]} />
    //   </Col>

    //   <Col className="d-flex flex-column gap-2 m-0 p-0">
    //     <Row style={{ height: '60%' }} className="d-flex flex-column gap-2 bg-secondary">
    //       <FeaturedProducts />
    //     </Row>

    //     <Row style={{ height: '40%' }} className="d-flex flex-column w-100">
    //       <RecommendedProducts />
    //     </Row>
    //   </Col>
    // </Row>
  );
}

export default MasterGrid;
