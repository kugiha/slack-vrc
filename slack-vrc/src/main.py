import json
from utils import respond
def run_command(user, command, channel, command_text):
    return respond(None, "%s invoked %s in %s with the following text: %s" % (user, command, channel, command_text))
