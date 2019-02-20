import json
from utils import respond
from vrconline import online
def run_command(user, command, channel, command_text):
    command_text_list = command_text.split()
    if command_text[0] in ['online', 'o']:
        respond(online())
    return respond(None, "%s invoked %s in %s with the following text: %s" % (user, command, channel, command_text))
