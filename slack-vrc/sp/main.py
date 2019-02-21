import json
from utils import respond
from vrconline import online, online_grouped
def run_command(user, command, channel, command_text):
    command_text_list = command_text.split()
    if command_text_list[0] in ['online', 'o']:
        return respond(None, online())
    if command_text_list[0] in ['ong', 'g']:
        return respond(None, online_grouped())
    return respond(None, "%s invoked %s in %s with the following text: %s" % (user, command, channel, command_text))
