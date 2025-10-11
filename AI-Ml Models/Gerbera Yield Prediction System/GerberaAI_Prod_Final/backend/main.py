from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os, io, json, requests, time
from PIL import Image
import numpy as np

app = FastAPI(title="GerberaAI - Backend (final)")
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

# Load keys from env or .env if available
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", None)
# Knowledge base
KB_PATH = "./data/gerbera_knowledge.json"
try:
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        KNOWLEDGE = json.load(f)
except Exception as e:
    KNOWLEDGE = {"greetings": ["Namaste", "Hello"], "facts": []}

TREATMENT_DB = {
  "Powdery Mildew": {"advice":["Remove infected leaves and burn them away from crop","Apply recommended sulfur or potassium bicarbonate spray"], "severity":"medium"},
  "Healthy": {"advice":["Plant appears healthy; continue monitoring"], "severity":"low"},
  "Unknown": {"advice":["Could not identify. Upload more photos or consult local KVK."], "severity":"unknown"}
}

def green_ratio(contents):
    try:
        img = Image.open(io.BytesIO(contents)).convert('RGB').resize((256,256))
        arr = np.array(img)
        r,g,b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
        mask = (g > r) & (g > b) & (g > 100)
        return float(mask.mean())
    except Exception as e:
        return 0.0

@app.post('/predict/disease')
async def predict_disease(file: UploadFile = File(...)):
    contents = await file.read()
    ratio = green_ratio(contents)
    if ratio > 0.12:
        pred='Healthy'; conf=0.9
    else:
        # conservative unknown instead of mislabeling
        pred='Unknown'; conf=0.45 + ratio
    advice = TREATMENT_DB.get(pred, TREATMENT_DB['Unknown'])['advice']
    severity = TREATMENT_DB.get(pred, TREATMENT_DB['Unknown'])['severity']
    return {'prediction':pred,'confidence':round(conf,2),'advice':advice,'severity':severity}

@app.post('/chat')
async def chat(payload: dict):
    """
    Knowledgebase-backed chatbot. Searches simple KB for matching keywords.
    If OPENAI_API_KEY is set, this endpoint could be extended to call OpenAI for more fluent responses.
    """
    msg = payload.get('message','').lower()
    # greetings
    for g in KNOWLEDGE.get('greetings', []):
        if g.lower() in msg:
            return {'reply': f"{g}! I am GerberaAI for Maharashtra. Ask me about diseases, treatment, weather, market prices, or soil."}
    # keyword search in facts
    for fact in KNOWLEDGE.get('facts', []):
        keywords = fact.get('keywords', [])
        for kw in keywords:
            if kw.lower() in msg:
                return {'reply': fact.get('answer')}
    # weather-awareness quick check (uses OpenWeather)
    if 'weather' in msg or 'temperature' in msg or 'climate' in msg:
        if not OPENWEATHER_API_KEY:
            return {'reply': "Weather lookup not configured. Please set OPENWEATHER_API_KEY on the backend host."}
        # try to parse location
        loc = 'Pune,IN'
        parts = msg.split()
        for p in parts:
            if p.endswith(',in') or p.lower() in ['pune','mumbai','nagpur','nashik','aurangabad']:
                loc = p if ',' in p else f"{p.capitalize()},IN"
        q = {"q": loc, "appid": OPENWEATHER_API_KEY, "units":"metric"}
        try:
            r = requests.get("https://api.openweathermap.org/data/2.5/weather", params=q, timeout=10)
            j = r.json()
            temp = j.get('main', {}).get('temp')
            desc = j.get('weather', [{}])[0].get('description', '')
            return {'reply': f"Current weather in {loc}: {temp}°C, {desc}."}
        except Exception as e:
            return {'reply': "Could not fetch weather: " + str(e)}
    return {'reply': "I couldn't find a direct answer in my knowledge base. Try asking about Gerbera care, diseases like 'powdery mildew', or 'market prices'."}

@app.get('/market-data')
def market():
    return {'market':'Pune','series':[{'date':'2025-01','price':12.5},{'date':'2025-02','price':13.0},{'date':'2025-03','price':12.0},{'date':'2025-04','price':14.2}]}

@app.get('/notifications/check')
def notifications_check(location: str = "Pune,IN"):
    if not OPENWEATHER_API_KEY:
        return {'ok':False, 'message':'OPENWEATHER_API_KEY not configured. Set it in environment or .env'}
    # minimal check placeholder
    return {'ok':True, 'message':'Weather notifications enabled (demo)'}