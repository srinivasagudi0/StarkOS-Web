import { useState } from "react";

function MissionForge() {
  const [input, setInput] = useState("")
  const [result, setResult] = useState("")
  const [loading, setLoading] = useState(false)

  function generateMissions() {
    setLoading(true)

    fetch("/api/ai-forge", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ input: input })
    })
      .then((response) => response.json())
      .then((data) => {
        setResult(data.message)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
        setResult("Something went wrong.")
      })
  }

  return (
    <main>
      <br />

      <div className="title3">
        <h1>Mission Forge</h1>
      </div>

      <br />

      <div className="forge-text1">
        <h2>Beta: Quick Add (with AI)</h2>

        <div className="card advice-card">
          <p>
            Enter a brief description of your mission(s). AI will generate one or more mission suggestions.
          </p>

          <textarea
            className="mission-input"
            placeholder="Enter your mission description here..."
            value={input}
            onChange={(event) => setInput(event.target.value)}
          ></textarea>

          <button className="mission-button" onClick={generateMissions}>
            Generate Missions
          </button>

          {loading && <p>Generating missions...</p>}

          {result && (
            <pre>{result}</pre>
          )}
        </div>

        <br />
      </div>
    </main>
  )
}

export default MissionForge;

