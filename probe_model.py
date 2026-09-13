import os 
import google.genai as genai
print('genai version loaded')
print('genai file:', genai.__file__)
print('Client attrs:')
print([a for a in dir(genai.Client) if 'model' in a.lower() or 'list' in a.lower() or 'generate' in a.lower()])
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print('client attrs:')
    print([a for a in dir(client) if 'model' in a.lower() or 'list' in a.lower() or 'generate' in a.lower()])
except Exception as e:
    print('client error:', type(e), e)
