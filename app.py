from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
import uvicorn
import os
from collections import defaultdict

app = FastAPI(
    title="People Counting API",
    description="FastAPI service for people detection using YOLOv8",
    version="1.0.0"
)

# 🔹 Load YOLO model (your best.pt file)
model = YOLO("best.pt")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>People Counting API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            form { margin-top: 20px; }
            input[type="file"] { margin: 10px 0; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            button:hover { background: #0056b3; }
            #result { margin-top: 20px; padding: 10px; border: 1px solid #ddd; background: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Welcome to the People Counting API</h1>
        <p>Upload an image or video to detect and count people using YOLOv8.</p>
        <form action="/predict" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*,video/*" required>
            <br>
            <button type="submit">Detect People</button>
        </form>
        <div id="result"></div>
    </body>
    </html>
    """

@app.post("/predict", response_class=HTMLResponse)
async def predict(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()

    if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # Video processing
        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        with open(temp_input.name, 'wb') as f:
            f.write(contents)

        cap = cv2.VideoCapture(temp_input.name)
        if not cap.isOpened():
            return "<h1>Error: Could not open video file</h1>"

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output.name, fourcc, fps, (width, height))

        person_id = 0
        track_history = defaultdict(lambda: [])

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLO detection
            results = model(frame, classes=[0], conf=0.4)[0]
            detections = len(results.boxes)

            # Annotate frame with IDs and count
            annotated_frame = results.plot()
            cv2.putText(annotated_frame, f"People Count: {detections}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Simple ID assignment (for demo - in real tracking, use proper tracking)
            for i, box in enumerate(results.boxes):
                x1, y1, x2, y2 = box.xyxy[0]
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                cv2.putText(annotated_frame, f"ID: {i+1}", (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            out.write(annotated_frame)

        cap.release()
        out.release()
        os.unlink(temp_input.name)

        filename = os.path.basename(temp_output.name)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Video People Detection Result</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                video {{ max-width: 100%; height: auto; margin-top: 20px; }}
                a {{ color: #007bff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>Video People Detection Result</h1>
            <p><strong>Annotated video:</strong> <a href="/video/{filename}">Download Video</a></p>
            <video controls>
                <source src="/video/{filename}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <br><br>
            <a href="/">Upload another file</a>
        </body>
        </html>
        """

    else:
        # Image processing
        npimg = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Run YOLO detection (only 'person' class)
        results = model(frame, classes=[0], conf=0.4)[0]
        detections = len(results.boxes)

        # Draw boxes and save annotated output
        annotated = results.plot()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(temp_file.name, annotated)

        filename = os.path.basename(temp_file.name)
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>People Detection Result</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                img {{ max-width: 100%; height: auto; margin-top: 20px; }}
                a {{ color: #007bff; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>People Detection Result</h1>
            <p><strong>Total people detected:</strong> {detections}</p>
            <p><strong>Annotated image:</strong> <a href="/image/{filename}">View Image</a></p>
            <img src="/image/{filename}" alt="Annotated Image">
            <br><br>
            <a href="/">Upload another file</a>
        </body>
        </html>
        """

@app.get("/image/{filename}")
async def get_image(filename: str):
    file_path = f"C:\\Users\\SHREE\\AppData\\Local\\Temp\\{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='image/jpeg')
    return {"error": "Image not found"}

@app.get("/video/{filename}")
async def get_video(filename: str):
    file_path = f"C:\\Users\\SHREE\\AppData\\Local\\Temp\\{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='video/mp4')
    return {"error": "Video not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
