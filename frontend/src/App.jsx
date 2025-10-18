import { useState } from 'react'
import './App.css'
import MasterLayout from './layouts/MasterLayout'

function App() {
  const [popup, setPopup] = useState(null)

  return (
    <>
      <MasterLayout popupChildren={popup} setPopup={setPopup} />
    </>
  )
}

export default App
