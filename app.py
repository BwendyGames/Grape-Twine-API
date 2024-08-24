from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = Client("hugging-face-space-endpoint-here")

@app.route('/generate', methods=['POST'])
def generate():
    if request.is_json:
        data = request.get_json()
        try:
            message = data.get('message', '')
            system_message = data.get('system_message', '')
            max_tokens = data.get('max_tokens', 512)  # Default to 512
            temperature = data.get('temperature', 0.7)  # Default to 0.7
            top_p = data.get('top_p', 0.95)  # Default to 0.95

            # Log the parameters to see what is being sent
            print(f"Message: {message}")
            print(f"System Message: {system_message}")
            print(f"Max Tokens: {max_tokens}")
            print(f"Temperature: {temperature}")
            print(f"Top P: {top_p}")

            result = client.predict(
                message=message,
                system_message=system_message,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                api_name="/chat"
            )

            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
