import { useState, useEffect } from 'react'


function Code() {
    const [hackatimeConnected, setHackatimeConnected] = useState(false)
  const [hours, setHours] = useState(null)
  useEffect(() => {
  fetch('/api/hackatime/hours', {
    credentials: 'include',
  })
    .then((response) => response.json())
    .then((data) => {
      setHackatimeConnected(data.connected)
      if (data.connected) {
        setHours(data.hours)
      }
    })
}, [])

    const [streak, setStreak] = useState(null)
    useEffect(() => {
        fetch('/api/hackatime/streak', {
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.connected) {
                    setStreak(data.streak)
                }   
        })
    })

    return (
        <main>
            <h1 className="title5">Coding Intelligence</h1>
            <div className="cards-row">
                <div className="card">
                    <div className='mission-icon'>⏱️</div>
                    <div className="content">
                        <h1>Coded Hours</h1>
                        <div className="stats">
                            <span className="number">
                                {hours}
                            </span>
                            <span className="label">Hours</span>
                        </div>
                    </div>
                </div>
                <div className="card">
                    <div className='mission-icon'>🎯</div>
                    <div className="content">
                        <h1>Streak</h1>
                        <div className="stats">
                            <span className="number">
                                {streak}
                            </span>
                            <span className="label">Days</span>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    )
}

export default Code;