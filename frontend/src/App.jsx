import { useState } from 'react'
import './App.css'
import MasterLayout from './layouts/mainComponents/MasterLayout'
import LoginRegister from './loginRegister/LoginRegister'
import { Routes, Route, Outlet } from 'react-router-dom'

function App() {

  const [popup, setPopup] = useState(null)
  
  return (
    <>
        <Routes>
          <Route path="/" element={ <MasterLayout popupChildren={<Outlet context={[popup, setPopup]} /> } setPopup={setPopup} /> } >
            <Route path="/login" element={ <LoginRegister formName="login" /> } />
            <Route path="/register" element={ <LoginRegister formName="register" /> } />
          </Route>
        </Routes>
    </>
  )
}

export default App