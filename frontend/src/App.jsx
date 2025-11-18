import { Routes, Route, Outlet } from 'react-router-dom';
import MasterLayout from '@main/MasterLayout';
import FocusedProduct from '@children/popupLayoutChildren/focusedProduct/FocusedProduct';
import Profile from '@children/popupLayoutChildren/profileSettingsCompanyInfo/Profile';
import ProtectedURLs from '@children/securityWrapper/ProtectedURLs';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react';
import StyleGuide from '@styles/StyleGuide';

function App() {
  const [popup, setPopup] = useState(null);

  return (
    <>
      <Routes>
        <Route path='/styleguide' element={<StyleGuide/>}/>
        <Route
          path="/"
          element={<MasterLayout state={{popup, setPopup}} />}
        >
          <Route
            path="/product/:int"
            element={
              <FocusedProduct
                onAddToCart={null}
                onBuyNow={null}
                onWishlist={null}
                onMoreLikeThis={null}
                onClose={null}
              /> }
          />
          
          {/* <Route element={<ProtectedURLs />}> */}
            <Route
              path="/profile"
              element={<Profile />}
            />
          {/* </Route> */}
        </Route>
      </Routes>
    </>
  );
}

export default App;
