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

  async function generateMissions() {
    if (!input.trim()) {
      setError("Enter a mission idea first.")
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
      setError("Something went wrong. Make sure Flask is running.")
    }

    setLoading(false)
  }

  function clearForge() {
    setInput("")
    setResult("")
    setPlan(null)
    setError("")
  }

  function applyPlan() {
    fetch('/api/apply_plan', {
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
      .then((response) => response.json())
      .then((data) => {
        setResult(data.message)
      })
  }

  function addCustomMission(type, value) {
    fetch(`/api/add_${type}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [type]: value }),
    })
      .then((response) => response.json())
      .then((data) => setResult(data.message))
  }

  return (
    <main className="page forge-page">
      <div className="title3">
        <h1>Mission Forge</h1>
        <p>Create missions that help you achieve long-term goals.</p>
      </div>

        
        <section className="forge-text1"> 
        <br />
        <div className="card advice-card forge-panel">

            <h1>✨ Quick Add with AI</h1>


          <p>Describe your goal very clearly. AI will turn it into missions.</p>

          <textarea
            className="mission-input"
            placeholder="Example: I want to get better at React and fitness."
            value={input}
            onChange={(event) => setInput(event.target.value)}
          />

          <div className="forge-actions">
            <button className="mission-button" onClick={generateMissions} disabled={loading}>
              {loading ? "Generating..." : "Generate Missions"}
            </button>

            <button className="mission-button secondary-button" onClick={clearForge}>
              Clear
            </button>

            {plan && (
              <button className="mission-button" onClick={applyPlan}>
                Apply to Mission Control
              </button>
            )}
          </div>

          {error && <p className="forge-error">{error}</p>}

          {loading && (
            <div className="forge-loading">
              <div className="loader"></div>
              <p>Forging your mission plan...</p>
            </div>
          )}

          {result && (
            <div className="forge-result">
              <h3>Generated Mission Plan</h3>
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
      <div className="card mission-card forge">
        <div className="custom-mission-header">
          <span className="custom-mission-icon">🧩</span>
          <h3>Daily Mission</h3>
        </div>
        <p>Enter a daily mission to add to your plan.</p>
        <textarea placeholder="Daily mission" value={dailyInput} onChange={(event) => setDailyInput(event.target.value)} />
        <button className="mission-button" onClick={() => addCustomMission("daily", dailyInput)}>Add Daily Mission</button>
      </div>
          <br />
      <div className="card mission-card forge">
        <div className="custom-mission-header">
          <span className="custom-mission-icon">📅</span>
          <h3>Weekly Mission</h3>
        </div>
        <p style={{ color: 'rgb(184, 83, 184)' }}>Enter a weekly mission to add to your plan.</p>
        <textarea placeholder="Weekly mission" value={weeklyInput} onChange={(event) => setWeeklyInput(event.target.value)} />
        <button className="mission-button" onClick={() => addCustomMission("weekly", weeklyInput)}>Add Weekly Mission</button>
      </div>
          <br />
      <div className="card mission-card forge">
        <div className="custom-mission-header">
          <span className="custom-mission-icon">🎯</span>
          <h3>Long-term Mission</h3>
        </div>
        <p style={{ color: 'orange' }}>Enter a long-term mission to add to your plan.</p>
        <textarea placeholder="Long-term mission" value={longTermInput} onChange={(event) => setLongTermInput(event.target.value)} />
        <button className="mission-button" onClick={() => addCustomMission("long_term", longTermInput)}>Add Long-term Mission</button>
      </div>
    </div>
  </div>
)}
      </section>
    </main>
  )
}

export default MissionForge;

// testin before submission