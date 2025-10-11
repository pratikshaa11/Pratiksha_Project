import React,{useState} from "react";
export default function Notifications(){ const [note,setNote]=useState(null);
async function check(){ const r=await fetch("http://127.0.0.1:8000/notifications/check"); const j=await r.json(); setNote(j); }
return (<div style={{maxWidth:900}}><h2>Notifications</h2><p>Weather notifications (demo). Set OPENWEATHER_API_KEY in backend to enable.</p><button onClick={check}>Check Now</button>{note && <pre>{JSON.stringify(note,null,2)}</pre>}</div>); }