import { Row, Col, Container } from 'react-bootstrap';
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
      <Row className='m-0 p-1'>
        Featured products go here
      </Row>
    </Col>
  );
}

export default FeaturedProducts;
