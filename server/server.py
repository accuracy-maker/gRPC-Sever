import asyncio
import logging
from time import perf_counter

import grpc
from inference import inference_audio, inference_image
from inference_pb2_grpc import InferenceServer, add_InferenceServerServicer_to_server
from inference_pb2 import InferenceRequest, AudioResponse, ImageRequest, ImageResponse

logging.basicConfig(level=logging.INFO)

class InferenceService(InferenceServer):
    async def GenerateAudio(self, request: InferenceRequest, context) -> AudioResponse:
        logging.info(f"Received audio generation request with prompt: {request.prompt}")
        start = perf_counter()
        audio = inference_audio(request.prompt)
        logging.info(f"Audio generation time: {perf_counter() - start:.2f}s")
        return AudioResponse(audio=audio['data'], sample_rate=audio['sample_rate'], status=audio['status'])


    async def GenerateImage(self, request: ImageRequest, context) -> ImageResponse:
        logging.info(f"Received image generation request with prompt: {request.prompt}")
        start = perf_counter()
        image = inference_image(request.prompt)
        logging.info(f"Image generation time: {perf_counter() - start:.2f}s")
        return ImageResponse(image=image['image'], width=image['width'], height=image['height'], format=image['format'], status=image['status'])


    

async def serve():
    server = grpc.aio.server()
    add_InferenceServerServicer_to_server(InferenceService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    logging.info("Server started")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
