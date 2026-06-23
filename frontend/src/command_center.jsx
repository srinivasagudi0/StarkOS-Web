import { useEffect, useState } from 'react'

function CommandCenter() {
  const [missions, setMissions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/command-center')
      .then((response) => response.json())
      .then((data) => {
        setMissions(data)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div>Loading...</div>
  }
// i am doing code hours peer day because i always do like 4 hrs for each day consistently unlike do as much as possible or less than 4hrs.
    return (
      <div className="cmd-center-txt">
        <h1>Command Center</h1>

        <br />
        <ul>Code Hours: {missions[0].code_hours}</ul>
        <ul>Mission: {missions[0].mission}</ul>
        <ul>Streaks: {missions[0].streaks}</ul>
        <ul>Focus Score: {missions[0].focus_score}</ul>
        <ul>Energy Score: {missions[0].energy_score}</ul>
        <ul>Warnings: {missions[0].warnings}</ul>
        <ul>Daily Goal: {missions[0].daily_advice}</ul>
        
      </div>
    )
}
export default CommandCenter;
