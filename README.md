# MediChatAI Fullstack Medical Assistant

 MediChatAIAI is a fullstack AI-powered health assistant built using FastAPI for the backend and React for the frontend. It uses Google's Gemini Pro (via LangChain), LangGraph, and Tavily Search to analyze patient symptoms and provide AI-generated medical insights.

---

## 🧠 Features

- Describe symptoms and get diagnosis
- AI-generated medicine recommendations
- Precautions and side-effects
- Self-care advice
- Suggestion to consult a real doctor when necessary
- Real-time chat UI

---

## 🗂️ Project Structure

project/
├── backend/
│ ├── backend.py
│ ├── requirements.txt
│ └── .env
└── frontend/
├── public/
├── src/
├── package.json
└── .env (optional)


cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt


GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key

to run backend
uvicorn backend:app --reload

to run frontend
npm run dev   # or npm start depending on setup



