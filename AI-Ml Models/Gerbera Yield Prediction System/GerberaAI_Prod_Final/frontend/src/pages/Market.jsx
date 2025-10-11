import React,{useEffect,useState} from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
export default function Market(){
  const [data,setData]=useState([]);
  useEffect(()=>{ fetch("http://127.0.0.1:8000/market-data").then(r=>r.json()).then(j=>setData(j.series || [])) },[]);
  return (
    <div style={{maxWidth:900, background:"#fff", padding:12, borderRadius:8}}>
      <h2>Market Trends - Pune (sample)</h2>
      <div style={{height:300}}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="date"/><YAxis/><Tooltip/><Line type="monotone" dataKey="price" stroke="#2f8f6d" /></LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}