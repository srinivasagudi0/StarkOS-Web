import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import CommandCenter from './command_center'
import About from './About'


function App() {
  
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