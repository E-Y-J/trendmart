
import NavBar from '../navbar/NavBar.jsx';
import MasterGrid from './MasterGrid.jsx';
import PopupLayout from './PopupLayout.jsx';
import bg from '/starBg.png?url';

function MasterLayout({ PopupChildren }) {
  return (
    <div  className='p-0 m-0' style={{width: '100vw', height: '100vh',backgroundImage: `url(${bg})`, backgroundSize: 'cover', backgroundPosition: 'center'}}>
      <NavBar />
      {PopupChildren && <PopupLayout children={ PopupChildren }/> }
      <MasterGrid />
    </div>
  )
}

export default MasterLayout;