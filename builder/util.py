import os
import json
import codecs

try:
    import svn.local
except ImportError:
    pass

def apply_settings_files(settings, file_names):
    for file_name in file_names:
        if not settings.get("project_root"):
            settings["project_root"] = os.path.abspath(os.path.join(os.path.dirname(file_name)))
        try:
            with codecs.open(file_name) as fp:
                try:
                    settings.update(json.load(fp))
                except ValueError:
                    raise ValueError("Failed to parse settings file: %s" % file_name)
        except IOError:
            raise IOError("Failed to open settings file: %s" % file_name)

def get_revision(settings):
    r = svn.local.LocalClient(settings.get("project_root"))
    return r.info().get("commit#revision")

def get_button_folders(limit, settings, data_folder="data"):
    return get_folders(limit, settings, data_folder)

def get_locale_folders(limit, settings, data_folder="locale"):
    return get_folders(limit, settings, data_folder)

def get_pref_folders(limit, settings, data_folder="options"):
    return get_folders(limit, settings, data_folder)

def get_folders(limit, settings, folder):
    """Gets all the folders inside another and applies some filtering to it

    filter maybe the value "all" or a comer seperated list of values

    get_folders(str, str) -> list<str>
    """
    if settings.get("project_root"):
        folder = os.path.join(settings.get("project_root"), folder)
    folders = [file_name for file_name in os.listdir(folder)
               if not file_name.startswith(".")]
    if isinstance(limit, basestring):
        limit = limit.split(",")
    if "all" not in limit:
        folders = list(set(folders).intersection(set(limit)))
    else:
        limits = [item[1:] for item in limit if item[0] == "-"]
        folders = list(folder for folder in folders if folder not in limits)
    return [os.path.join(folder, sub_folder) for sub_folder in folders], folders
