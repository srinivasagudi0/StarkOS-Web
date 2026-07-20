function About() {
  return (
    <main className="page about-page">
      <div className="title4">
        <h1>About StarkOS</h1>
      </div>

      <section className="about-hero">
        <p className="about-kicker">Built for focus, missions, and momentum</p>
        <h2>A personal dashboard for staying locked in.</h2>
        <p>
          StarkOS helps you see your coding hours, missions, streaks, warnings,
          and daily advice without jumping between a bunch of different tools.
          The goal is simple: open one page and know what to work on next.
        </p>
      </section>

      <section className="about-panel featured-card">
        <h2>Why I built StarkOS</h2>
        <p>
         I built StarkOS because I wanted a simple, personal dashboard to track my coding hours, missions, streaks, and daily advice. I was tired of jumping between different tools and wanted one place to see everything at a glance. The goal is to help you stay focused, organized, and motivated on your coding journey.
         I also got inspired by the idea of JARVIS from Iron Man, and wanted to create a personal assistant that could help me stay on track with my coding goals.
        </p>
      </section>

      <section className="about-grid">
        <div className="about-card small-card">
          <span>🛰️</span>
          <h3>Command Center</h3>
          <p>
            Shows daily coding hours, active missions, warnings, streaks,
            focus score, energy score, and daily advice.
          </p>
        </div>

        <div className="about-card small-card">
          <span>🎯</span>
          <h3>Mission Control</h3>
          <p>
            Organizes daily missions, weekly missions, long-term goals, XP,
            streaks, and failed mission recovery.
          </p>
        </div>

        <div className="about-card small-card">
          <span>⚒️</span>
          <h3>Mission Forge</h3>
          <p>
            Lets you create missions manually or generate a simple plan with AI,
            then apply it to Mission Control.
          </p>
        </div>
      </section>

      <section className="about-panel">
        <h2>How StarkOS works</h2>

        <div className="about-steps">
          <div>
            <strong>1</strong>
            <p>Flask stores and sends your mission data through API routes.</p>
          </div>

          <div>
            <strong>2</strong>
            <p>React fetches that data and turns it into dashboard cards.</p>
          </div>

          <div>
            <strong>3</strong>
            <p>Hackatime can connect with OAuth to show real coding activity.</p>
          </div>
        </div>
      </section>

      <section className="about-developer featured-card">
        <div className="developer-avatar">👨‍💻</div>

        <div>
          <p className="about-kicker">About Developer</p>
          <h2>Made by Srinivas</h2>
          <p>
            I built StarkOS while learning full-stack development. This project
            is my way of practicing React, Flask, APIs, databases, OAuth, and
            clean UI design while making something I would actually use. Also If you have any
            questions about how each features works, it is listed in the README of the repo.
          </p>
          <p>
            I wanted the app to feel like a command center for my own progress:
            simple, useful, and a little futuristic. Every page is part of that
            idea — track the work, plan the mission, recover from mistakes, and
            keep improving.
          </p>
          <p>
            If my work gets approved by hack club, I plan to add more features
            and make this project, like a flagship, for my portfolio. I also want you guys (users/hackers)
            to give me feedback on what you want to see in the app or any bugs you find. You can reach me in
            slack at 'srinivasagudi0'.
          </p>
          <h1>Hope you guys like it!</h1>
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
