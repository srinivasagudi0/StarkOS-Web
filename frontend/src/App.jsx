import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import Home from './Home'
import About from './About'
import { use, useEffect } from 'react'

function App() {
  
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Command Center</Link>{' '}
        <Link to="/about">About</Link>
      </nav>

      <Routes>
        <Route path="/" element={<command_center />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App