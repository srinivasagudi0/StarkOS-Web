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
        <Link className="nav-brand" to="/" aria-label="StarkOS home">
          <svg
            className="stark-logo-mark"
            viewBox="0 0 40 40"
            role="img"
            aria-label="StarkOS logo"
          >
            <path d="M20 3 34.5 11.5v17L20 37 5.5 28.5v-17Z" />
            <circle cx="20" cy="20" r="7" />
            <path className="logo-core" d="m20 13 5.8 10H14.2Z" />
          </svg>
          <span className="nav-wordmark">
            STARKOS
          </span>
        </Link>
        <Link to="/">Command Center</Link>
        <Link to="/mission-control">Mission Control</Link>
        <Link to="/missions-forge">Mission Forge</Link>
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
