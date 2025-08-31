import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from flasgger import Swagger, swag_from
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")
genai.configure(api_key=GEMINI_API_KEY)
app = Flask(__name__)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
origins_list = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]
CORS(app, resources={r"/api/*": {"origins": origins_list}})

app.config['SWAGGER'] = {
    "title": "LLM Q&A API",
    "uiversion": 3
}
    
swagger = Swagger(app)
@app.route("/api/health", methods=["GET"])
@swag_from({
    "tags": ["Health"],
    "summary": "Health check endpoint",
    "responses": {
        200: {
            "description": "Returns OK status",
            "content": {
                "application/json": {
                    "example": {"status": "ok"}
                }
            }
        }
    }
})
def health():
    return jsonify({"status": "ok"})


@app.route("/api/ask", methods=["POST"])
@swag_from({
    "tags": ["Q&A"],
    "summary": "Ask a question to Gemini LLM",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "example": "What documents do I need to travel from Kenya to Ireland?"}
                    },
                    "required": ["question"]
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "AI-generated response",
            "content": {
                "application/json": {
                    "example": {
                        "answer": "### Required documents\n- Passport ...",
                        "model": "gemini-pro"
                    }
                }
            }
        },
        400: {
            "description": "Invalid input"
        },
        500: {
            "description": "Server error"
        }
    }
})
def ask():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question'"}), 400
    question = data["question"].strip()
    if not question:
        return jsonify({"error": "Question is empty"}), 400
    system_prompt = (
        "You are a helpful assistant. Provide structured answers with clear sections like:\n"
        "- Required documents\n"
        "- Passport requirements\n"
        "- Additional notes\n"
        "- Travel advisories\n"
    )
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(f"{system_prompt}\nUser Question: {question}")
        answer = response.text.strip() if response and response.text else "No response generated."
        return jsonify({"answer": answer, "model": MODEL})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
