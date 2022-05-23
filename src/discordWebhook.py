import requests, json
import os

def post_discord_webhook(text: str, avatar_url: str = None):
    main_content = {'content': text, 'avatar_url': avatar_url}
    if avatar_url:
        main_content.update({'avatar_url': avatar_url})
    headers = {'Content-Type': 'application/json'}
    requests.post(os.environ["DISCORD_WEBHOOK_URL"], json.dumps(main_content), headers=headers)