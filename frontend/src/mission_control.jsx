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
  const [actionLoading, setActionLoading] = useState(false)

  function loadMissionData(showLoading = true) {
    if (showLoading) setMissionLoading(true)
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

  async function updateMission(missionId, action) {
    try {
      if (action === 'complete') {
        setActionLoading(true)
      }

      const response = await fetch(`/api/missions/${missionId}/${action}`, {
        method: 'POST',
      })
      const data = await response.json()

      setMissionMessage(data.message)

      if (action === 'complete') {
        await new Promise((resolve) => setTimeout(resolve, 500))
      }

      setActionLoading(false)

      loadMissionData(false)
    } catch {
      setActionLoading(false)
      setMissionMessage("That didn't go through. Try it again in a moment.")
    }
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
              <button title="Complete Mission"  onClick={() => updateMission(mission.id, 'complete')}>✓</button>
              <button title="Fail Mission" onClick={() => updateMission(mission.id, 'fail')}>X</button>
              <button title="Delete Mission" className="delete-button" onClick={() => updateMission(mission.id, 'delete')}>
                🗑️
              </button>
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
      return <li>Nothing missed. Nice work!</li>
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
    fetch('/api/hackatime/streak', {
      credentials: 'include',
    })
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


    const [message, setMessage] = useState('')
    useEffect(() => {
        fetch('/api/pages/personalize')
            .then((response) => response.json())
            .then((data) => {
                setMessage(data.message)
            })
    }, [])

    const [count, setCount] = useState(null)
    const [countMessage, setCountMessage] = useState("")
    
    useEffect(() => {
        fetch('/api/mission-control/count')
            .then((response) => response.json())
            .then((data) => {
                setCount(data.count)
                setCountMessage(data.message)
            })
    }, [])

  if (missionLoading || recoveryLoading) {
    return (
      <div className="loading-screen">
        <div className="loader"></div>
        <p>Getting your dashboard ready...</p>
      </div>

    )


  }

  return (
    <main className="page mission-control-text">
      <br />
      <div className="title2">
        <h1>Mission Control</h1>
        <p>{countMessage}</p>
      </div>

      <br />

      {missionMessage && <p className="mission-message">{missionMessage}</p>}

      {actionLoading && (
        <div className="mission-action-loading">
          <div className="loader"></div>
          <span>Updating your mission...</span>
        </div>
      )}

      <div className="cards-row">
        <div className="card mission-card featured-card">
          <div className="mission-header">
            <div className="mission-icon">🎯</div>
            <h2>Daily Missions</h2>
          </div>
          <ul>
            {renderMissionList(
              missionData.daily_mission_items,
              missionData.legacy_daily_missions,
              "Your day is clear - add a mission when you're ready."
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
              "Nothing planned this week yet - add something when you're ready."
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
              "No big goal yet - add one when you know what you're aiming for."
            )}
          </ul>
        </div>
      </div>

      <div className="cards-row">
        <div className="card small-card">
          <div className="mission-icon">⭐</div>
          <ul>
            <div>
              <div className="number">{missionData.XP_points}</div>
              <div className="label">XP</div>
            </div>
          </ul>
        </div>

        <div className="card small-card">
          <div className="mission-icon">🔥</div>
          <h2>Streaks: </h2>
          <div className="number">{streak}</div>
          <div className="label">day(s)</div>
        </div>

        <div className="card mission-card featured-card">
          <div className="mission-header">
            <div className="mission-icon">🛠️</div>
            <h2>Failed Mission: {missionData.failed_count}</h2> 
          </div>
          <ul>
            {renderFailedMissions()}
          </ul>
        </div>
      </div>
      <div className='card mission-card featured-card'>
        <div className="mission-header">
          <div className="mission-icon">💡</div>
          <h2>Failed Mission Recovery</h2>
        </div>
        <ul>
              <li>{recovery.message}</li>

          </ul>
      </div>
      <p className='personalize'>{message}</p>
    </main>
  )
}

export default MissionControl;
