from vrchat_api import VRChatAPI

with open('./vrc_api_credentials.txt') as f:
    a = VRChatAPI(
        f.readline().rstrip('\r\n'),
        f.readline().rstrip('\r\n')
    )
a.authenticate()