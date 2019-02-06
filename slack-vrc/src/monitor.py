from enum import Enum
import time
import threading
from auth import a
from vrchat_api.enum import Status
check_interval_sec = 30
class UserMonitor:
    def __init__(self, user, monitor_type, message):
        self.user = user
        self.user_state = {}
        self.save_user_state(user, initial=True)
        self.monitor_type = monitor_type
        self.message = message
        self.finished = False
        self.start_monitoring_thread()
    def start_monitoring_thread(self):
        thread = threading.Thread(target=self.monitor_thread)
        thread.start()
        self.message.reply('Monitor {} has successfully started.'.format(str(self)))
    def monitor_thread(self):
        while True:
            time.sleep(check_interval_sec)
            if self.finished:
                self.message.reply('Monitor {} has been successfully canceled.'.format(str(self)))
                return
            print('monitor')
            self.save_user_state(a.getUserById(self.user.id))
    def finish_monitoring_thread(self):
        self.finished = True
    def save_user_state(self, user, initial=False):
        if not initial:
            if self.user_state['location'] != user.location:
                self.on_location_change(self.user_state['location'], user.location)
            if self.user_state['status'] != user.status:
                self.on_status_change(self.user_state['status'], user.status)
        self.user_state = {
            'location': user.location,
            'status': user.status
        }
    def on_status_change(self, old, new):
        if (self.monitor_type >= UserMonitorType.ONOFF) and (old != new):
            self.message.reply('{}\n>Status: {} -> `{}`'.format(str(self), old.name, new.name))
    def on_location_change(self, old, new):
        if (self.monitor_type == UserMonitorType.PRIVATE) and (old.private != new.private):
            self.message.reply('{}\n>Private: {} -> `{}`'.format(str(self), old.private, new.private))
        if (self.monitor_type == UserMonitorType.WORLD_MOVE) and (old.worldId != new.worldId):
            old_worldname = a.getWorldById(old.worldId).name if old.worldId is not None else ':lock:'
            new_worldname = a.getWorldById(new.worldId).name if new.worldId is not None else ':lock:'
            self.message.reply('{}\n>{} -> `{}`'.format(str(self), old_worldname, new_worldname))
    def __str__(self):
        return '{} for {}'.format(self.user.displayName, self.monitor_type)
class UserMonitorType(Enum):
    ONOFF = 1
    PRIVATE = 2
    WORLD_MOVE = 3
    @staticmethod
    def getUserMonitorTypeByString(string):
        if string == 'onoff':
            return UserMonitorType.ONOFF
        if string == 'private':
            return UserMonitorType.PRIVATE
        if string == 'move':
            return UserMonitorType.WORLD_MOVE
        return None