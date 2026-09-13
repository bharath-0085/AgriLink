import os 
import google.genai as genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
models = list(client.models.list())
print('models count:', len(models))
for m in models:
    print(m.name)
