import { useEffect, useState } from 'react'

function CommandCenter() {
  const [missions, setMissions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/command-center')
      .then((response) => response.json())
      .then((data) => {
        setMissions(data)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <p>Loading command center...</p>
  }

  return (
    <main>
      <h1>Command Center</h1>

      <section>
        <h2>Active Missions</h2>

        {missions.length === 0 ? (
          <p>No active missions.</p>
        ) : (
          missions.map((mission) => (
            <article key={mission.id}>
              <h3>{mission.mission}</h3>
              <p>Streak: {mission.streaks}</p>
              <p>XP: {mission.xp_points}</p>
              <p>Focus score: {mission.focus_score}</p>
            </article>
          ))
        )}
      </section>
    </main>
  )
}

export default CommandCenter;