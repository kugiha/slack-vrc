DEFAULT_REPLY = "Sorry, I don't know what you mean."
PLUGINS = ['plugins']
with open('./slack_api_token.txt') as f:
    API_TOKEN = f.read()