import { useEffect, useState } from 'react'

function CommandCenter() {
  const [CommandData, setCommandData] = useState([])
  const [loading, setLoading] = useState(true)

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

  const [missionData, setMissionData] = useState({
  daily_missions: [],
  weekly_missions: [],
  long_term_goals: [],
  })
  
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

  const [warnings, setWarnings] = useState([])

  useEffect(() => {
    fetch('/api/warnings')
      .then((response) => response.json())
      .then((data) => {
        setWarnings(JSON.parse(data.message))
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div>Loading...</div>
  }
// i am doing code hours peer day because i always do like 4 hrs for each day consistently unlike do as much as possible or less than 4hrs.
    return (
      <div className="cmd-center-txt">
        <br />
        <div className="title">

        <h1>Command Center</h1>
        </div>  

        <br />
        <div className="cards-row">
          <div className="card">
              <div className='mission-icon'>⏱️</div>

            <div className="content">
              <h4>Code Hours (Yesterday)</h4>

              <div className="stats">
                <span className="number">{CommandData.code_hours}</span>
                <span className="label">Hours</span>
              </div>
            </div>
          </div>

          <div className="card mission-card">
            <div className="mission-header">
              <div className="mission-icon">🎯</div>
              <h2>Missions</h2>
            </div>
            <ul>
              {missionData.daily_missions.map((mission) => (
                <li key={mission}>{mission}</li>
              ))}

              {missionData.weekly_missions
                .map((mission) => (
                  <li key={mission}>{mission}</li>
                ))}

              {missionData.long_term_goals
              .map((missions) => (
                <li key={missions}>{missions}</li>
              ))}


              </ul>
            
          </div>
          <div className="card mission-card">
            <div className="mission-header">
              <div className="mission-icon">🔺</div>
              <h2>Warnings</h2>
            </div>
            <ul>
              <div className="warning">
              {warnings.map((warnings) => (
                <li key={warnings}>{warnings}</li>
              ))}
              </div>

        </ul>
          </div>
            </div>
        <br/>
        <div className="cards-row bottom-cards">
        <div className="card">
          <div className="mission-icon">🔥</div>
          <h3>Streaks : {CommandData.streaks}</h3>
          </div>
       <div className="card">
        <div className="mission-icon">🧠</div>
        <h3>Focus Score: {CommandData.focus_score}</h3>
        </div>
        <div className="card">
          <div className="mission-icon">⚡</div>
        <h3>Energy Score: {CommandData.energy_score}</h3>
        </div>
        
        </div>
        <div className="card advice-card">
          <div className="mission-header">
            <div className="mission-icon">💡</div>
            <h2>Daily Advice</h2>
          </div>

          <ul>
            {CommandData.daily_advice.map((advice) => (
              <li>{advice}</li>
            ))}
          </ul>
        </div>
      </div>
    )
}
export default CommandCenter;

// done!!