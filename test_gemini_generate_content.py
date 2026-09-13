import google.genai as genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print('generate_content signature:', client.models.generate_content)
models_to_test = [
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite',
    'gemini-flash-latest',
    'gemini-pro-latest',
    'gemini-3.5-flash',
    'gemini-3.6-flash',
]
for model_name in models_to_test:
    print('\nTesting model:', model_name)
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[types.Content(role='user', parts=[types.Part(text='Say hello.')])],
            config=types.GenerateContentConfig(temperature=0.1),
        )
        print('success:', type(response), getattr(response, 'text', None))
    except Exception as e:
        print('error type:', type(e).__name__)
        print('error:', e)
