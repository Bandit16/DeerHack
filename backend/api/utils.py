from .models import model, processor
from PIL import Image
import torch
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

def detect_emotion_from_image(image: Image.Image):
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
    
    # Convert scores to dictionary
    labels = model.config.id2label
    results = {labels[i]: float(probs[i]) for i in range(len(labels))}
    dominant_emotion = max(results, key=results.get)

    return {
        "dominant_emotion": dominant_emotion,
        "scores": results
    }

# Load environment variables from .env file
load_dotenv()

endpoint = os.getenv("endpoint")
model_name = os.getenv("model_name")
deployment = os.getenv("deployment")
subscription_key = os.getenv("subscription_key")
api_version = os.getenv("api_version")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def ask_gpt(user_message: str, system_message: str = "You are a helpful assistant.") -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )
    return response.choices[0].message.content

# #Example usage:
# question = "Can you interact with and use the project without requiring permission from a central entity?\nOptions: Yes, No"
# print(ask_gpt(question))