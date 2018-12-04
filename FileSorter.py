import os
import rumps
import shutil

from collections import defaultdict

from DareDoesRumps import DareDoesRumps
from utils import path_to_folder, filetype

app_name = "FileSorter"
app_title = "FS"

builtin_folders_to_sort = {"Desktop": "~/Desktop", "Downloads": "~/Downloads"}

default_extension_groups = {
    "TextFiles": (
        {
            "doc": 1,
            "docx": 1,
            "log": 1,
            "msg": 1,
            "odt": 1,
            "pages": 1,
            "rtf": 1,
            "tex": 1,
            "txt": 1,
            "wpd": 1,
            "wps": 1,
            "gdoc": 1,
        },
        1,
    ),
    "DataFiles": (
        {
            "csv": 1,
            "dat": 1,
            "ged": 1,
            "key": 1,
            "keychain": 1,
            "pps": 1,
            "ppt": 1,
            "pptx": 1,
            "sdf": 1,
            "tar": 1,
            "tax2016": 1,
            "tax2018": 1,
            "vcf": 1,
            "xml": 1,
        },
        1,
    ),
    "AudioFiles": (
        {
            "aif": 1,
            "iff": 1,
            "m3u": 1,
            "m4a": 1,
            "mid": 1,
            "mp3": 1,
            "mpa": 1,
            "wav": 1,
            "wma": 1,
        },
        1,
    ),
    "VideoFiles": (
        {
            "3g2": 1,
            "3gp": 1,
            "asf": 1,
            "avi": 1,
            "flv": 1,
            "m4v": 1,
            "mov": 1,
            "mp4": 1,
            "mpg": 1,
            "rm": 1,
            "srt": 1,
            "swf": 1,
            "vob": 1,
            "wmv": 1,
            "mkv": 1,
        },
        1,
    ),
    "3DVideoFiles": ({"3dm": 1, "3ds": 1, "max": 1, "obj": 1}, 1),
    "RasterImageFiles": (
        {
            "bmp": 1,
            "dds": 1,
            "gif": 1,
            "jpg": 1,
            "jpeg": 1,
            "png": 1,
            "psd": 1,
            "pspimage": 1,
            "tga": 1,
            "thm": 1,
            "tif": 1,
            "tiff": 1,
            "yuv": 1,
        },
        1,
    ),
    "VectorImageFiles": ({"ai": 1, "eps": 1, "ps": 1, "svg": 1}, 1),
    "PageLayoutFiles": ({"indd": 1, "pct": 1, "pdf": 1}, 1),
    "SpreadsheetFiles": ({"xlr": 1, "xls": 1, "xlsx": 1}, 1),
    "DatabaseFiles": ({"accdb": 1, "db": 1, "dbf": 1, "mdb": 1, "pdb": 1, "sql": 1}, 1),
    "ExecutableFiles": (
        {
            "apk": 1,
            "app": 1,
            "bat": 1,
            "cgi": 1,
            "com": 1,
            "exe": 1,
            "gadget": 1,
            "jar": 1,
            "wsf": 1,
        },
        1,
    ),
    "GameFiles": ({"dem": 1, "gam": 1, "nes": 1, "rom": 1, "sav": 1}, 1),
    "CADFiles": ({"dwg": 1, "dxf": 1}, 1),
    "GISFiles": ({"gpx": 1, "kml": 1, "kmz": 1}, 1),
    "WebFiles": (
        {
            "asp": 1,
            "aspx": 1,
            "cer": 1,
            "cfm": 1,
            "csr": 1,
            "css": 1,
            "html": 1,
            "js": 1,
            "jsp": 1,
            "jsx": 1,
            "php": 1,
            "rss": 1,
            "xhtml": 1,
        },
        1,
    ),
    "PluginFiles": ({"crx": 1, "plugin": 1}, 1),
    "FontFiles": ({"fnt": 1, "fon": 1, "otf": 1, "ttf": 1, "woff": 1}, 1),
    "SystemFiles": (
        {
            "cab": 1,
            "cpl": 1,
            "cur": 1,
            "deskthemepack": 1,
            "dll": 1,
            "dmp": 1,
            "drv": 1,
            "icns": 1,
            "ico": 1,
            "lnk": 1,
            "sys": 1,
        },
        1,
    ),
    "SettingsFiles": ({"cfg": 1, "ini": 1, "prf": 1}, 1),
    "EncodedFiles": ({"hqx": 1, "mim": 1, "uue": 1}, 1),
    "CompressedFiles": (
        {
            "7z": 1,
            "cbr": 1,
            "deb": 1,
            "gz": 1,
            "pkg": 1,
            "rar": 1,
            "rpm": 1,
            "sitx": 1,
            "tar.gz": 1,
            "zip": 1,
            "zipx": 1,
        },
        1,
    ),
    "DiskImageFiles": (
        {"bin": 1, "cue": 1, "dmg": 1, "iso": 1, "mdf": 1, "toast": 1, "vcd": 1},
        1,
    ),
    "DeveloperFiles": (
        {
            "c": 1,
            "class": 1,
            "cpp": 1,
            "cs": 1,
            "dtd": 1,
            "fla": 1,
            "h": 1,
            "java": 1,
            "lua": 1,
            "m": 1,
            "pl": 1,
            "py": 1,
            "sh": 1,
            "sln": 1,
            "swift": 1,
            "vb": 1,
            "vcxproj": 1,
            "xcodeproj": 1,
        },
        1,
    ),
    "BackupFiles": ({"bak": 1, "tmp": 1}, 1),
    "MiscFiles": ({"crdownload": 1, "ics": 1, "msi": 1, "part": 1, "torrent": 1}, 1),
}

