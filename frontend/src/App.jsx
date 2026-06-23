import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import CommandCenter from './command_center'
import MissionControl from './mission_control'
import About from './About'


function App() {

  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Command Center</Link>
        <Link to="/mission-control">Mission Control</Link>

        <Link to="/about">About</Link>
      </nav>

      <Routes>
        <Route path="/" element={<CommandCenter />} />
        <Route path="/mission-control" element={<MissionControl />} />
        <Route path="/about" element={<About />} />
        
      </Routes>
    </BrowserRouter>
  )
}

export default App