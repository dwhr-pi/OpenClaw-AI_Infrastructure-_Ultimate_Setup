"""Proxy example source for a separately reviewed image; never started by setup."""
import hmac
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 65536

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL")
GEMINI_MODEL = os.environ["GEMINI_MODEL"]
PROXY_AUTH_TOKEN = os.environ["PROXY_AUTH_TOKEN"]
if len(PROXY_AUTH_TOKEN) < 32 or not GEMINI_API_KEY:
    raise RuntimeError("Proxy requires separately provisioned credentials")

@app.before_request
def authorize():
    supplied = request.headers.get("Authorization", "")
    expected = "Bearer " + PROXY_AUTH_TOKEN
    if not hmac.compare_digest(supplied.encode("utf-8"), expected.encode("utf-8")):
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/generate", methods=["POST"])
def generate():
    body = request.get_json(silent=True)
    prompt = body.get("prompt") if isinstance(body, dict) else None
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 16000:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # Versuch, Gemini zu nutzen
        gemini_headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
        gemini_payload = {"contents": [{"parts": [{"text": prompt}]}]}
        gemini_response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
            headers=gemini_headers,
            json=gemini_payload,
            timeout=10
        )
        gemini_response.raise_for_status()
        gemini_data = gemini_response.json()
        if gemini_data and "candidates" in gemini_data and gemini_data["candidates"]:
            return jsonify({"text": gemini_data["candidates"][0]["content"]["parts"][0]["text"]})

    except (requests.exceptions.RequestException, KeyError, ValueError, IndexError, TypeError):
        app.logger.warning("Gemini request failed; no request or credential details logged")
        # Fallback auf Ollama
        if OLLAMA_URL:
            try:
                ollama_payload = {"model": "llama3.2:1b", "prompt": prompt, "stream": False}
                ollama_response = requests.post(f"{OLLAMA_URL}/api/generate", json=ollama_payload, timeout=30)
                ollama_response.raise_for_status()
                ollama_data = ollama_response.json()
                return jsonify({"text": ollama_data["response"]})
            except (requests.exceptions.RequestException, ValueError, KeyError):
                app.logger.warning("Ollama request failed; no request details logged")
                return jsonify({"error": "Beide LLM-Anbieter sind nicht erreichbar."}), 500
        else:
            return jsonify({"error": "Gemini fehlgeschlagen und Ollama-URL nicht konfiguriert."}), 500

    return jsonify({"error": "Unbekannter Fehler bei der LLM-Generierung."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
