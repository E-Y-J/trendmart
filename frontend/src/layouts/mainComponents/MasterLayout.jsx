import React from 'react';
import NavBar from '../layoutChildren/navbar/NavBar.jsx';
import MasterGrid from './MasterGrid.jsx';
import PopupLayout from './PopupLayout.jsx';
import AlertSpace from '../layoutChildren/alert/AlertSpace.jsx';
import { Outlet, useOutlet } from 'react-router-dom';

function MasterLayout({ popupChildren }) {
  const outletContent = useOutlet();

  return (
    <div
      style={{
        margin: 0,
        padding: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: '#f3f3ea',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <NavBar />
      <AlertSpace alertMessage={ 'this in an alert' } variant='info' />
      { outletContent && <PopupLayout>{popupChildren}</PopupLayout> }
      <MasterGrid />
    </div>
  );
}

export default MasterLayout;
