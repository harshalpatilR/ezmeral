import gradio as gr
import requests
import json

# --- Core API Logic ---
def call_llm_api(api_url, api_key, prompt, payload_str):
    """
    Constructs the request and calls the LLM API.

    Args:
        api_url (str): The URL of the LLM API endpoint.
        api_key (str): The API key for authentication.
        prompt (str): The user's prompt.
        payload_str (str): A JSON string representing the request body.

    Returns:
        str: The response text from the LLM or an error message.
    """
     # Sanitize inputs
    if not api_url or not api_key or not prompt:
        return "Please fill in the API URL, API Key, and Prompt."

    try:
        # Replace the <prompt> placeholder with the actual prompt
        modified_payload_str = payload_str.replace("<prompt>", prompt)
        
        print(modified_payload_str)
        # Load the user's modified JSON payload
        payload = json.loads(modified_payload_str)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}" # Or check API documentation for correct header
        }

        # Make the API call
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response
        llm_response = response.json()
        
        # Assuming the response has a similar structure, extract the text
        return f"Response: {json.dumps(llm_response, indent=2)}"

    except json.JSONDecodeError:
        return "Error: Invalid JSON payload. Please check your syntax."
    except requests.exceptions.RequestException as e:
        return f"API Call Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Gradio UI Setup ---

# A standard JSON payload for a hypothetical LLM API
DEFAULT_PAYLOAD = json.dumps(

  {"model": "meta/llama-3.1-8b-instruct", "messages":[{"role": "user", "content": "<prompt>"}]}
  , indent=2
)

# Define the Gradio interface
iface = gr.Interface(
    fn=call_llm_api,
    inputs=[
        gr.Textbox(label="API URL", placeholder="e.g., https://api.llm.com/v1/models/gemini:generateContent"),
        gr.Textbox(label="API Key", type="password", placeholder="Paste your API key here"),
        gr.Textbox(label="Prompt", placeholder="Enter your prompt here..."),
        gr.Textbox(label="JSON Payload (Editable)", lines=10, value=DEFAULT_PAYLOAD)
    ],
    outputs=gr.Textbox(label="LLM Response", lines=20),
    title="Simple LLM API Client",
    description="Enter your API details and prompt to interact with an LLM. You can also modify the JSON payload for advanced settings."
)

# Launch the app
iface.launch(share=False, server_name="0.0.0.0")