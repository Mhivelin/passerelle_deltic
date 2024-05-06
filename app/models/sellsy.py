import json

import requests

url = "https://api.sellsy.com/items/search?direction=asc&limit=25"

payload = json.dumps(
    {"filters": {
        "type": ["<string>"],
        "favourite_filter": "<integer>"
    }})
headers = {
    "Content-Type":
    "application/json",
    "Authorization":
    "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIwOTQzOWU5YS01YzU1LTQyZWUtYWI5OS1lNzQzNTU4YzcyZTkiLCJqdGkiOiI1OTdhMTI1ZTFmNDliNGNmYTE4OGMzOGJmYjY2MWJlZWRlNTNhNDkwNDg5NzY2ODJiMTY5MGNiZTg1YWFhNGE0MDA3YjMxNzBmYjI0M2RjMyIsImlhdCI6MTcwODk1Mzk0NS43OTk4MDcsIm5iZiI6MTcwODk1Mzk0NS43OTk4MTEsImV4cCI6MTcwOTA0MDM0NS43OTA5NzIsInN1YiI6IjRkYzJmN2FmLTkwNTMtNGVjOS04YWQ2LTAyZjk2NjcwNzJhMyIsInNjb3BlcyI6WyJhbGwiXSwidXNlclR5cGUiOiJzdGFmZiIsInVzZXJJZCI6Mjk4MzEzLCJjb3JwSWQiOjEwOTI5MiwiY29ycE5hbWUiOiJkZWx0aWNkZW1vIiwiZmlyc3ROYW1lIjoiTWFyaXVzIiwibGFzdE5hbWUiOiJIaXZlbGluIiwibGFuZ3VhZ2UiOiJmciIsImVtYWlsIjoibWFyaXVzLmhpdmVsaW5AZ21haWwuY29tIn0.qBR1HC6J7Vr_524kvp6FyXoyHNm0HH-6UN1J_sGV-09CtWg7qmpp_QHzjDzbKw_Q177JpS2ef3Smzk78hJP4JGLQ4pGP-LnmEm5zQlpllX9ilhrMn_2u54CPrERsCTa9q67F0nRTrYXNS8tY7PWMsPk6UuXrNeXpU_hueEFWAIZRyfS9lG4Wzhly14Di0Y614l99zvQkFGIJu6WPsOBGsqyUT6jymE7HV4_PMeuTdhEy0WB4S0et5AH5FQzl7Rmg_HQK-mvGY0ISACl9bpa9vaSloDSlh7ucJEc8oIydOIa-V3QMMGDVJ3zHG64MTrZNtf-5jPv3tMhX-rZjo52tNQ",
}

response = requests.request("POST", url, headers=headers, data=payload)

# la réponse est une page web
print(response.text)
