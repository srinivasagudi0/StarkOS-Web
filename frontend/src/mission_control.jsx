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
  const [missionLoading, setMissionLoading] = useState(true)

  useEffect(() => {
    fetch('/api/mission-control')
      .then((response) => response.json())
      .then((data) => {
        setMissionData(data)
        setMissionLoading(false)
      })
      .catch(() => {
        setMissionLoading(false)
      })
  }, [])

  const [CommandData, setCommandData] = useState([])
  const [commandLoading, setCommandLoading] = useState(true)


  useEffect(() => {
    fetch('/api/command-center')
      .then((response) => response.json())
      .then((data) => {
        setCommandData(data)
        setCommandLoading(false)
      })
      .catch(() => {
        setCommandLoading(false)
      })
  }, [])

  const [recovery, setRecovery] = useState('')
  const [recoveryLoading, setRecoveryLoading] = useState(true)

  useEffect(() => {
    fetch('/api/recovery-assistant')
        .then((response) => response.json())
        .then((data) => {
            setRecovery(data) // its just full explantion
            setRecoveryLoading(false)
        })
        .catch(() => {
            setRecoveryLoading(false)
        })
    }, [])


  if (missionLoading || commandLoading || recoveryLoading) {
    return <div>
      <p>Loading...</p>
      </div>
  }

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
          <ul>
          <div className="number">{missionData.XP_points}pts</div>
          </ul>
        </div>

        <div className="card">
          <div className="mission-icon">🔥</div>
          <h2>Streaks: </h2>
          <div className="number">{CommandData.streaks}</div>
          <p>day(s)</p>
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
        <ul>
              <li>{recovery.message}</li>

          </ul>
      </div>
    </div>

  )
}

export default MissionControl
