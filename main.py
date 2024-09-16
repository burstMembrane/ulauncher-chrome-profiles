import profile
import subprocess as sp
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.event import (
    KeywordQueryEvent,
    ItemEnterEvent,
)
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
import logging
from pathlib import Path
from dataclasses import dataclass
from json import load, JSONDecodeError

logger = logging.getLogger(__name__)


@dataclass
class ChromeProfile:
    name: str
    email: str
    icon_path: Path
    profile_folder: Path


class ChromeProfileExtension(Extension):
    """Main Extension Class"""

    def __init__(self):
        """Initializes the extension"""
        super(ChromeProfileExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

        self.config_folder: Path = Path.home() / ".config" / "google-chrome"
        self.chrome_path = (
            sp.Popen(["which", "google-chrome"], stdout=sp.PIPE)
            .communicate()[0]
            .decode()
            .strip()
        )

        # Initialize profiles once
        self.profiles = self.get_profiles()

    def get_profiles(self):
        """Get the chrome profiles"""
        profiles = []
        profile_folders = [
            self.config_folder / "Default",
            *[
                x
                for x in self.config_folder.iterdir()
                if x.is_dir() and x.name.startswith("Profile")
            ],
        ]

        for profile_folder in profile_folders:
            pref_file = profile_folder / "Preferences"
            if not pref_file.exists():
                continue

            try:
                with pref_file.open() as f:
                    prefs = load(f)
            except (JSONDecodeError, PermissionError) as e:
                logger.error(f"Error reading preferences: {e}")
                continue

            account_info_list = prefs.get("account_info", [])
            if not account_info_list or not isinstance(account_info_list, list):
                continue

            account_info = account_info_list[0] if account_info_list else {}
            if not account_info:
                continue

            name = account_info.get("full_name")
            email = account_info.get("email")

            if not name or not email:
                continue

            icon_path = profile_folder / "Google Profile Picture.png"
            profile = ChromeProfile(name, email, icon_path, profile_folder)
            profiles.append(profile)

        return profiles

    def open_chrome(self, profile_folder: Path):
        """Open chrome with the selected profile"""
        cmd = [self.chrome_path, f"--profile-directory={profile_folder.name}"]
        sp.Popen(cmd)
        return DoNothingAction()


class KeywordQueryEventListener(EventListener):
    """Listener that handles user input"""

    def sort_profiles(self, profiles, query):
        """Sort profiles based on query"""
        query = query.lower()
        return sorted(
            profiles,
            key=lambda x: (
                query in x.name.lower(),
                query in x.email.lower(),
                x.name.lower(),
            ),
            reverse=True,
        )

    def on_event(self, event, extension):
        # Filter profiles based on user query
        query = event.get_argument() or ""
        profiles = extension.profiles

        profiles = self.sort_profiles(profiles, query)

        items = [
            ExtensionResultItem(
                icon=(
                    str(profile.icon_path)
                    if profile.icon_path.exists()
                    else "images/icon.png"
                ),
                name=profile.name,
                description=profile.email,
                on_enter=ExtensionCustomAction(
                    {
                        "action": "open_chrome",
                        "profile_folder": profile.profile_folder,
                    },
                    keep_app_open=False,
                ),
            )
            for profile in profiles
        ]

        if not items:
            items.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="No profiles found",
                    on_enter=DoNothingAction(),
                )
            )

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        action = data["action"]
        if action == "open_chrome":
            profile_folder = data["profile_folder"]
            return extension.open_chrome(profile_folder)


if __name__ == "__main__":
    ChromeProfileExtension().run()
