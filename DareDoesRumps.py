import keyring

from cipher import cipher  # magic import of compiled pyc file
from cryptography.fernet import Fernet
from rumps import App, notification
from threading import Thread

default_settings = {}


class DareDoesRumps(App):

    def __init__(self, name, title=None, icon=None, template=None, menu=None, quit_button='Quit',
                 default_persistent_settings=default_settings, settings_filename='persistent_settings.json'):
        super(DareDoesRumps, self).__init__(name, title=title, icon=icon, template=template, menu=menu,
                                            quit_button=quit_button,
                                            default_persistent_settings=default_persistent_settings,
                                            settings_filename=settings_filename)
        self.cipher = Fernet(cipher)
        self.notifications = True

    def set_password(self, username, password):
        keyring.set_password(self.name, username, password)

    def get_password(self, username):
        keyring.get_password(self.name, username)

    def encrypt(self, string):
        return self.cipher.encrypt(bytes(string, 'utf-8')).decode('utf-8')

    def decrypt(self, string):
        return self.cipher.decrypt(bytes(string, 'utf-8')).decode('utf-8')

    def notify(self, message, title=None, subtitle=None, sound=True, data=None, override_app_setting=False):
        if self.notifications or override_app_setting:
            title = title if title else self.name

            def send_notification():
                notification(title=title, subtitle=subtitle, message=message, sound=sound, data=data)
            Thread(target=send_notification, daemon=True).start()
