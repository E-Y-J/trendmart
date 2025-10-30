import React from 'react';
import NavBar from '../layoutChildren/navbar/NavBar.jsx';
import MasterGrid from './MasterGrid.jsx';
import PopupLayout from './PopupLayout.jsx';
import AlertSpace from '../layoutChildren/alert/AlertSpace.jsx';
import { Outlet, useOutlet } from 'react-router-dom';

function MasterLayout({ popupChildren }) {
  const outletContent = useOutlet();

  return (
    <>
      <NavBar />
      <AlertSpace alertMessage={ 'this in an alert' } variant='info' />
      <div
        id='mainContainer'
        style={{
          width: '98%',
          alignContent: 'center',
          marginLeft: '1%',
          marginRight: '1%',
          display: 'flex',
          justifyContent: 'space-between',
          margin: 'auto',
          padding: 0,
          minHeight: '75vh',
        }}
      >
        { outletContent && <PopupLayout>{popupChildren}</PopupLayout> }
          
        <MasterGrid />
      </div>
    </>
  );
}

export default MasterLayout;
