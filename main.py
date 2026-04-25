from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import google.generativeai as genai
import os
import tempfile
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = FastAPI(title="Voice Sentiment Agent")

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r") as f:
        return f.read()

@app.post("/analyze")
async def analyze_sentiment(audio: UploadFile = File(...)):
    try:
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
            content = await audio.read()
            temp_audio.write(content)
            temp_audio_path = temp_audio.name
        
        try:
            # Read audio bytes
            with open(temp_audio_path, "rb") as f:
                audio_bytes = f.read()
                
            response = gemini_model.generate_content([
                """Transcribe this audio and analyze sentiment.

Return EXACTLY in this format:
Sentiment: Positive/Negative/Neutral
Reason: one short sentence
Transcription: exact spoken text
""",
                {
                    "mime_type": "audio/webm",
                    "data": audio_bytes
                }
            ])

            response_text = (response.text or "").strip()

            # Default values
            transcription = ""
            sentiment = "Neutral"
            reason = "Unable to determine sentiment."

            # Parse response
            for line in response_text.split("\n"):
                if line.startswith("Sentiment:"):
                    sentiment_raw = line.replace("Sentiment:", "").strip()
                    if "Positive" in sentiment_raw:
                        sentiment = "Positive"
                    elif "Negative" in sentiment_raw:
                        sentiment = "Negative"
                elif line.startswith("Reason:"):
                    reason = line.replace("Reason:", "").strip()
                elif line.startswith("Transcription:"):
                    transcription = line.replace("Transcription:", "").strip()

            # Handle empty transcription
            if not transcription:
                return JSONResponse(
                    status_code=200,
                    content={
                        "transcription": "",
                        "sentiment": "Neutral",
                        "reason": "No speech detected in the recording."
                    }
                )

            return JSONResponse(
                status_code=200,
                content={
                    "transcription": transcription,
                    "sentiment": sentiment,
                    "reason": reason
                }
            )
            
        finally:
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
                
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)