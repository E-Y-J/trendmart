import NavBar from '../navbar/NavBar.jsx';
import MasterGrid from './MasterGrid.jsx';
import PopupLayout from './PopupLayout.jsx';
import bg from '/starBg.png?url';

function MasterLayout({ PopupChildren }) {
  return (
    <div
      style={{
        margin: 0,
        padding: 0,
        width: '100vw',
        height: '100vh',
        backgroundImage: `url(${bg})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <NavBar />
      <div id="alertSpace" style={{ height: '8vh', color: 'white' }}>alert space</div>
      {PopupChildren && <PopupLayout>{PopupChildren}</PopupLayout>}
      <MasterGrid />
      <div style={{ height: '4vh', color: 'white', justifyContent: 'center', alignItems: 'center', display: 'flex' }}>
        links: legal, privacy, terms | &copy; TrendMart 2024
      </div>
    </div>
  );
}

export default MasterLayout;
