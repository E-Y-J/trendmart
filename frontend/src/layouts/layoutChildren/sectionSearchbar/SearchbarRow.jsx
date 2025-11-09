import { Row, Col, Form, Image } from 'react-bootstrap';
import filterIcon from '/filterIcon.svg?url';

function SearchbarHeader({ searchId, placeholder, filterButton = false, sectionTitle = null }) {
  return (
    <Row
      id="featuredHeader"
      className="d-flex align-items-center m-0 px-2 w-100"
      style={{ height: '2.5rem', backgroundColor: '#9f9f9f' }}
    >
      <Col className="d-flex align-items-center">
        <Form.Control
          id={searchId}
          type="text"
          placeholder={placeholder}
          style={{ height: '100%', width: '100%', boxSizing: 'border-box', fieldSizing: 'content' }}
        />
      </Col>
      {filterButton &&
        <Col className='p-0' style={{ height: '2.5rem' }}>
          <Image
            alt="filter"
            src={ filterIcon }
            style={{ height: '100%', cursor: 'pointer' }}
          />
        </Col>
      }
      {sectionTitle &&
        <Col className="d-flex justify-content-end align-items-center text-light p-0" style={{ fontSize: '1.4rem' }}>
          { sectionTitle }
        </Col>
      }
    </Row>
  );
}

export default SearchbarHeader;