default_settings = {
    "folders": builtin_folders_to_sort,
    "extensions": default_extension_groups,
}


class FileSorter:
    def __init__(self, extensions):
        self._extensions = extensions

    def add_extension_group(self, group_name, overwrite=False):
        if overwrite or group_name not in self.extensions.keys():
            self._extensions[group_name] = ({}, 0)
            return True

    def delete_extension_group(self, group_name):
        if group_name in self._extensions.keys():
            del self._extensions[group_name]
            return True

    def toggle_watch_of_extension(self, extension, group_name):
        if group_name in self._extensions.keys():
            if extension in self._extensions[group_name][0].keys():
                self._extensions[group_name][0][extension] = 0 if self._extensions[group_name][0][extension] else 1
                return self._extensions[group_name][0][extension]

    def add_extension_to_group(self, extension, group_name):
        if group_name not in self._extensions.keys():
            self.add_extension_group(group_name)
        self._extensions[group_name][0][str(extension).lower()] = 1
        return True

    def delete_extension_from_group(self, group_name, extension):
        if group_name in self._extensions.keys():
            if extension in self._extensions[group_name][0].keys():
                del self._extensions[group_name][0][extension]
                return True
        return False

    @property
    def extensions(self):
        return self._extensions.copy()

    def sort_folder(self, path, levels=0):
        path = os.path.expanduser(path)
        self.sort_by_filetype(self.get_files(path, levels), path)

    def watched_folders(self):
        return [x for x in self.extensions.keys() if self.extensions[x][1]]

    def watched_keys_for_folder(self, folder):
        items = self.extensions[folder][0]
        return [x for x in items.keys() if items[x]]

    def sort_by_filetype(self, files, root_path):
        """Moves files into new folders, handles folders recursively"""
        moving_files = defaultdict(list)
        folders_to_sort = []
        for folder, folder_contents in files.items():
            if isinstance(folder_contents, list):
                # if instance has files, prepare for sorting
                for a_file in folder_contents:
                    moving_files[filetype(a_file)].append(a_file)
            if isinstance(folder_contents, dict):
                # if instance is folder, sort the folder
                folders_to_sort.append(folder)
        for extension in moving_files.keys():
            if isinstance(moving_files[extension], list):
                try:
                    watched_folders = self.watched_folders()
                    for folder in watched_folders:
                        watched_keys = self.watched_keys_for_folder(folder)
                        if str(extension).lower() in watched_keys:
                            final_destination = "{}/{}".format(root_path, folder)
                            os.mkdir(final_destination)
                            break
                except OSError:
                    pass

                for the_file in moving_files[extension]:
                    try:
                        for folder_name in [
                            key
                            for key in self.extensions.keys()
                            if self.extensions[key][1]
                        ]:
                            lower_case_extension = str(extension).lower()
                            valid_extensions = [
                                x
                                for x in self.extensions[folder_name][0]
                                if self.extensions[folder_name][0][x]
                            ]
                            if (
                                lower_case_extension in valid_extensions
                                and self.extensions[folder_name][0][
                                    lower_case_extension
                                ]
                            ):
                                print("File: {}".format(path_to_folder(the_file)))
                                final_destination = "{}/{}/{}".format(
                                    root_path, folder_name, path_to_folder(the_file)
                                )
                                print("Moving to {}".format(final_destination))
                                shutil.move(the_file, final_destination)
                                print("Moved to {}".format(final_destination))
                                break

                    except shutil.Error:
                        pass
            for folder in folders_to_sort:
                self.sort_by_filetype(files[folder], "{}/{}".format(root_path, folder))

    def get_files(self, path, levels=0):
        """Checks files and folders, searches subfolders recursively"""
        files = {path_to_folder(path): []}
        for filename in os.listdir(path):
            try:
                # if this errors, then this is a file
                os.listdir(path + "/" + filename)
                # if it doesn't error, this is a Folder
                # check that the folder is not a Folder we tend to sort into
                if filename not in self.extensions.keys():
                    if levels > 0:
                        # if this passes we are searching the folders of this folder
                        files[filename] = {}
                        print("Searching Folder: {}".format(filename))
                        files[filename] = self.get_files(
                            "{}/{}".format(path, filename), levels - 1
                        )
            except OSError:
                # add file to dictionary
                files[path_to_folder(path)].append(path + "/" + filename)
        print("Leaving Folder: {}".format(path_to_folder(path)))
        return files


