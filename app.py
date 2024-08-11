import openai
import requests

# Set up your OpenAI API key
openai.api_key = "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"

# ML API URL
ml_api_url = "https://sklearn-xyz-ppml.onrender.com/predict"

def get_product_info(product_name):
    try:
        # Send the request with the original product name
        response = requests.post(ml_api_url, json={"product_name": product_name})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Log the entire response for debugging
        print("Debug: API response:", data)
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"error": "Error fetching product details"}

def generate_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or any other engine you prefer
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "Sorry, I couldn't generate a response at the moment."

def chat():
    print("Chatbot: Hello, how may I help you today?")

    while True:
        user_input = input("You: ").strip()

        if "hello" in user_input.lower() or "hey" in user_input.lower():
            print("Chatbot: Hello, how may I help you today?")
        
        elif "tell me something about" in user_input.lower():
            product_name = user_input.replace("tell me something about", "").strip()
            if product_name:
                print(f"Sending request to ML API: {ml_api_url} with data: {{'product_name': '{product_name}'}}")
                product_info = get_product_info(product_name)
                if "error" in product_info:
                    print("Chatbot:", product_info["error"])
                else:
                    # Check if the expected keys are in the response
                    if all(key in product_info for key in ["product_name", "product_url", "MRP", "discounted_price", "average_predicted_price", "advice_message"]):
                        # Display the detailed information received from the API
                        print(f"Chatbot: Product Name: {product_info['product_name']}")
                        print(f"        Product URL: {product_info['product_url']}")
                        print(f"        MRP: {product_info['MRP']}")
                        print(f"        Discounted Price: {product_info['discounted_price']}")
                        print(f"        Average Predicted Price: {product_info['average_predicted_price']}")
                        print(f"        Advice: {product_info['advice_message']}")
                    else:
                        print("Chatbot: The API response is missing some information.")
            else:
                print("Chatbot: Please specify a product name.")
        
        elif user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        
        else:
            # Generate an OpenAI-based response for unrecognized inputs
            openai_response = generate_openai_response(user_input)
            print(f"Chatbot: {openai_response}")

# Start the chatbot
if __name__ == "__main__":
    chat()
