function About() {
  return (
    <main className="page about-page">
      <div className="title4">
        <h1>About StarkOS</h1>
      </div>

      <section className="about-hero">
        <p className="about-kicker">Stay focused. Keep moving.</p>
        <h2>See your work in one place.</h2>
        <p>
          StarkOS shows your coding time, missions, streak, and progress.
        </p>
      </section>

      <section className="about-panel featured-card">
        <h2>Why I built StarkOS</h2>
        <p>
          I wanted one place for my coding work. Iron Man inspired the design.
          I built StarkOS to help me stay on track.
        </p>
      </section>

      <section className="about-grid">
        <div className="about-card small-card">
          <h3>Command Center</h3>
          <p>See your coding stats and missions.</p>
        </div>

        <div className="about-card small-card">
          <h3>Mission Control</h3>
          <p>Plan, finish, and recover missions.</p>
        </div>

        <div className="about-card small-card">
          <h3>Mission Forge</h3>
          <p>Turn an idea into a mission plan.</p>
        </div>
      </section>

      <section className="about-panel">
        <h2>How StarkOS works</h2>

        <div className="about-steps">
          <div>
            <strong>1</strong>
            <p>Flask stores your mission data.</p>
          </div>

          <div>
            <strong>2</strong>
            <p>React displays the app.</p>
          </div>

          <div>
            <strong>3</strong>
            <p>Hackatime provides your coding stats.</p>
          </div>
        </div>
      </section>

      <section className="about-developer featured-card">
        <div className="developer-avatar">SG</div>

        <div>
          <p className="about-kicker">A little about me</p>
          <h2>Built by Srinivas</h2>
          <p>
            I built StarkOS while learning React and Flask. It is my first full-stack app.
          </p>
          <p>
            I wanted it to feel personal and a little futuristic. Each page has one job.
          </p>
          <p>
            I want to keep improving StarkOS. You can find me on Slack at srinivasagudi0.
          </p>
          <h1>I hope StarkOS helps you keep moving.</h1>
        </div>
      </section>

      <section className="about-panel featured-card">
        <h2>Built with</h2>

        <div className="about-tags">
          <button>React</button>
          <button>Flask</button>
          <button>SQLite</button>
          <button>Vite</button>
          <button>Hackatime OAuth</button>
          <button>OpenAI API</button>
        </div>
      </section>
    </main>
  )
}

export default About;
