import ollama

# Configure your server URL here
SERVER_HOST = 'localhost:11434'
client = ollama.Client(host=SERVER_HOST)

# A safety cap so a forgotten num_predict can't turn into a multi-minute
# generation. Every lab in this course is meant to run fast (each exercise
# under ~5 minutes); this is what keeps that true even when a call doesn't
# set its own limit. Pass num_predict=... explicitly to override it.
_DEFAULT_NUM_PREDICT = 300

def _with_default_cap(options):
    options = dict(options)
    options.setdefault('num_predict', _DEFAULT_NUM_PREDICT)
    return options

def call_ollama(prompt, model="qwen2.5-coder:latest", think=False, **options):
    """
    Send a prompt to the Ollama API.

    Args:
        prompt (str): The prompt to send
        model (str): Model name to use
        think (bool): Whether to allow the model to reason before answering.
            Defaults to False: several models in this course's roster (e.g.
            gemma4) think by default, and a tight num_predict budget can get
            silently consumed by hidden reasoning tokens, leaving response
            empty. Pass think=True for labs that specifically study reasoning
            (and give it a generous num_predict when you do).
        **options: Additional model parameters (temperature, top_k, etc.)
            If you don't set num_predict, it defaults to 300 tokens so a
            single call can't run away; pass num_predict=... to override.

    Returns:
        str: The model's response
    """
    try:
        response = client.generate(
            model=model,
            prompt=prompt,
            think=think,
            options=_with_default_cap(options)
        )
        return response['response']

    except Exception as e:
        return f"Error: {e}"

def chat_ollama(messages, model="gemma4:latest", think=False, **options):
    """
    Send a chat conversation to the Ollama API.

    Args:
        messages (list): List of message dicts with 'role' and 'content'
        model (str): Model name to use
        think (bool): See call_ollama. Defaults to False.
        **options: Additional model parameters. num_predict defaults to 300
            if you don't set it (see call_ollama).

    Returns:
        str: The model's response
    """
    try:
        response = client.chat(
            model=model,
            messages=messages,
            think=think,
            options=_with_default_cap(options)
        )
        return response['message']['content']

    except Exception as e:
        return f"Error: {e}"

def stream_ollama(prompt, model="gemma4:latest", think=False, **options):
    """
    Stream a response from Ollama (for real-time output).

    Args:
        prompt (str): The prompt to send
        model (str): Model name to use
        think (bool): See call_ollama. Defaults to False.
        **options: Additional model parameters. num_predict defaults to 300
            if you don't set it (see call_ollama).

    Yields:
        str: Chunks of the response as they arrive
    """
    try:
        stream = client.generate(
            model=model,
            prompt=prompt,
            stream=True,
            think=think,
            options=_with_default_cap(options)
        )
        for chunk in stream:
            yield chunk['response']

    except Exception as e:
        yield f"Error: {e}"


_image_cache = {}

def _download_image(image_url, headers, retries=3):
    """Download image bytes, cached by URL and retried with backoff on 429.

    Several lab exercises call analyze_image on the same URL more than once
    (e.g. a "basic" and a "detailed" description back to back). Without a
    cache, a lab session can fire off enough rapid repeat requests to trip
    a host's rate limiting (Wikimedia's included).

    This shells out to curl rather than using `requests` directly: some
    hosts (Wikimedia among them) block on TLS/HTTP client fingerprint, not
    just request rate, and reject `requests`/urllib3's handshake while
    accepting curl's, even for the same URL, headers, and IP. If curl isn't
    available on your machine, swap this back to requests.get(...).
    """
    if image_url in _image_cache:
        return _image_cache[image_url]
    import subprocess
    import time
    ua = headers.get('User-Agent', '')
    last_result = None
    for attempt in range(retries):
        result = subprocess.run(
            ['curl', '-sL', '-A', ua, '-w', '%{http_code}', image_url],
            capture_output=True, timeout=30
        )
        body, status = result.stdout[:-3], result.stdout[-3:].decode()
        if status == '429':
            last_result = status
            time.sleep(2 ** attempt)
            continue
        if status != '200':
            raise RuntimeError(f"curl got HTTP {status} for {image_url}")
        _image_cache[image_url] = body
        return body
    raise RuntimeError(f"curl got HTTP {last_result} for {image_url} after {retries} retries")

def analyze_image(image_url, prompt, model="qwen3-vl:8b", temperature=0.3):
    """
    Analyze an image from a URL with a text prompt.

    Args:
        image_url: URL of the image
        prompt: Question or instruction about the image
        model: Vision model to use
        temperature: Randomness (0.0-1.0)
    """

    # Add User-Agent header to avoid 403 errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    image_bytes = _download_image(image_url, headers)

    # Pass image bytes directly
    response = client.chat(
        model=model,
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [image_bytes]
        }],
        think=False,
        options={'temperature': temperature, 'num_predict': _DEFAULT_NUM_PREDICT}
    )
    return response['message']['content']

# Test the function
if __name__ == "__main__":
    test_prompt = "Say 'Hello, World!' and nothing else."
    print("Testing API call...")
    result = call_ollama(test_prompt, temperature=0.1)
    print(f"Response: {result}")
    
    print("\n" + "="*50)
    print("Testing streaming:")
    for chunk in stream_ollama("Count to 5 slowly.", temperature=0.1):
        print(chunk, end='', flush=True)
    print()
