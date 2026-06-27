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

  if (loading) {
    return <div>Loading...</div>
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
          <h3>XP Points: {missionData.XP_points}</h3>
        </div>

        <div className="card">
          <div className="mission-icon">🔥</div>
          <h3>Streaks: {missionData.streaks}</h3>
        </div>

        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">🛠️</div>
            <h2>Failed Recovery</h2>
          </div>
          <ul>
            {missionData.failed_missions.map((mission) => (
              <li>{mission}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}

export default MissionControl
