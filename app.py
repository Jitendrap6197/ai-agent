from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

# ✅ Model Name (Ensure it matches `ollama list`)
DEEPSEEK_MODEL_NAME = "deepseek-r1:1.5b"

# ✅ Request schema
class ChatRequest(BaseModel):
    messages: List[str]
    system_prompt: str

@app.post("/chat")
def chat_with_deepseek(request: ChatRequest):
    """
    API Endpoint to communicate with DeepSeek R1 via Ollama.
    """
    try:
        # ✅ Format API request for Ollama
        ollama_payload = {
            "model": DEEPSEEK_MODEL_NAME,
            "prompt": f"{request.system_prompt}\nUser: {request.messages[-1]}\nAI:",
            "stream": False  # Disable streaming
        }

        # ✅ Send request to Ollama's API
        response = requests.post("http://localhost:11434/api/generate", json=ollama_payload)

        # ✅ Handle Response
        if response.status_code == 200:
            ai_response = response.json().get("response", "No response received.")
            return {"messages": [{"type": "ai", "content": ai_response}]}
        else:
            return {"error": f"DeepSeek API Error: {response.status_code} - {response.text}"}

    except Exception as e:
        return {"error": f"Server Error: {str(e)}"}

# ✅ Run FastAPI with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.3", port=8080)
