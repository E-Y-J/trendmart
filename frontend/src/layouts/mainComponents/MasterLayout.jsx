import React from 'react';
import NavBar from '../layoutChildren/navbar/NavBar.jsx';
import MasterGrid from './MasterGrid.jsx';
import PopupLayout from './PopupLayout.jsx';
import { useOutlet } from 'react-router-dom';
import { Row, Col, Container, Stack } from 'react-bootstrap';
import GlobalAlert from '../layoutChildren/alert/GlobalAlert.jsx';
import AlertSpace from '../layoutChildren/alert/AlertSpace.jsx';

function MasterLayout({ popupChildren }) {
  const outletContent = useOutlet();

  return (
    <Container fluid className="v-100 justify-content-center align-items-center" style={{ height: '100vh', backgroundColor: '#f3f3ea' }} >
        <Row id="navbarContainer" className="" style={{ height: '10vh' }}>
          <NavBar />
        </Row>
      <Container fluid className='h-100 m-0 px-2'>
        <Row id="alertSpaceContainer" className="py-2" style={{ height: '8vh' }} >
          <AlertSpace alertMessage={'abc'} variant='error' />
        </Row>
        <Row id="masterGridnPopupContainer" className="pb-2" style={{ height: '81vh' }}>
          {outletContent && (
            <Col className='h-100 w-100m-0 p-0'>
              <PopupLayout>{popupChildren}</PopupLayout>
            </Col>
          )}
          <Col className="w-100 h-100 m-0 p-0">
            <MasterGrid />
          </Col>
        </Row>
      </Container>
    </Container>


    // <Container fluid className='p-0 m-0 justify-content-center'>
    //   <Row style={{ height: '10vh' }}>
    //       <NavBar />
    //   </Row>

    //   <Row id="alterSpaceContainer" className="m-0 p-2" style={{ height: '8vh' }}>
    //     <Col className='m-0 p-0'>
    //       <AlertSpace alertMessage={'this in an alert'} variant="info" />
    //     </Col>
    //   </Row>

    //   <Row id="masterGridnPopContainer" className="align-items-center w-100 p-2" style={{ height: '82vh' }}>
    //     {outletContent && (
    //       <Col className='h-100 w-100m-0 p-0'>
    //         <PopupLayout>{popupChildren}</PopupLayout>
    //       </Col>
    //     )}
    //     <Col className="w-100 h-100 m-0 p-0">
    //       <MasterGrid />
    //     </Col>
    //   </Row>
    // </Container>
  );
}

export default MasterLayout;