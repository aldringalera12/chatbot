# 🎓 PRMSU Chatbot - Minimal Railway Deployment

## 📋 What's Included

This minimal deployment contains only the essential files for Railway:

- ✅ **minimal_fastapi_chatbot.py** - Complete FastAPI chatbot with embedded knowledge
- ✅ **minimal_requirements.txt** - Only essential dependencies (5 packages)
- ✅ **minimal_Dockerfile** - Lightweight Docker configuration
- ✅ **minimal_railway.json** - Railway deployment settings

## 🚀 Deploy to Railway

1. **Create New Project** on [railway.app](https://railway.app)
2. **Deploy from GitHub** → Select this repository
3. **Choose Branch** → `minimal-deployment`
4. **Set Environment Variables:**
   ```
   COHERE_API_KEY=m7uIZhmn9itLRlZmEvHVwIJ6nvJ0FU2zZ5vd40e9
   PORT=8000
   ```
5. **Deploy!** - Should complete in under 2 minutes

## 📱 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /chat` - Main chat endpoint
- `GET /docs` - API documentation

## 🧪 Test Your Deployment

```bash
# Health check
curl https://your-app.railway.app/health

# Test chat
curl -X POST https://your-app.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does PRMSU stand for?"}'
```

## 🎯 Features

- ✅ **PRMSU Validation** - Only answers PRMSU questions
- ✅ **Embedded Knowledge** - No external database needed
- ✅ **User-Friendly Formatting** - Emojis and structured responses
- ✅ **Bypass Prevention** - Rejects non-PRMSU questions
- ✅ **Under 4GB** - Fits Railway's image size limit

## 📊 Knowledge Base

Covers all essential PRMSU topics:
- University information and history
- Admission requirements
- Grading system and honors
- Scholarship requirements
- Uniform policies
- Disciplinary policies
- Student assistant programs
- Cross-enrollment procedures

Ready for your Android app integration! 🚀
