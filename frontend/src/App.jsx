import { useState } from "react";
import { Routes, Route, Outlet } from "react-router-dom";
import MasterLayout from "./layouts/mainComponents/MasterLayout";
import LoginRegister from "./layouts/layoutChildren/popupLayoutChildren/loginRegister/LoginRegister";
import FocusedProduct from "./layouts/layoutChildren/popupLayoutChildren/focusedProduct/FocusedProduct";
import Profile from "./layouts/layoutChildren/popupLayoutChildren/profileSettingsCompanyInfo/Profile";
import ProtectedURLs from './layouts/layoutChildren/securityWrapper/ProtectedURLs'
// import Profile from './layouts/layoutChildren/popupLayoutChildren/profileSettingsCompanyInfo/Profile'
// import ProtectedURLs from './access/ProtectedURLs'
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

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
              setPopup={ setPopup }
            />
          }
        >
          <Route path="/login" element={<LoginRegister />} />
          <Route path="/product" element={<FocusedProduct />} />
          <Route element={ <ProtectedURLs /> } >
            <Route path="/profile" element={ <Profile /> } />
          </Route>
        </Route>
      </Routes>
    </>
  );
}

export default App;
