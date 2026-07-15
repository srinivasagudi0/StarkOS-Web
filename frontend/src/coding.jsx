import { useState, useEffect } from 'react'

function getHeatLevel(hours) {
    if (hours === 0) {
        return 0
    }
    if (hours < 0.5) {
        return 1
    }
    if (hours < 1) {
        return 2
    }
    if (hours < 2) {
        return 3
    }
    if (hours < 3) {
        return 4
    }
    if (hours < 4) {
        return 5
    }
    return 6
}


function Code() {
    const [hours, setHours] = useState(null)
    const [lang, setLang] = useState([])
    const [os, setOS] = useState([])
    useEffect(() => {
        fetch('/api/hackatime/projects', {
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.connected) {
                    setHours(data.data.human_readable_total)
                    setLang(data.languages)
                    setOS(data.operating_systems)
                    
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
    }, [])

    const [goals, setGoals] = useState(null)
    useEffect(() => {
        fetch('/api/hackatime/goals', {
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.connected) {
                    setGoals(data.goal.completion_percent)
                }
            })
    }, [])


    const [goalsText, setGoalsText] = useState(null)
    useEffect(() => {
        fetch('/api/hackatime/goals', {
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.connected) {
                    setGoalsText(data.grand_total?.text || "No goal set")
                }
            })
    }, [])


    const [projects, setProjects] = useState([])
    useEffect(() => {
        fetch('/api/hackatime/projects', {
            credentials: 'include',
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.connected) {
                    setProjects(data.projects)
                }
            })
    }, [])


    const [heatmapDays, setHeatmapDays] = useState([])
    const [heatmapLoading, setHeatmapLoading] = useState(true)
    const [heatmapError, setHeatmapError] = useState("")

   useEffect(() => {
  fetch('/api/hackatime/heatmap', {
    credentials: 'include',
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.connected) {
        setHeatmapDays(Array.isArray(data.days) ? data.days : []);
      } else {
        setHeatmapError(data.message);
      }
      setHeatmapLoading(false);
    })
    .catch(() => {
      setHeatmapError('Failed to fetch heatmap');
      setHeatmapLoading(false);
    });
}, []);
    return (
        <main className="page">
            <h1 className="title5">Coding Intelligence</h1>
            <div className="cards-row">
                <div className="card">
                    <div className='mission-icon'>⏱️</div>
                    <div className="content">
                        <h1>Coded Hours (This week)</h1>
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
                <div className="card">
                    <div className='mission-icon'>🏆</div>
                    <div className="content">
                        <h1>Daily Coding Goal</h1>
                        <div className="stats">
                            <span className="number">
                                {goals ?? 0}%
                            </span>
                            <span className="label">{goalsText}</span>
                        </div>
                    </div>
                </div>

            <div className="mission-card">
                <div className="card">
                <div className="content">
                    <h1>This Week's Projects 📊</h1>
                    <div className="warning">
                    <div className="projects-scroll">
                    <ul>
                        {projects.map((project) => (
                            <li key={project.name}>
                                <strong>{project.name}</strong> - {project.text}
                            </li>
                        ))}
                    </ul>
                    </div>
                    </div>
    
                    
                </div>
                </div>
                </div>
            
            <div className='mission-card'>
                <div className="card">
                <div className="content">
                    <h1>Coding Heatmap</h1>
                    <p>Last 7 Days</p>

                    {heatmapLoading && <p>Loading...</p>}
                    {heatmapError && <p>{heatmapError}</p>}

                    <div className="heatmap-grid">
                        {heatmapDays.map((day) => (
                            <div className="heatmap-day" key={day.date}>
                                <p>{day.day}</p>
                                <div className={`heatmap-cell heat-level-${getHeatLevel(day.hours)}`}></div>
                                <p>{day.hours}h</p>
                            </div>
                        ))}
                    </div>
                </div>
                </div>
            </div>

            <div className='mission-card'>
                <div className="card">
                    <div className='mission-icon'>💻</div>
                    <div className="content">
                        <h1>Languages
                         (top 3)
                            </h1>
                        <ul>
                            {lang.slice(0,3).map((language) => (
                                <li key={language.name}>
                                    <strong>{language.name}</strong>
                                </li>
                            ))}
                        </ul>
                        
                    </div>
                </div>
            </div>
            <br />
            <div className='mission-card'>
                <div className="card">
                    <div className="content">
                        <h1>Operating System</h1>
                        <ul>
                        {os.slice(0, 3).map((system) => (
                            <li key={system.name}>
                            <strong>{system.name}</strong>
                            </li>
                        ))}
                        </ul>
                    </div>
                </div>
            </div>
            </div>

        </main>
    )
}

export default Code;
