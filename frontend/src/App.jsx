import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import CommandCenter from './command_center'
import MissionControl from './mission_control'
import MissionForge from './mission_forge'
//import MissionTracker from './mission_tracker'
import Code from './coding'
import About from './About'


function App() {

  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Command Center</Link>
        <Link to="/mission-control">Mission Control</Link>
        <Link to="/missions-forge">Mission Forge</Link>
        <Link to="/coding">Coding Intelligence</Link>
        <Link to="/About">About</Link>
      </nav>

      <Routes>
        <Route path="/" element={<CommandCenter />} />
        <Route path="/mission-control" element={<MissionControl />} />
        <Route path="/missions-forge" element={<MissionForge />} />
        <Route path="/coding" element={<Code />} />
        <Route path="/About" element={<About />} />
        
      </Routes>
    </BrowserRouter>
  )
}

export default App;
