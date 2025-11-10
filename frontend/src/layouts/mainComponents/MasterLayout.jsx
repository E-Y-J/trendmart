import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import GlobalAlert from '../layoutChildren/alert/GlobalAlert.jsx';
import MasterGrid from './MasterGrid.jsx';
import NavBar from '../layoutChildren/navbar/NavBar.jsx';
import PopupLayout from './PopupLayout.jsx';

function MasterLayout({ popupChildren }) {
  const outletContent = useOutlet();

  return (
    <Container id="superContainer" fluid className="v-100 justify-content-center align-items-center" style={{ height: '100vh', backgroundColor: '#f3f3ea' }} >
      <Row id="navbarContainer" style={{ height: '10vh', minWidth: '100%' }}>
        <NavBar />
      </Row>

      <Container id="alert-mGrid-popupContainer" fluid className='h-100 m-0 px-2'>
        <Row id="alertContainer" className="py-2" style={{ height: '8vh' }} >
          <GlobalAlert />
        </Row>

        <Row id="mGrid-popupContainer" className="pb-2" style={{ height: '81vh' }}>
          <Col className="w-100 h-100 m-0 p-0">
            <MasterGrid />
          </Col>

          {outletContent && (
              <PopupLayout>{ popupChildren }</PopupLayout>
          )}

        </Row>

      </Container>

    </Container>
  );
}

export default MasterLayout;