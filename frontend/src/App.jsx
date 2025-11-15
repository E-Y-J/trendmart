import { useState } from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import MasterLayout from '@main/MasterLayout';
import LoginRegister from '@children/popupLayoutChildren/loginRegister/LoginRegister';
import FocusedProduct from '@children/popupLayoutChildren/focusedProduct/FocusedProduct';
import Profile from '@children/popupLayoutChildren/profileSettingsCompanyInfo/Profile';
import ProtectedURLs from '@children/securityWrapper/ProtectedURLs';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [popup, setPopup] = useState(null);

  return (
    <>
      <Routes>
        <Route
          path="/"
          element={
            <MasterLayout
              popupChildren={<Outlet context={[popup, setPopup]} />}
              setPopup={setPopup}
            />
          }
        >
          <Route
            path="/login"
            element={<LoginRegister />}
          />
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
          <Route element={<ProtectedURLs />}>
            <Route
              path="/profile"
              element={<Profile />}
            />
          </Route>
        </Route>
      </Routes>
    </>
  );
}

export default App;
