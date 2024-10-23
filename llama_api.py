import time
#import openai
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from huggingface_hub import InferenceClient
from colorama import Fore
from config import cfg

def request_with_timeout(*args, **kwargs):
    kwargs['timeout'] = 10  # Timeout in seconds
    return requests.request(*args, **kwargs)

"""
@retry(stop=stop_after_attempt(5),  # Retry up to 5 times
       wait=wait_exponential(min=1, max=60),  # Exponential backoff
       retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.RequestException)))
"""
def create_chat_completion(messages):
    """Create a chat completion using the OpenAI API"""
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-70B"
    headers = {"Authorization": "Bearer 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"}


    response = requests.post(API_URL, headers=headers, json=messages)
    if response is None:
        raise RuntimeError("Failed to get response after 5 retries")
    return response.json()




print(create_chat_completion({"inputs": "Is apple white or red?"},))