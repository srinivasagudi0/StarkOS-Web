import { useEffect, useState } from 'react'

function MissionControl() {
  const [missionData, setMissionData] = useState({
    daily_missions: [],
    weekly_missions: [],
    long_term_goals: [],
    legacy_daily_missions: [],
    legacy_weekly_missions: [],
    legacy_long_term_goals: [],
    daily_mission_items: [],
    weekly_mission_items: [],
    long_term_goal_items: [],
    XP_points: 0,
    streaks: 0,
    failed_missions: [],
    failed_mission_items: [],
    failed_count: 0,
    completed_count: 0,
  })
  const [missionLoading, setMissionLoading] = useState(true)
  const [missionMessage, setMissionMessage] = useState("")

  function loadMissionData() {
    setMissionLoading(true)
    fetch('/api/mission-control')
      .then((response) => response.json())
      .then((data) => {
        setMissionData(data)
        setMissionLoading(false)
      })
      .catch(() => {
        setMissionLoading(false)
      })
  }

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

  function updateMission(missionId, action) {
    fetch(`/api/missions/${missionId}/${action}`, {
      method: 'POST',
    })
      .then((response) => response.json())
      .then((data) => {
        setMissionMessage(data.message)
        loadMissionData()
      })
      .catch(() => {
        setMissionMessage("Could not update mission.")
      })
  }

  function renderMissionList(items = [], legacyItems = [], emptyMessage) {
    if (items.length === 0 && legacyItems.length === 0) {
      return <li>{emptyMessage}</li>
    }

    return (
      <>
        {legacyItems.map((mission, index) => (
          <li key={`legacy-${index}`}>{mission}</li>
        ))}

        {items.map((mission) => (
          <li className="mission-action-item" key={mission.id}>
            <span>{mission.title}</span>

            <div className="mission-actions">
              <button onClick={() => updateMission(mission.id, 'complete')}>Complete</button>
              <button onClick={() => updateMission(mission.id, 'fail')}>Fail</button>
              <button onClick={() => updateMission(mission.id, 'delete')}>Delete</button>
            </div>
          </li>
        ))}
      </>
    )
  }

  function renderFailedMissions() {
    const realFailedMissions = missionData.failed_mission_items || []
    const realFailedTitles = realFailedMissions.map((mission) => mission.title)
    const legacyFailedMissions = missionData.failed_missions.filter(
      (mission) => !realFailedTitles.includes(mission)
    )

    if (realFailedMissions.length === 0 && legacyFailedMissions.length === 0) {
      return <li>No failed missions.</li>
    }

    return (
      <>
        {legacyFailedMissions.map((mission, index) => (
          <li key={`failed-legacy-${index}`}>{mission}</li>
        ))}

        {realFailedMissions.map((mission) => (
          <li className="mission-action-item" key={mission.id}>
            <span>{mission.title}</span>

            <div className="mission-actions">
              <button onClick={() => updateMission(mission.id, 'recover')}>Recover</button>
              <button onClick={() => updateMission(mission.id, 'delete')}>Delete</button>
            </div>
          </li>
        ))}
      </>
    )
  }


  const [streak, setStreak] = useState(null)

  useEffect(() => {
    fetch('/api/hackatime/streak')
      .then((response) => response.json())
      .then((data) => {
        setStreak(data.streak)
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


  if (missionLoading || recoveryLoading) {
    return (
      <div className="loading-screen">
        <div className="loader"></div>
        <p>Loading StarkOS...</p>
      </div>

    )


  }

  return (
    <div className="mission-control-text">
      <br />
      <div className="title2">
        <h1>Mission Control</h1>
      </div>

      <br />

      {missionMessage && <p className="mission-message">{missionMessage}</p>}

      <div className="cards-row">
        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">🎯</div>
            <h2>Daily Missions</h2>
          </div>
          <ul>
            {renderMissionList(
              missionData.daily_mission_items,
              missionData.legacy_daily_missions,
              "No daily missions available."
            )}
          </ul>
        </div>

        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">📅</div>
            <h2>Weekly Missions</h2>
          </div>
          <ul>
            {renderMissionList(
              missionData.weekly_mission_items,
              missionData.legacy_weekly_missions,
              "No weekly missions available."
            )}
          </ul>
        </div>

        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">🚀</div>
            <h2>Long-Term Goals</h2>
          </div>
          <ul>
            {renderMissionList(
              missionData.long_term_goal_items,
              missionData.legacy_long_term_goals,
              "No long-term goals available."
            )}
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
          <div className="number">{streak}</div>
          <p>day(s)</p>
        </div>

        <div className="card mission-card">
          <div className="mission-header">
            <div className="mission-icon">🛠️</div>
            <h2>Failed Mission: {missionData.failed_count}</h2> 
          </div>
          <ul>
            {renderFailedMissions()}
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

export default MissionControl;
