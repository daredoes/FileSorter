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
        self.notifications = True

    def notify(self, message, title=None, subtitle=None, sound=True, data=None, override_app_setting=False):
        if self.notifications or override_app_setting:
            title = title if title else self.name

            def send_notification():
                notification(title=title, subtitle=subtitle, message=message, sound=sound, data=data)
            Thread(target=send_notification, daemon=True).start()
