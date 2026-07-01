import { useState } from "react";

function MissionForge() {
  const [input, setInput] = useState("")
  const [result, setResult] = useState("")
  const [plan, setPlan] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

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
      const response = await fetch("/api/ai-forge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      })

      const data = await response.json()
      setResult(data.message)

      try {
        setPlan(JSON.parse(data.message))
      } catch {
        setPlan(null)
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
        daily: plan.daily?.[0] || '',
        weekly: plan.weekly?.[0] || '',
        long_term: plan.long_term?.[0] || '',
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.message)
      })
  }

  return (
    <main className="forge-page">
      <div className="title3">
        <h1>Mission Forge</h1>
      </div>

      <section className="forge-text1">
        <h1>Beta: Quick Add with AI</h1>

        <div className="card advice-card forge-panel">
          <p>Describe your goal. AI will turn it into missions.</p>

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
      </section>
    </main>
  )
}

export default MissionForge;
