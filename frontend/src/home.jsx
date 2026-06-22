import { useEffect, useState } from 'react'

function Home() {
  const [message, setMessage] = useState('Loading...')

  useEffect(() => {
    fetch('/api/hello')
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage('Could not connect to Flask'))
  }, [])

  return (
    <main>
      <h1>Home Page</h1>
      <p>Flask says: {message}</p>
    </main>
  )
}

export default Home;
