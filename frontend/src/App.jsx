import { useState } from 'react'
import './App.css'
import MasterLayout from './layouts/mainComponents/MasterLayout'
import LoginRegister from './layouts/layoutChildren/popupLayoutChildren/loginRegister/LoginRegister'
import { Routes, Route, Outlet } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {

  const [popup, setPopup] = useState(null)
  
  return (
    <>
        <Routes>
          <Route path="/" element={ <MasterLayout popupChildren={<Outlet context={[popup, setPopup]} /> } setPopup={setPopup} /> } >
            <Route path="/login" element={ <LoginRegister /> } />
            <Route path="/register" element={ <LoginRegister /> } />
          </Route>
        </Routes>
    </>
  )
}

export default App