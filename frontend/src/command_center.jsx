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
        <div className="card">
          <div className="icon"></div>

          <div className="content">
            <h4>Code Hours (Yesterday)</h4>

            <div className="stats">
              <span className="number">{CommandData.code_hours}</span>
              <span className="label">Hours</span>
            </div>

          </div>

        </div>

        
        <h2>Missions</h2>
        <ul>
          {CommandData.missions.map((mission) => (
            <li>{mission}</li>
          ))}
        </ul>
        <h3>Streaks: {CommandData.streaks}</h3>
        <h3>Focus Score: {CommandData.focus_score}</h3>
        <h3>Energy Score: {CommandData.energy_score}</h3>
        <h2>Warnings</h2>
        <ul>
          {CommandData.warnings.map((warning) => (
            <li>{warning}</li>
          ))}
        </ul>

        <h2>Daily Advice</h2>
        <ul>
          {CommandData.daily_advice.map((advice) => (
            <li>{advice}</li>
          ))}
        </ul>
        
      </div>
    )
}
export default CommandCenter;
