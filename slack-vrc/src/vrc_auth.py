import os
from vrchat_api import VRChatAPI
vrc_id = os.environ['vrcID']
vrc_pw = os.environ['vrcPW']
vrc = VRChatAPI(
    vrc_id,
    vrc_pw
)
vrc.authenticate()
