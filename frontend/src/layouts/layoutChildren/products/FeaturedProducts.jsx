import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import SearchbarRow from "../sectionSearchbar/SearchbarRow";

function FeaturedProducts() {
  return (
    <Col className='w-100 p-0'>
      <SearchbarRow
        searchId="featuredSearch"
        placeholder="Search Featured"
        sectionTitle="Featured Products"
        filterButton
      />
      <Row className='d-flex flex-row m-0 p-1'>
        <Col className="d-flex flex-column m-0 p-0">
        </Col>
      </Row>
    </Col>
  );
}

export default FeaturedProducts;
