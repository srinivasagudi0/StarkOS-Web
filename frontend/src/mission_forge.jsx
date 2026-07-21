import { useState } from "react";

function MissionForge() {
  const [input, setInput] = useState("")
  const [result, setResult] = useState("")
  const [plan, setPlan] = useState(null)
  const [error, setError] = useState("")
  const [showCustomAdd, setShowCustomAdd] = useState(false)
  const [loading, setLoading] = useState(false)
  const [dailyInput, setDailyInput] = useState("")
  const [weeklyInput, setWeeklyInput] = useState("")
  const [longTermInput, setLongTermInput] = useState("")
  const [lastAddedAt, setLastAddedAt] = useState(() => (
    localStorage.getItem("lastMissionAddedAt") || ""
  ))

  function getCurrentTime() {
    return new Date().toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit",
    })
  }

  function saveLastAddedTime() {
    const time = getCurrentTime()
    localStorage.setItem("lastMissionAddedAt", time)
    setLastAddedAt(time)
  }

  async function generateMissions() {
    if (!input.trim()) {
      setError("Tell me what you want to accomplish first.")
      return
    }

    setLoading(true)
    setError("")
    setResult("")
    setPlan(null)

    try {
      const response = await fetch('/api/ai-forge', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      })

      const data = await response.json()
      setResult(data.message)

      if (typeof data.plan === "string") {
        setPlan(JSON.parse(data.plan))
      } else {
        setPlan(data.plan)
      }
    } catch {
      setError("I couldn't build your plan. Check that the app is connected and try again.")
    }

    setLoading(false)
  }

  function clearForge() {
    setInput("")
    setResult("")
    setPlan(null)
    setError("")
  }

  async function applyPlan() {
    const response = await fetch('/api/apply_plan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        daily: plan.daily || [],
        weekly: plan.weekly || [],
        long_term: plan.long_term || [],
      }),
    })

    const data = await response.json()
    setResult(data.message)

    if (response.ok) {
      saveLastAddedTime()
    }
  }

  async function addCustomMission(type, value) {
    const response = await fetch(`/api/add_${type}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [type]: value }),
    })

    const data = await response.json()
    setResult(data.message)

    if (response.ok) {
      saveLastAddedTime()
    }
  }

  return (
    <main className="page forge-page">
      <div className="title3">
        <h1>Mission Forge</h1>
        <p className="greeting">Turn what you want to do into a plan you can actually follow.</p>
      </div>

        
        <section className="forge-text1"> 
        <br />
        <div className="card advice-card forge-panel featured-card">

            <h1>✨ Quick Add with AI</h1>


          <p>Tell me what you want to work on, and I'll break it into missions you can follow.</p>

          <textarea
            className="mission-input"
            placeholder="Example: I want to get better at React and fitness."
            value={input}
            onChange={(event) => setInput(event.target.value)}
          />

          <div className="forge-actions">
            <button className="mission-button" onClick={generateMissions} disabled={loading}>
              {loading ? "Building your plan..." : "Generate Missions"}
            </button>

            <button className="mission-button secondary-button" onClick={clearForge}>
              Start over
            </button>

            {plan && (
              <button className="mission-button" onClick={applyPlan}>
                Add this plan to Mission Control
              </button>
            )}
          </div>

          {error && <p className="forge-error">{error}</p>}

          {loading && (
            <div className="forge-loading">
              <div className="loader"></div>
              <p>Putting your plan together...</p>
            </div>
          )}

          {result && (
            <div className="forge-result">
              <h3>Your plan</h3>
              <pre>{result}</pre>
            </div>
          )}

        </div>
        <button className="mission-button" onClick={() => setShowCustomAdd(!showCustomAdd)}>
          {showCustomAdd ? "Hide Custom Add ⬆" : "Show Custom Add ⬇"}
        </button>
        
         {showCustomAdd && (
  <div className="custom-add">
    <h1>Custom Add</h1>

    <div className="card-rows">
      <div className="card mission-card forge small-card">
        <div className="custom-mission-header">
          <span className="custom-mission-icon">🧩</span>
          <h3>Daily Mission</h3>
        </div>
        <p>Add one thing you want to finish today.</p>
        <textarea placeholder="What do you want to finish today?" value={dailyInput} onChange={(event) => setDailyInput(event.target.value)} />
        <button className="mission-button" onClick={() => addCustomMission("daily", dailyInput)}>Add Daily Mission</button>
      </div>
          <br />
      <div className="card mission-card forge small-card">
        <div className="custom-mission-header">
          <span className="custom-mission-icon">📅</span>
          <h3>Weekly Mission</h3>
        </div>
        <p style={{ color: 'rgb(184, 83, 184)' }}>Add something you want to make progress on this week.</p>
        <textarea placeholder="What do you want to make progress on this week?" value={weeklyInput} onChange={(event) => setWeeklyInput(event.target.value)} />
        <button className="mission-button" onClick={() => addCustomMission("weekly", weeklyInput)}>Add Weekly Mission</button>
      </div>
          <br />
      <div className="card mission-card forge small-card">
        <div className="custom-mission-header">
          <span className="custom-mission-icon">🎯</span>
          <h3>Long-term Mission</h3>
        </div>
        <p style={{ color: 'orange' }}>Add a bigger goal you want to keep moving toward.</p>
        <textarea placeholder="What are you working toward?" value={longTermInput} onChange={(event) => setLongTermInput(event.target.value)} />
        <button className="mission-button" onClick={() => addCustomMission("long_term", longTermInput)}>Add Long-term Mission</button>
      </div>
    </div>
  </div>
)}
      </section>

        {lastAddedAt && <p className="personalize">Last mission added at {lastAddedAt}</p>}
    </main>
  )
}

export default MissionForge;

// testin before submission
