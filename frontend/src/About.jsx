function About() {
  return (
    <main className="page about-page">
      <div className="title4">
        <h1>About StarkOS</h1>
      </div>

      <section className="about-hero">
        <p className="about-kicker">Made for staying focused and keeping your momentum.</p>
        <h2>One place to see your work and know what to do next.</h2>
        <p>
          StarkOS keeps your coding time, missions, streaks, warnings, and daily
          advice in one place. Open it when you sit down to work and you'll know
          where you stand and what to tackle next.
        </p>
      </section>

      <section className="about-panel featured-card">
        <h2>Why I built StarkOS</h2>
        <p>
          I made StarkOS because I wanted one simple place to see my coding life.
          I was tired of switching between tools just to check my hours, tasks,
          and progress. The JARVIS idea from Iron Man inspired me to make
          something that feels like a small personal assistant for staying on track.
        </p>
      </section>

      <section className="about-grid">
        <div className="about-card small-card">
          <span>🛰️</span>
          <h3>Command Center</h3>
          <p>
            See today's coding time, missions, warnings, streak, focus, energy,
            and advice at a glance.
          </p>
        </div>

        <div className="about-card small-card">
          <span>🎯</span>
          <h3>Mission Control</h3>
          <p>
            Plan your day, your week, and bigger goals. Complete missions, earn XP,
            and recover when a day doesn't go to plan.
          </p>
        </div>

        <div className="about-card small-card">
          <span>⚒️</span>
          <h3>Mission Forge</h3>
          <p>
            Turn a rough idea into a mission plan with AI, or add each mission
            yourself.
          </p>
        </div>
      </section>

      <section className="about-panel">
        <h2>How StarkOS works</h2>

        <div className="about-steps">
          <div>
            <strong>1</strong>
            <p>Flask keeps your mission data organized behind the scenes.</p>
          </div>

          <div>
            <strong>2</strong>
            <p>React turns that data into the cards you use every day.</p>
          </div>

          <div>
            <strong>3</strong>
            <p>Hackatime connects your real coding activity to the dashboard.</p>
          </div>
        </div>
      </section>

      <section className="about-developer featured-card">
        <div className="developer-avatar">👨‍💻</div>

        <div>
          <p className="about-kicker">A little about me</p>
          <h2>Built by Srinivas</h2>
          <p>
            I'm building StarkOS while learning full-stack development. It lets
            me practice React, Flask, APIs, databases, OAuth, and UI design while
            making something I actually want to use. If you're curious about a
            feature, the README explains how it works.
          </p>
          <p>
            I wanted this to feel like a command center for my own progress:
            useful, personal, and a little futuristic. Each page has a job - track
            the work, plan the next mission, recover from a miss, and keep moving.
          </p>
          <p>
            Next, I want to keep growing StarkOS and make it even more useful for developers. I'd also love feedback from users and
            hackers about features, ideas, or bugs. You can find me on Slack at
            srinivasagudi0.
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
