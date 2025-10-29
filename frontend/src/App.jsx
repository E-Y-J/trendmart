import { useState } from 'react'
import './App.css'
import MasterLayout from './layouts/mainComponents/MasterLayout'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom'

function App() {
  const [popup, setPopup] = useState(null)
  console.log(Link, useNavigate, useLocation)
  
  return (
    <>
      <MasterLayout popupChildren={ popup } setPopup={ setPopup } />
    </>
  )
}

export default App