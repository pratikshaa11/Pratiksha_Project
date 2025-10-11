import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Disease from "./pages/Disease";
import Advisory from "./pages/Advisory";
import Market from "./pages/Market";
import Notifications from "./pages/Notifications";
import Chat from "./pages/Chat";

const headerTop = { background:"#f5f2ed", padding:6, fontSize:12, color:"#333", display:"flex", justifyContent:"space-between", alignItems:"center" }
const headerMain = { background:"#e9e6df", padding:"14px 20px", display:"flex", alignItems:"center", gap:12 }
const logo = { fontSize:20, fontWeight:700 }

const sidebar = { width:220, background:"#2f3940", color:"white", minHeight:"80vh", padding:12 }

export default function App(){
  return (
    <div>
      <div style={headerTop}>
        <div>GerberaAI - Farmer assistant for Maharashtra</div>
        <div style={{fontSize:13}}>Local advisory • Market trends</div>
      </div>
      <div style={headerMain}>
        <div style={logo}>🌼 GerberaAI</div>
        <div style={{marginLeft:10, color:"#666"}}>Localized for Maharashtra</div>
      </div>
      <div style={{display:"flex"}}>
        <div style={sidebar}>
          <div style={{fontSize:18, marginBottom:12}}>Menu</div>
          <div style={{display:"flex", flexDirection:"column", gap:8}}>
            <Link to="/" style={{color:"white", textDecoration:"none"}}>Dashboard</Link>
            <Link to="/disease" style={{color:"white", textDecoration:"none"}}>Disease Detection</Link>
            <Link to="/advisory" style={{color:"white", textDecoration:"none"}}>Advisory</Link>
            <Link to="/market" style={{color:"white", textDecoration:"none"}}>Market Trends</Link>
            <Link to="/notifications" style={{color:"white", textDecoration:"none"}}>Notifications</Link>
            <Link to="/chat" style={{color:"white", textDecoration:"none"}}>Chatbot</Link>
          </div>
        </div>
        <div style={{flex:1, padding:20}}>
          <Routes>
            <Route path="/" element={<Home/>} />
            <Route path="/disease" element={<Disease/>} />
            <Route path="/advisory" element={<Advisory/>} />
            <Route path="/market" element={<Market/>} />
            <Route path="/notifications" element={<Notifications/>} />
            <Route path="/chat" element={<Chat/>} />
          </Routes>
        </div>
      </div>
    </div>
  )
}