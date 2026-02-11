"""
Pablosi Embedding Server
Fast HTTP server using SentenceTransformers with model loaded in memory
"""

from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load model once at startup
logging.info("Loading Pablosi model...")
model = SentenceTransformer("pablosi/bge-m3-spa-law-qa-trained-2")
logging.info("Model loaded successfully!")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model": "pablosi/bge-m3-spa-law-qa-trained-2"})

@app.route('/embed', methods=['POST'])
def embed():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "text is required"}), 400
        
        # Generate embedding
        embedding = model.encode([text])[0].tolist()
        
        return jsonify({"embedding": embedding})
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on localhost:5001
    app.run(host='127.0.0.1', port=5001, debug=False)
