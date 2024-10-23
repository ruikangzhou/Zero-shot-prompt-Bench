import time
#import openai
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAI
from colorama import Fore
from config import cfg

def request_with_timeout(*args, **kwargs):
    kwargs['timeout'] = 10  # Timeout in seconds
    return requests.request(*args, **kwargs)


@retry(stop=stop_after_attempt(5),  # Retry up to 5 times
       wait=wait_exponential(min=1, max=60),  # Exponential backoff
       retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.RequestException)))
def create_chat_completion(messages, model="gpt-4o-mini", temperature=1, max_tokens=None) -> str:
    """Create a chat completion using the OpenAI API"""
    client = OpenAI()
    response = None
    #num_retries = 5
    #for attempt in range(num_retries):
    #try:
    #print(messages)
    """"""

    response = client.chat.completions.create(
        #model=model,
        model = model,
        messages=messages,
        temperature = temperature,
        max_tokens = max_tokens
    )
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    break
    """
    """
    except openai.error.RateLimitError:
        if cfg.debug_mode:
            print(Fore.RED + "Error: ", "API Rate Limit Reached. Waiting 20 seconds..." + Fore.RESET)
        time.sleep(20)
    except openai.error.APIError as e:
        if e.http_status == 502:
            if cfg.debug_mode:
                print(Fore.RED + "Error: ", "API Bad gateway. Waiting 20 seconds..." + Fore.RESET)
            time.sleep(20)
        else:
            raise
        if attempt == num_retries - 1:
            raise
    except openai.error.InvalidRequestError:
        raise
    """

    if response is None:
        raise RuntimeError("Failed to get response after 5 retries")

    return response.choices[0].message.content.strip()
