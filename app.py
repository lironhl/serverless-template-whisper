import torch
import whisper
import os
import base64
from io import BytesIO

DEFAULT_MODEL_OPTIONS = {
    "language": "he",
    "beam_size": 5,
    "best_of": 5,
    "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
}

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model
    
    model = whisper.load_model("medium")

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs: dict) -> dict:
    global model

    # Parse out your arguments
    mp3BytesString = model_inputs.get('mp3BytesString', None)
    if mp3BytesString == None:
        return {'message': "No input provided"}
    
    mp3Bytes = BytesIO(base64.b64decode(mp3BytesString.encode("ISO-8859-1")))
    with open('input.mp3','wb') as file:
        file.write(mp3Bytes.getbuffer())
    
    # Run the model
    result = model.transcribe(
        "input.mp3",
        **DEFAULT_MODEL_OPTIONS
    )
    output = {"text":result["text"]}
    os.remove("input.mp3")

    # Return the results as a dictionary
    return output
