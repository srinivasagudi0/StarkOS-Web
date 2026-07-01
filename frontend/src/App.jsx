import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import CommandCenter from './command_center'
import MissionControl from './mission_control'
import MissionForge from './mission_forge'
//import MissionTracker from './mission_tracker'


function App() {

  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Command Center</Link>
        <Link to="/mission-control">Mission Control</Link>

        <Link to="/missions-forge">Mission Forge</Link>
      </nav>

      <Routes>
        <Route path="/" element={<CommandCenter />} />
        <Route path="/mission-control" element={<MissionControl />} />
        <Route path="/missions-forge" element={<MissionForge />} />
        
      </Routes>
    </BrowserRouter>
  )
}

export default App;