import { useEffect, useState } from 'react'

function CommandCenter() {
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

  const [missionData, setMissionData] = useState({
  daily_missions: [],
  weekly_missions: [],
  long_term_goals: [],
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

  const [hours, setHours] = useState(0)
  useEffect(() => {
  fetch('/api/hackatime/hours')
    .then((response) => response.json())
    .then((data) => {
      if (data.connected) {
        setHours(data.hours)
      }
    })
}, [])

  const [streak, setStreak] = useState(null)
  useEffect(() => {
  fetch('/api/hackatime/streak')
    .then((response) => response.json())
    .then((data) => {
      if (data.connected) {
        setStreak(data.streak)
      }
    })
}, [])

  const [warnings, setWarnings] = useState([])
  const [warningsLoading, setWarningsLoading] = useState(true)

  useEffect(() => {
    fetch('/api/warnings')
      .then((response) => response.json())
      .then((data) => {
        try {
          setWarnings(JSON.parse(data.message))
        } catch {
          setWarnings([data.message])
        }
        setWarningsLoading(false)
      })
      .catch(() => {
        setWarningsLoading(false)
      })
  }, [])

  const [focus, setFocus] = useState(null)
  useEffect(() => {
    fetch('/api/command-center/focus-score')
      .then((response) => response.json())
      .then((data) => {
        if (data.connected) {
          setFocus(data.focus_score)
        }
      })
      .catch(() => {
        setFocus(0)
      })
  }, [])

  const [energy, setEnergy] = useState(null)
  useEffect(() => {
    fetch('/api/command-center/energy-score')
      .then((response) => response.json())
      .then((data) => {
        if (data.connected) {
          setEnergy(data.energy_score)
        }
      })
      .catch(() => {
        setEnergy(0)
      })
  }, [])

  


  const [advice, setAdvice] = useState([])
  const [adviceLoading, setAdviceLoading] = useState(true)
  
  useEffect(() => {
    fetch ('/api/advice')
      .then((response) => response.json())
      .then((data) => {
        setAdvice(data.message)
        setAdviceLoading(false)
      })
      .catch(() => {
        setAdviceLoading(false)
      })
  }, [])

  if (commandLoading || missionLoading || warningsLoading || adviceLoading) {

    return (
      <div className="loading-screen">
        <div className="loader"></div>
        <p>Loading StarkOS...</p>
      </div>
    )
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
              <h1>Code Hours</h1>
              <div className="stats">
                <span className="number">
                  {hours ?? CommandData.code_hours}
                </span>
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
            {missionData.daily_missions.length === 0 && missionData.weekly_missions.length === 0 && missionData.long_term_goals.length === 0 ? (
                <li>No active missions</li>
              ) : (
                <>
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
                </>
              )}
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
          <h1>Streaks : {streak}</h1>
          </div>
       <div className="card">
        <div className="mission-icon">🧠</div>
        <h1>Focus Score: {focus}</h1>
        </div>
        <div className="card">
          <div className="mission-icon">⚡</div>
        <h3>Energy Score: {energy}</h3>
        </div>
        
        </div>
        <div className="card advice-card">
          <div className="mission-header">
            <div className="mission-icon">💡</div>
            <h2>Daily Advice</h2>
          </div>

          <ul>
            <li>{advice}</li>
          </ul>
          
        </div>
      </div>
    )
}
export default CommandCenter;

// done!!
