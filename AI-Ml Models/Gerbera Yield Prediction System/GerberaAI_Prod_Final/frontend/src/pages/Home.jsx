import React from "react";
export default function Home(){
  return (
    <div style={{maxWidth:1100}}>
      <h1 style={{marginTop:0}}>Dashboard</h1>
      <p style={{color:"#444"}}>Quick actions: Upload image, view advisories, check market trends, and chat.</p>
      <div style={{display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:12}}>
        <div style={{background:"#fff", padding:12, borderRadius:6}}> <h4>Detect disease</h4> <p>Upload image to detect.</p> </div>
        <div style={{background:"#fff", padding:12, borderRadius:6}}> <h4>Market trends</h4> <p>Recent Pune prices.</p> </div>
        <div style={{background:"#fff", padding:12, borderRadius:6}}> <h4>Notifications</h4> <p>Weather & alerts.</p> </div>
      </div>
    </div>
  )
}