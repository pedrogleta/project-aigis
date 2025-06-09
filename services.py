import requests
import json

SESSION_ID = 's_123'
USER_ID = 'u_123'
AGENT_ID = 'aigis'

# Create Session
requests.post(
    f'http://127.0.0.1:8000/apps/{AGENT_ID}/users/{USER_ID}/sessions/{SESSION_ID}',
    headers={'Content-Type': 'application/json'}
)


# def parse_ai_response(ai_response: str) -> str:
#     data = json.loads(ai_response)
#     result = data[0]['content']['parts'][0]['text']
#     return result


def talk_to_agent(message: str) -> str:
    response = requests.post(
        'http://0.0.0.0:8000/run',
        headers={'Content-Type': 'application/json'},
        json={
            'app_name': AGENT_ID,
            'user_id': USER_ID,
            'session_id': SESSION_ID,
            'new_message': {
                'role': 'user',
                'parts': [
                    {
                        "text": message
                    }
                ]
            }
        }
    )

    return response.text


print(talk_to_agent('Pedro, faz um favor pra mim, identifica os agentes comerciais que estão com a maior performance essa semana e monta uma lista pra mim'))
