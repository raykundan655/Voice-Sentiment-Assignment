🎤 Voice Sentiment Agent (Simple Version)

A lightweight voice sentiment analysis application using FastAPI backend with plain HTML/JavaScript frontend. No React, no Node.js, no build steps - just pure simplicity!

## ✨ Features

- **Single-File Backend**: FastAPI with OpenAI Whisper + Google Gemini
- **Plain HTML/JS Frontend**: No frameworks, no build process
- **Sentiment Analysis**: Get Positive/Negative/Neutral with reasoning
- **Lightweight**: API-based, optimized for Render.com free tier (<512MB RAM)
- **Simple Deployment**: Just 3 files + Dockerfile

## 📁 Project Structure

```
voice-sentiment-simple/
├── main.py                 # FastAPI backend (serves HTML + API)
├── templates/
│   └── index.html         # Plain HTML/JS frontend
├── requirements.txt       # Python dependencies
└── Dockerfile            # For deployment
```

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export OPENAI_API_KEY="your-openai-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
```

On Windows:
```cmd
set OPENAI_API_KEY=your-openai-api-key
set GEMINI_API_KEY=your-gemini-api-key
```

3. **Run the server:**
```bash
python main.py
```

4. **Open your browser:**
```
http://localhost:8000
```

That's it! No npm install, no build steps, no complex setup.

## 🌐 Deploy to Render.com

### Method 1: Using Dockerfile (Recommended)

1. **Create a new Web Service** on [Render.com](https://dashboard.render.com/)
2. **Connect your GitHub repository**
3. **Configure settings:**
   - **Environment**: Docker
   - **Region**: Choose closest to you
   - **Instance Type**: Free (512MB RAM)
   - **Dockerfile Path**: `./Dockerfile` (if in root) or leave default

4. **Add environment variables:**
   ```
   OPENAI_API_KEY = sk-...
   GEMINI_API_KEY = AI...
   ```

5. **Deploy!**

### Method 2: Direct Python Deploy

If you prefer not to use Docker:

1. **Build Command:**
```bash
pip install -r requirements.txt
```

2. **Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Add environment variables** (same as above)

## 🔑 Getting API Keys

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AI`)

## 📊 How It Works

```
User clicks "Record"
        ↓
Browser captures audio (MediaRecorder API)
        ↓
User clicks "Stop"
        ↓
Audio blob sent to /analyze endpoint
        ↓
Backend receives audio
        ↓
OpenAI Whisper transcribes to text
        ↓
Google Gemini analyzes sentiment + gives reason
        ↓
Result returned to frontend
        ↓
Display sentiment with emoji and reasoning
```

## 🎯 API Endpoints

### `GET /`
Serves the main HTML page

### `POST /analyze`
Analyzes sentiment from audio file

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Audio file (WebM format)

**Response:**
```json
{
  "transcription": "I'm having a wonderful day!",
  "sentiment": "Positive",
  "reason": "The speaker expresses enthusiasm and happiness about their day."
}
```

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "openai_configured": true,
  "gemini_configured": true
}
```

## 💰 Cost Estimates

### Render.com
- **Free tier**: 750 hours/month, 512MB RAM
- **Limitation**: Sleeps after 15 min inactivity

### API Costs
- **OpenAI Whisper**: ~$0.006 per minute of audio
- **Google Gemini**: Free tier (60 requests/min)

**Example Monthly Usage:**
- 100 recordings/day × 30 seconds each = 50 minutes/day
- Monthly Whisper cost: ~$9
- Monthly Gemini cost: $0 (free tier)

## 🔧 Customization

### Change Sentiment Prompt

Edit `main.py`, line ~55:

```python
prompt = f"""Analyze the sentiment of this text and provide:
1. The sentiment: Positive, Negative, or Neutral
2. A brief 1-sentence reason for your classification

Text: {transcription}

Respond in this exact format:
Sentiment: [Positive/Negative/Neutral]
Reason: [One sentence explanation]"""
```

### Change UI Colors

Edit `templates/index.html`, look for the style section:

```css
/* Change gradient background */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change button colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add More Sentiment Categories

1. Update the Gemini prompt to include more options
2. Add color mappings in `getSentimentData()` function in `index.html`

## 🐛 Troubleshooting

**Microphone not working:**
- Ensure browser has microphone permissions
- Use HTTPS in production (required for microphone access)
- Check that no other app is using the microphone

**API errors:**
- Verify API keys are set correctly
- Check API key has sufficient credits
- View browser console (F12) for detailed errors

**Render deployment issues:**
- Ensure environment variables are set
- Check logs in Render dashboard
- Verify Dockerfile is in the root directory

**CORS errors:**
- This shouldn't happen since frontend is served from same domain
- If using separate frontend, add CORS middleware

## 📝 File Descriptions

### `main.py`
- FastAPI application
- Serves HTML frontend at `/`
- Handles audio upload at `/analyze`
- Integrates OpenAI Whisper and Google Gemini APIs
- Health check at `/health`

### `templates/index.html`
- Complete HTML/CSS/JS in one file
- MediaRecorder API for audio capture
- Fetch API for backend communication
- Beautiful gradient UI with animations
- Fully responsive design

### `requirements.txt`
- Minimal Python dependencies
- FastAPI for web framework
- OpenAI for Whisper API
- Google GenerativeAI for Gemini
- Uvicorn for ASGI server

### `Dockerfile`
- Python 3.11 slim base image
- Installs dependencies
- Copies application files
- Exposes port 8000
- Runs uvicorn server

## 🎨 Features Highlight

✅ **Zero Build Process** - Just HTML/CSS/JS
✅ **No Node.js Required** - Pure Python backend
✅ **Single Command Deploy** - Docker or direct Python
✅ **Beautiful UI** - Gradient design, smooth animations
✅ **Responsive** - Works on desktop and mobile
✅ **Real-time Feedback** - Loading states, error handling
✅ **Sentiment Reasoning** - Not just label, but why
✅ **Clean Code** - Easy to understand and modify

## 📜 License

MIT License - Use freely!

## 🤝 Contributing

Feel free to open issues or submit pull requests!

---

**Built with ❤️ using FastAPI, OpenAI Whisper, and Google Gemini**