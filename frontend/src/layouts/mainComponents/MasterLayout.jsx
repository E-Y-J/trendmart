import NavBar from '../layoutChildren/navbar/NavBar.jsx';
import MasterGrid from './MasterGrid.jsx';
import PopupLayout from './PopupLayout.jsx';
import AlertSpace from '../layoutChildren/alert/AlertSpace.jsx';

function MasterLayout({ popupChildren, setPopup }) {
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
      <NavBar setPopup={setPopup} />
      <AlertSpace alertMessage={ 'this in an alert' } variant='info' />
      { popupChildren && <PopupLayout children={ popupChildren } /> }
      <MasterGrid />
      <div style={{ height: '4vh', color: 'white', justifyContent: 'center', alignItems: 'center', display: 'flex' }}>
        links: legal, privacy, terms | &copy; TrendMart 2024
      </div>
    </div>
  );
}

export default MasterLayout;
