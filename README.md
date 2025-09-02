# AgentZeroo Backend

This is the backend service for **AgentZeroo**, built with FastAPI, the OpenAI Agents SDK, and Supabase for session management. The app streams markdown responses in real-time and is containerized with Docker for easy deployment.

---

## 🚀 Features

- **FastAPI**-based API for handling agent queries
- **Streaming Responses**: Real-time markdown streaming with proper handling of partial chunks
- **Supabase Session Management**
- **Dockerized** for cloud deployments (e.g., Koyeb)
- **CORS Enabled**: Ready to be consumed by a React frontend

---

## 📦 Project Structure

```
.
├── main.py               # FastAPI entrypoint
├── agent.py              # AgentZero definition
├── utils/config.py       # Utils
├── supabase_session.py   # Supabase session handler
├── pyproject.toml        # Dependencies (uv project)
├── uv.lock               # Lockfile (optional)
├── Dockerfile            # Container build file
├── .env                  # Environment variables (not committed)
└── README.md             # Project documentation
```

---

## 🛠 Requirements

- **Python**: >=3.12
- **uv**: Dependency manager ([astral.sh/uv](https://astral.sh/uv))
- **Docker** (optional, for containerized runs)

---

## ⚡ Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/ehtashamtoor/AgentZeroUsingSDK.git
cd AgentZeroUsingSDK
```

### 2. Install dependencies (with `uv`)

```bash
uv pip install --system --no-cache .
```

### 3. Start the FastAPI server

```bash
uv run python main.py
```

The API will be available at:

```
http://127.0.0.1:8000/docs
```

---

## 🐳 Running with Docker

### 1. Build the Docker image

```bash
docker build -t agentzero-backend .
```

### 2. Run the container

```bash
docker run -it --rm -p 8000:8000 agentzero-backend
```

Now the API is available at:

```
http://localhost:8000/docs
```

---

## 🔧 Environment Variables

Make sure to configure these in your `.env` file:

```env
HOST=0.0.0.0
PORT=8000
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_api_key
model=gemini-2.5-flash(in my case)
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

---

## 📡 API Endpoints

### Health Check

```
GET /system-health
```

Response:

```json
{
  "status": "System is online"
}
```

### Ask AgentZero

```
GET /ask-AgentZero?question=Your+question&session_id=123
```

Response: **EventStream (text/event-stream)**

- Streams markdown chunks as they are generated
- Ends with `[DONE]`

---

---

## 👤 Author

Built by **Ehtasham Toor**

