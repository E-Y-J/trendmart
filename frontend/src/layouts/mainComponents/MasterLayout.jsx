import React from 'react';
import NavBar from '../layoutChildren/navbar/NavBar.jsx';
import MasterGrid from './MasterGrid.jsx';
import PopupLayout from './PopupLayout.jsx';
import AlertSpace from '../layoutChildren/alert/AlertSpace.jsx';
import { useOutlet } from 'react-router-dom';

function MasterLayout({ popupChildren }) {
  const outletContent = useOutlet();

  return (
    <div
      id="superContainer"
      style={{
        width: '100%',
        height: '100%',
        backgroundColor: '#f3f3ea'
      }}
    >
      <div
        id="navbarContainer"
        style={{
          height: '10vh',
          width: '100%',
          flexDirection: 'row'
        }}
      >
        <NavBar />
      </div>
      <div
        id="alertContainer"
        style={{
          height: '8vh',
          width: '100%',
          flexDirection: 'row',
          padding: '.5rem'
        }}
      >
        <AlertSpace alertMessage={ 'this in an alert' } variant='info' />
      </div>
      <div
        id='mainContainer'
        style={{
          height: '82vh',
          alignContent: 'center',
          display: 'flex',
          gap: '.5rem',
          padding: '0 .5rem .5rem .5rem',
        }}
      >
        { outletContent && <PopupLayout>{popupChildren}</PopupLayout> }
          
        <MasterGrid />
      </div>
    </div>
  );
}

export default MasterLayout;
