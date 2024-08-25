import asyncio
from io import BytesIO

import grpc
from PIL import Image
import logging
from time import perf_counter
from inference_pb2 import ImageRequest, ImageResponse
from inference_pb2_grpc import InferenceServerStub

logging.basicConfig(level=logging.INFO)

# Define your image prompts
image_prompt_1 = 'pixel art, must pure white background, a character Wears a heavily modified AR visor with additional gadgets and a sleek tech-heavy outfit'
image_prompt_2 = 'pixel art, a futuristic cityscape with neon lights and flying cars, night time, vibrant colors'

async def generate_image(stub, prompt, filename):
    res: ImageResponse = await stub.GenerateImage(
        ImageRequest(prompt=prompt)
    )
    logging.info(f"Image generation status for '{prompt}': {res.status}")

    if res.status == 0:
        img = Image.open(BytesIO(res.image))
        img.save(filename)
        logging.info(f"Image saved to {filename}")
    else:
        logging.error(f"Image generation failed for prompt: {prompt}")

async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = InferenceServerStub(channel)
        start = perf_counter()

        # Run two image generation requests concurrently
        await asyncio.gather(
            generate_image(stub, image_prompt_1, "image1.png"),
            generate_image(stub, image_prompt_2, "image2.png")
        )

        logging.info(f"Finished image generation. Total time: {perf_counter() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())