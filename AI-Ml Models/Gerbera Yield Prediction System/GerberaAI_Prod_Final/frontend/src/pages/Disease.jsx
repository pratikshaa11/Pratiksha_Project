import React, {useState} from "react";
import axios from "axios";
const API = "http://127.0.0.1:8000";

function speak(text, lang="mr-IN"){ if(window.speechSynthesis){ const ut=new SpeechSynthesisUtterance(text); ut.lang=lang; window.speechSynthesis.cancel(); window.speechSynthesis.speak(ut);} }

export default function Disease(){
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  async function detect(){
    if(!file) return alert("Choose a file");
    const fd = new FormData();
    fd.append("file", file);
    setResult({loading:true});
    try{
      const res = await axios.post(API + "/predict/disease", fd, { headers:{ "Content-Type":"multipart/form-data" } });
      setResult(res.data);
    }catch(e){
      setResult({error:"Server or network error"});
    }
  }

  return (
    <div style={{maxWidth:1000}}>
      <div style={{display:"flex", alignItems:"center", gap:12, marginBottom:12}}>
        <img src="/images/gerbera_banner.png" alt="gerbera" style={{height:80}}/>
        <div>
          <h2 style={{margin:0}}>Disease Detection</h2>
          <div style={{color:"#666"}}>Upload clear photos of flowers/leaves (multiple angles give better results).</div>
        </div>
      </div>
      <div style={{background:"#fff", padding:12, borderRadius:8}}>
        <div style={{display:"flex", gap:12, alignItems:"center"}}>
          <input type="file" accept="image/*" onChange={e=>setFile(e.target.files[0])} />
          <button onClick={detect}>Detect</button>
        </div>
        <div style={{marginTop:12}}>
          {!result && <div>No result yet.</div>}
          {result && result.loading && <div>Loading…</div>}
          {result && result.prediction && (
            <div>
              <div style={{display:"flex", alignItems:"center", gap:8}}>
                <div style={{fontSize:20,fontWeight:700}}>{result.prediction}</div>
                <div style={{color:"#666"}}>({Math.round(result.confidence*100)}%)</div>
              </div>
              <div style={{marginTop:8}}>
                <h4>Treatment steps</h4>
                <ol>
                  {result.advice.map((a,i)=> <li key={i}>{a}</li>)}
                </ol>
                <button onClick={()=>speak(result.advice.join(". "))}>🔊 Read advice</button>
              </div>
            </div>
          )}
          {result && result.error && <div style={{color:"red"}}>{result.error}</div>}
        </div>
      </div>
    </div>
  )
}