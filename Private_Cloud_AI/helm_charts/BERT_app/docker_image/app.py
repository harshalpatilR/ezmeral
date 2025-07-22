import gradio as gr
from transformers import pipeline
import sys
import io
import torch # Import torch to check for CUDA availability and device

# Define a custom class to write to multiple outputs (tee effect)
class DualOutput:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # Ensure immediate writing

    def flush(self):
        for f in self.files:
            f.flush()

# --- Model Loading ---
# Initialize a single variable to capture all loading messages
combined_output_status = ""

# Redirect stdout to capture print statements AND send to original streams
old_stdout = sys.stdout
# old_stderr = sys.stderr # Removed stderr tracking

# Create a single StringIO buffer for combined capture (now only stdout)
combined_redirected_output = io.StringIO()

# Now, sys.stdout will write to both the original stdout and the combined buffer
sys.stdout = DualOutput(old_stdout, combined_redirected_output)
# sys.stderr is no longer redirected to the combined buffer


print("Loading sentiment analysis model...")
try:
    # Check for CUDA availability and set device
    # Pass the device argument to the pipeline for explicit control
    if torch.cuda.is_available():
        device_str = "cuda:0" # Use the first GPU
        print("CUDA (GPU) is available. Using GPU.")
    else:
        device_str = "cpu"
        print("CUDA (GPU) is not available. Using CPU.")

    # Pass the detected device to the pipeline
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=device_str)

    print("Model loaded successfully!")
    # Get and print the actual device the model is on
    if classifier and hasattr(classifier, 'model') and hasattr(classifier.model, 'device'):
        print(f"Model is running on device: {classifier.model.device}")
    else:
        print("Could not determine the specific device of the loaded model.")

except Exception as e:
    # These print statements will now go to the redirected sys.stdout (and thus the buffer)
    # True exceptions and tracebacks will still go to the original sys.stderr by default
    print(f"Error loading model: {e}")
    print("Please ensure you have an active internet connection to download the model.")
    # Fallback or exit if model cannot be loaded
    classifier = None # Set to None to indicate failure

# Restore stdout to its original stream
sys.stdout = old_stdout
# sys.stderr is not restored here as it was never redirected to the buffer

# Get the content from the combined buffer (now only stdout)
combined_output_status = combined_redirected_output.getvalue()

# Function to format the loading status with colors
def format_loading_status_html(status_log: str) -> str:
    """
    Formats the model loading status log into an HTML string with
    background colors based on CPU/GPU mentions.
    """
    lines = status_log.strip().split('\n')
    html_lines = []
    
    # Use a pre-formatted block to maintain line breaks and monospace font
    # Default light gray background for the whole block container
    html_content = "<div style='font-family: monospace; padding: 10px; border-radius: 5px; background-color: #f0f0f0;'>" 
   
    for line in lines:
        #line_lower = line.lower()
        text_color = "darkorange" # Default for lines without specific device mention
        
        if device_str == "cuda:0":
            text_color = "darkgreen" # Green for GPU
        
        # Wrap each line in a span with the determined background color
        # display: block ensures each line gets its own row
        #html_lines.append(f"<span style='display: block; background-color: {background_color}; padding: 2px 5px; margin-bottom: 2px; border-radius: 3px;'>{line}</span>")
        html_lines.append(f"<span style='display: block; color: {text_color}; padding: 2px 5px; margin-bottom: 2px; border-radius: 3px;'>{line}</span>")  
    
    html_content += "".join(html_lines)
    html_content += "</div>"
    return html_content


# --- Prediction Function ---
def predict_sentiment(text):
    """
    Predicts the sentiment of the input text using the loaded BERT model.
    Returns HTML formatted string with color based on sentiment.

    Args:
        text (str): The input text string.

    Returns:
        str: An HTML formatted string indicating the predicted sentiment and its score,
             with color (green for positive, red for negative), or an error message.
    """
    if not classifier:
        return "<span style='color: gray;'>Error: Model not loaded. Cannot perform prediction.</span>"

    if not text.strip():
        return "<span style='color: gray;'>Please enter some text to analyze.</span>"

    try:
        result = classifier(text)[0]
        label = result['label']
        score = result['score']

        color = "green" if label == "POSITIVE" else "red"
        # If the model can output NEUTRAL, you might add another condition:
        # color = "orange" if label == "NEUTRAL" else color

        return f"<span style='color: {color}; font-weight: bold;'>Sentiment: {label} (Confidence: {score:.2f})</span>"
    except Exception as e:
        return f"<span style='color: gray;'>An error occurred during prediction: {e}</span>"

# --- Gradio UI Setup ---
print("Setting up Gradio interface...")

# Define the Gradio Blocks interface to allow more flexible layout
with gr.Blocks(theme="soft", title="BERT-based Sentiment Analysis") as iface:
    gr.Markdown(
        """
        # BERT-based Sentiment Analysis
        Enter any English text below to get its sentiment (Positive/Negative) predicted by a DistilBERT model.
        """
    )
    # Display the combined stdout status here
    if combined_output_status: # Only show if there's any output
        #gr.Markdown(f"** Model Loading Status : **\n```\n{combined_output_status}```")
        # Use gr.HTML to display the pre-formatted HTML string
        gr.HTML(format_loading_status_html(combined_output_status), label="Model Loading Status")

    with gr.Row():
        text_input = gr.Textbox(lines=5, placeholder="Enter text here...", label="Your Text")
        sentiment_output = gr.HTML(label="Sentiment Prediction")

    # Add Submit and Clear buttons
    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary") # Primary variant for emphasis
        clear_btn = gr.ClearButton(components=[text_input, sentiment_output]) # Clears specified components

    # Link button actions
    # The prediction will now only happen when the submit_btn is clicked
    submit_btn.click(fn=predict_sentiment, inputs=text_input, outputs=sentiment_output)

    # Examples will still populate the input and trigger prediction directly when clicked
    gr.Examples(
        examples=[
            "This movie was absolutely fantastic! I loved every minute of it.",
            "I found the service to be quite disappointing and slow.",
            "The weather today is neither good nor bad, just average.",
            "What a wonderful day to be alive!",
            "I'm feeling a bit under the weather."
        ],
        inputs=text_input,
        outputs=sentiment_output,
        fn=predict_sentiment,
        cache_examples=True, # Cache example predictions for faster loading
    )

# Launch the Gradio app.
print("Launching Gradio app...")
iface.launch(share=False, server_name="0.0.0.0")
print("Gradio app launched. Check your local URL (usually http://127.0.0.1:7860).")