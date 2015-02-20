import getopt
import sys

from builder.build import build_extension, apply_max_version
from config import settings

config = dict(settings.config_default)

config.update({
    "image_path": "/home/michael/Pictures/PastelSVG/png",
    "projects": ("data", "staging", "pre"),
    "extra_options": True,
    "include_icons_for_custom_window": True,
    "fix_meta": True,
    "show_updated_prompt": False,
    "output_folder": "extensions/single",
    "restartless": True,
    "create_menu": True,
    "as_submenu": False,
    "use_keyboard_shortcuts": True,
    "translate_description": True,
    "applications": ["browser", "messenger", "suite"],
    "version": "1.0.4",
})

apply_max_version(config)

buttons = ["addons", "bookmark-manager", "preferences", "bookmark", "snap-back", "restart-app", "about-config", "print-preview", ]

mini_sets = [
    {
     "buttons": ["top-page", "bottom-page"],
     },
    {
     "buttons": ["tb-page-reload", "tb-page-stop", "tb-page-go", "reload-skip-cache", "stop-all", "tb-reload-all-tabs"],
     },
    {
     "buttons": ["tb-cut", "tb-copy", "tb-paste", "select-all", "delete-button", "redo", "undo"],
     },
    {
     "buttons": ["bookmark-manager", "bookmark", "toggle-bookmark-toolbar", "bookmarks-menu-button2", "personal-bookmarks-menu-button", "bookmarks-menu-button1", "bookmark-nopop"],
     },
]

def main():
    opts, args = getopt.getopt(sys.argv[1:], "t:", [])
    opts_table = dict(opts)
    if "-t" in opts_table:
        config["missing_strings"] = "search"
    for button in buttons:
        config["buttons"] = [button]
        config["extension_id"] = "%s-single@codefisher.org" % button
        config["add_to_main_toolbar"] = [button]
        config["current_version_pref"] = 'current.version.%s' % button
        config["chrome_name"] = "%s-toolbar-button" % button
        config["locale_file_prefix"] = "%s_" % button
        build_extension(config)
    

if __name__ == "__main__":
    main()
