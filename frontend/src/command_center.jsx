import { useEffect, useState } from 'react'

function CommandCenter() {
  const [commandData, setCommandData] = useState({
    code_hours: 0,
    missions: [],
    streaks: 0,
    focus_score: 0,
    energy_score: 0,
    warnings: [],
    daily_advice: [],
  })
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
                <span className="number">{commandData.code_hours}</span>
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
              {commandData.missions.map((mission) => (
                <li>{mission}</li>
              ))}
            </ul>
          </div>
          <div className="card mission-card">
            <div className="mission-header">
              <div className="mission-icon">🔺</div>
              <h2>Warnings</h2>
            </div>
            <ul>
          {commandData.warnings.map((warning) => (
            <li>{warning}</li>
          ))}
        </ul>
          </div>
            </div>
        <br/>
        <div className="cards-row bottom-cards">
        <div className="card">
          <div className="mission-icon">🔥</div>
          <h3>Streaks : {commandData.streaks}</h3>
          </div>
       <div className="card">
        <div className="mission-icon">🧠</div>
        <h3>Focus Score: {commandData.focus_score}</h3>
        </div>
        <div className="card">
          <div className="mission-icon">⚡</div>
        <h3>Energy Score: {commandData.energy_score}</h3>
        </div>
        
        </div>
        <div className="card advice-card">
          <div className="mission-header">
            <div className="mission-icon">💡</div>
            <h2>Daily Advice</h2>
          </div>

          <ul>
            {commandData.daily_advice.map((advice) => (
              <li>{advice}</li>
            ))}
          </ul>
        </div>
      </div>
    )
}
export default CommandCenter;

// done!!