class App(DareDoesRumps):

    how_to = """
    Pass
    """

    def __init__(self, name, *args, **kwargs):
        super(App, self).__init__(name, *args, **kwargs)
        self.fs = FileSorter(self.settings.get("extensions", {}))
        self.menu.add(rumps.MenuItem("Add Folder", callback=self.add_folder_button))
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Sort All Selected"))
        self.menu.add(None)
        self.folders = rumps.MenuItem("Folders", callback=lambda: print())
        self.add_folders_to_menu()
        self.menu.add(self.folders)
        self.extensions = rumps.MenuItem("Extensions", callback=lambda: print())
        self.add_extensions_to_menu()
        self.menu.add(self.extensions)
        self.menu.add(None)
        self.menu.add(rumps.MenuItem("Help", callback=self.help_menu))
        self.menu.add(None)

    def help_menu(self, sender):
        rumps.alert('How To Use FileSorter', self.how_to)

    def make_extension_button(self, parent_folder, parent_menu):
        def callback(self, sender):
            res = rumps.Window(cancel=True, message='Please enter a file extension, without `.`',
                               title='Add Extension For {}'.format(parent_folder)).run()

            if res.clicked:
                self.add_extension(res.text, parent_folder, parent_menu)
        return callback

    def add_extension(self, extension, parent_folder, parent_menu):
        self.fs.add_extension_to_group(extension, parent_folder)
        self.insert_extension_into_menu(extension, parent_menu)
        self.settings = {
            "extensions": self.fs.extensions
        }

    def make_toggle_of_extension(self, extension, group_name):
        def callback(sender):
            sender.state = self.fs.toggle_watch_of_extension(extension, group_name)
            self.settings = {
                'extensions': self.fs.extensions
            }
        return callback

    def insert_extension_into_menu(self, extension, parent):
        keys = [x for i, x in enumerate(parent.keys()) if i > 2]  # The number of non-extension menus at the top
        menu = rumps.MenuItem(extension, callback=self.make_toggle_of_extension(extension, parent.title))
        menu.state = self.fs.extensions[parent.title][0][extension]

        def callback(sender):
            if self.fs.delete_extension_from_group(parent.title, extension):
                del parent[extension]
                self.notify('Extension Deleted', subtitle=parent.title)

        remove_menu = rumps.MenuItem("Delete", callback=callback)
        menu.add(remove_menu)
        keys.append(extension)
        key_to_use = None
        for key in sorted(keys):
            if key == extension:
                break
            key_to_use = key

        if key_to_use:
            parent.insert_after(key_to_use, menu)
        else:
            parent.add(menu)

    def add_folder_button(self, sender):
        res = rumps.Window(cancel=True, message='Please enter an absolute path, or one that starts from `~`.',
                           title='Add Folder').run()

        if res.clicked:
            resp = rumps.Window(cancel=True, title='Add Name',
                                message='Please enter a name for the path, this will be displayed in the menu.').run()
            if resp.clicked:
                self.add_path(res.text, resp.text)

    def add_path(self, path, key=None):
        if not key:
            key = path
        folders = self.settings.get("folders", {})
        folders[key] = path
        self.settings = {
            "folders": folders
        }
        self.insert_folder_into_menu(key, path)

    def insert_folder_into_menu(self, folder, path):
        keys = [x for i, x in enumerate(self.folders.keys()) if i > 2]
        menu = rumps.MenuItem(folder, callback=self.make_folder_callback(folder, path))

        def callback(sender):
            folders = self.settings.get("folders", {})
            if folder in folders.keys() and folder in self.folders.keys():
                del self.folders[folder]
                del folders[folder]
                self.settings = {
                    'folders': folders
                }
                self.notify('Deleted', subtitle=folder)

        remove_menu = rumps.MenuItem("Delete", callback=callback)
        menu.add(remove_menu)
        keys.append(folder)
        key_to_use = None
        for key in sorted(keys, key=lambda k: str(k).lower()):
            if key == folder:
                break
            key_to_use = key

        if key_to_use:
            self.folders.insert_after(key_to_use, menu)
        else:
            self.folders.add(menu)

    def add_folders_to_menu(self):
        for folder, path in sorted(
            self.settings.get("folders", {}).items(), key=lambda kv: kv[0].lower()
        ):
            self.insert_folder_into_menu(folder, path)

    def make_folder_callback(self, folder, path):
        def callback(sender):
            self.fs.sort_folder(path)
        return callback

    def add_extensions_to_menu(self):
        for folder, extensions in sorted(
            self.fs.extensions.items(), key=lambda kv: kv[0].lower()
        ):
            folder_menu = rumps.MenuItem(folder)
            folder_menu.add(rumps.MenuItem("Add Extension", callback=self.make_extension_button(folder, folder_menu)))
            folder_menu.add(None)
            for extension in sorted(extensions[0].keys(), key=lambda value: value.lower()):
                self.insert_extension_into_menu(extension, folder_menu)
            self.extensions.add(folder_menu)


if __name__ == "__main__":
    app = App(app_name, title=app_title, default_persistent_settings=default_settings)
    app.run()
