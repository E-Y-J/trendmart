import { Row, Col, Form, Image } from 'react-bootstrap';
import filterIcon from '/filterIcon.svg?url';

function SearchbarHeader({ searchId, placeholder, filterButton = false, sm=null, sectionTitle = null }) {
  return (
    <Row
      id="featuredHeader"
      className="d-flex flex-grow-0 align-items-center m-0 w-100 px-1 py-0 px-sm-1 gap-1"
      style={{ height: '2.5rem', backgroundColor: '#9f9f9f' }}
    >
      <Col xs={ 10 } sm={ sm } className="d-flex flex-grow-0 flex-shrink-1 align-items-center p-0">
        <Form.Control
          id={ searchId }
          type="text"
          placeholder={ placeholder }
          className='h-100 w-100'
          style={{ boxSizing: 'border-box', fieldSizing: 'content' }}
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
        <Col className="d-flex flex-grow-1 justify-content-end align-items-center text-light p-0 text-nowrap d-none d-sm-flex" style={{ fontSize: 'clamp(1rem ' }}>
          { sectionTitle }
        </Col>
      }
    </Row>
  );
}

export default SearchbarHeader;
