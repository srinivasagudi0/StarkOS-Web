import { useEffect, useState } from 'react'

function MissionControl() {
  const [missionData, setMissionData] = useState({
    daily_missions: [],
    weekly_missions: [],
    long_term_goals: [],
    XP_points: 0,
    streaks: 0,
    failed_missions: [],
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/mission-control')
      .then((response) => response.json())
      .then((data) => {
        setMissionData(data)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  const [CommandData, setCommandData] = useState([])


  useEffect(() => {
    fetch('/api/command-center')
      .then((response) => response.json())
      .then((data) => {
        setCommandData(data)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  const [recovery, setRecovery] = useState('')

  useEffect(() => {
    fetch('/api/recovery-assistant')
        .then((response) => response.json())
        .then((data) => {
            setRecovery(data) // its just full explantion
            setLoading(false)
        })
        .catch(() => {
            setLoading(false)
        })
    }, [])

  if (loading) {
    return <div>Loading...</div>
  }

  const xpPoints = (CommandData.focus_score + CommandData.energy_score ) / (CommandData.code_hours || 1) * 10

  return (
    <div className="mission-control-text">
      <div className="title">
        <h1>Mission Control</h1>
      </div>

      <br />

      <div className="cards-row">
        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">🎯</div>
            <h2>Daily Missions</h2>
          </div>
          <ul>
            {missionData.daily_missions.map((mission) => (
              <li>{mission}</li>
            ))}
          </ul>
        </div>

        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">📅</div>
            <h2>Weekly Missions</h2>
          </div>
          <ul>
            {missionData.weekly_missions.map((mission) => (
              <li>{mission}</li>
            ))}
          </ul>
        </div>

        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">🚀</div>
            <h2>Long-Term Goals</h2>
          </div>
          <ul>
            {missionData.long_term_goals.map((goal) => (
              <li>{goal}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="cards-row">
        <div className="card">
          <div className="mission-icon">⭐</div>
          <h3>XP Points: {xpPoints.toFixed(2)}pts</h3>
        </div>

        <div className="card">
          <div className="mission-icon">🔥</div>
          <h3>Streaks: {CommandData.streaks}</h3>
        </div>

        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">🛠️</div>
            <h2>Failed Mission</h2>
          </div>
          <ul>
            {missionData.failed_missions.map((mission) => (
              <li>{mission}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className='card mission-card'>
        <div className="mission-header">
          <div className="mission-icon">💡</div>
          <h2>Failed Mission Recovery</h2>
        </div>
        <p>{recovery.message}</p>
      </div>
    </div>

  )
}


export default MissionControl
