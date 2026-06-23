import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import CommandCenter from './command_center'
import About from './About'
import {useState, useEffect} from 'react'


function App() {
  

  useEffect(() => {
    fetch('/api/command-center').then(res => res.json()).then(data => setMissionData(data));
  }, []);

  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Command Center</Link>

        <Link to="/about">About</Link>
      </nav>

      <Routes>
        <Route path="/" element={<CommandCenter />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App