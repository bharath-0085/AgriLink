import json, urllib.request, urllib.error
url = 'http://127.0.0.1:8000/api/v1/ai/chatbot/'
req = urllib.request.Request(url, data=json.dumps({'message': 'Hello farmer'}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        print('STATUS', resp.status)
        print(resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('HTTPERROR', e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print('ERROR', repr(e))
