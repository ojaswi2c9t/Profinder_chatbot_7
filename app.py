from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up your OpenAI API key
openai.api_key = "your_openai_api_key"

# ML API URL
ml_api_url = "https://sklearn-xyz-ppml.onrender.com/predict"

# Session data storage
session_data = {}

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if "hello" in user_input.lower() or "hey" in user_input.lower():
        return jsonify({"reply": "Hello! How can I assist you today?"})
    
    elif "tell me something about" in user_input.lower():
        product_name = user_input.replace("tell me something about", "").strip()
        if product_name:
            session_data['last_product'] = product_name
            product_info = get_product_info(product_name)
            if "error" in product_info:
                return jsonify({"reply": product_info["error"]})
            else:
                if all(key in product_info for key in ["product_name", "product_url", "MRP", "discounted_price", "average_predicted_price", "advice_message"]):
                    session_data['product_info'] = product_info
                    bot_response = (
                        f"<b>Product Name:</b> {product_info['product_name']}<br>"
                        f"<b>Product URL:</b> <a href='{product_info['product_url']}'>{product_info['product_url']}</a><br>"
                        f"<b>MRP:</b> {product_info['MRP']}<br>"
                        f"<b>Discounted Price:</b> {product_info['discounted_price']}<br>"
                        f"<b>Average Predicted Price:</b> {product_info['average_predicted_price']}<br>"
                        f"<b>Advice:</b> {product_info['advice_message']}"
                    )
                    return jsonify({"reply": bot_response})
                else:
                    return jsonify({"reply": "The API response is missing some information."})
        else:
            return jsonify({"reply": "Please specify a product name."})
    
    elif "what was the last product" in user_input.lower():
        if 'last_product' in session_data:
            return jsonify({"reply": f"The last product you asked about was '{session_data['last_product']}'."})
        else:
            return jsonify({"reply": "You haven't asked about any products yet."})
    
    elif user_input.lower() in ["exit", "quit"]:
        return jsonify({"reply": "Goodbye!"})
    
    else:
        openai_response = generate_openai_response(user_input)
        return jsonify({"reply": openai_response})


def get_product_info(product_name):
    try:
        response = requests.post(ml_api_url, json={"product_name": product_name})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"An error occurred while fetching product details: {str(e)}"}

def generate_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
