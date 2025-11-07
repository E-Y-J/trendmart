import { Row, Col } from 'react-bootstrap';
import SearchbarRow from "../sectionSearchbar/SearchbarRow";

function RecommendedProducts() {
  return (
    <Col
      className="d-flex flex-column justify-content-start align-items-center m-0 p-0"
      style={{ width: '100%', height: '100%', backgroundColor: '#d9d9d9' }}
    >
      <SearchbarRow
        searchId="recommendedSearch"
        placeholder="Search Recommended"
        sectionTitle="Recommended Products"
      />
      <Row className='m-0 p-1'>
        Recommended products go here
      </Row>
    </Col>
  );
}

export default RecommendedProducts;
