from typing import List
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import numpy as np

from io import BytesIO
import requests
from PIL import Image
from openai import OpenAI
from collections import Counter


# Load the model and processor
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device)

client = OpenAI()

def detect_background_color(image):
    # Get image size
    width, height = image.size
    
    # Extract edge pixels (top, bottom, left, right edges)
    edge_pixels = []
    for x in range(width):
        edge_pixels.append(image.getpixel((x, 0)))       # Top edge
        edge_pixels.append(image.getpixel((x, height-1))) # Bottom edge
    for y in range(height):
        edge_pixels.append(image.getpixel((0, y)))       # Left edge
        edge_pixels.append(image.getpixel((width-1, y)))  # Right edge
    
    # Determine the most common color in the edge pixels
    most_common_color = Counter(edge_pixels).most_common(1)[0][0]
    return most_common_color

def remove_background(image, background_color, tolerance=30):
    image = image.convert("RGBA")
    data = image.getdata()

    new_data = []
    
    for item in data:
        # If all RGB values are greater than 250, make it transparent
        if item[0] > 250 and item[1] > 250 and item[2] > 250:
            new_data.append((255, 255, 255, 0))  # Change to transparent
        else:
            new_data.append(item)  # Keep the original color for other pixels
    
    image.putdata(new_data)
    return image 


@torch.no_grad()
def inference_audio(prompts: List[str], max_new_tokens: int = 512) -> List[np.ndarray]:
    try:
        # Process the input text prompts
        inputs = processor(
            text=prompts,
            padding=True,
            return_tensors="pt",
        )
        
        # Generate audio
        audio_values = model.generate(
            **inputs.to(device),
            do_sample=True,
            guidance_scale=3,
            max_new_tokens=max_new_tokens
        )

        return {
            "data": audio_values[0,0].cpu().numpy().tobytes(),
            "sample_rate": model.config.audio_encoder.sampling_rate,
            "status": 0
        }

    except Exception as e:
        return {
            "data": b'',
            "sample_rate": 0,
            "status": 1
        }


@torch.no_grad()
def inference_image(prompt: str) -> Image:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        img_info = requests.get(image_url)
        img = Image.open(BytesIO(img_info.content))
        
        # post processing
        background_color = detect_background_color(img)

        img_with_transparency = remove_background(img, background_color)

        img_format = 'PNG'

        img_bytes = BytesIO()
        img_with_transparency.save(img_bytes, format=img_format)
        img_bytes = img_bytes.getvalue()

        width, height = img_with_transparency.size

        status = 0

        return {
            "image": img_bytes,
            "width": width,
            "height": height,
            "format": img_format,
            "status": status,
        }
    
    except Exception as e:
        return {
            "image": b'',
            "width": 0,
            "height": 0,
            "format": '',
            "status": 1,
        }


  
    