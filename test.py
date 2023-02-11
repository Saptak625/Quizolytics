import requests

payload = {
            "maxQueryReturnLength": "1000",
            "queryString": 'alcohol',
            "questionType": "tossup",
            "randomize": False,
            "regex": True,
            "searchType": "answer",
            "setName": ""
        }

q = requests.get('https://www.qbreader.org/api/query', params=payload)
print(q.json())