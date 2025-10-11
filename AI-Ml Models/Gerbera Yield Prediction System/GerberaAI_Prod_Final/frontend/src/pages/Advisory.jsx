import React,{useEffect,useState} from "react";
export default function Advisory(){
  const [data,setData]=useState(null);
  useEffect(()=>{ fetch("/data/maharashtra_advisory.json").then(r=>r.json()).then(setData) },[]);
  return (
    <div style={{maxWidth:900, background:"#fff", padding:12, borderRadius:8}}>
      <h2>Localized Advisory - Maharashtra</h2>
      {data && (<div><h4>General</h4><ul>{data.general.map((g,i)=><li key={i}>{g}</li>)}</ul><h4>Soil & Bed</h4><ul>{data.soil_bed_advice.map((s,i)=><li key={i}>{s}</li>)}</ul></div>)}
    </div>
  )
}