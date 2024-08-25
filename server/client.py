import asyncio
from io import BytesIO

import grpc
from PIL import Image
import scipy
import numpy as np

from inference_pb2 import InferenceRequest, AudioResponse, ImageRequest, ImageResponse
from inference_pb2_grpc import InferenceServerStub
import logging
from pprint import pformat
from time import perf_counter

logging.basicConfig(level=logging.INFO)

image_prompt = 'pixel art, must pure white background, a character Wears a heavily modified AR visor with additional gadgets and a sleek tech-heavy outfit'
audio_prompt = 'generate a music with a intensed mood, 10 sec, used for game background music'


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = InferenceServerStub(channel)
        start = perf_counter()

        # Image generation

        res: ImageResponse = await stub.GenerateImage(
            ImageRequest(prompt=image_prompt)
        )

        logging.info(f"Image generation status: {res.status}")

        if res.status == 0:
            print(len(res.image))
            img = Image.open(BytesIO(res.image))
            img.save("image.png")
            logging.info(f"Image saved to image.png")
        else:
            logging.error("Image generation failed")

        # Audio generation

        res: AudioResponse = await stub.GenerateAudio(
            InferenceRequest(prompt=audio_prompt)
        )

        logging.info(f"Audio generation status: {res.status}")

        if res.status == 0:
            sample_rate = res.sample_rate
            audio_data = np.frombuffer(res.audio, dtype=np.float32)
            scipy.io.wavfile.write("audio.wav", sample_rate, audio_data)
            logging.info(f"Audio saved to audio.wav")

        else:
            logging.error("Audio generation failed")

        logging.info(f"Finish. Total time: {perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())