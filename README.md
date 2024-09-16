Here's a `README.md` file for the Chrome Profile Ulauncher Extension:

```markdown
# Chrome Profile Ulauncher Extension

This extension allows you to easily manage and switch between your Google Chrome profiles from within Ulauncher. It lists all your Chrome profiles, including the profile name, email, and icon, and allows you to launch Chrome with the selected profile.

## Features

- **List all Chrome profiles**: Displays a list of profiles based on the configuration stored in `~/.config/google-chrome`.
- **Search Profiles**: Search for profiles by name or email.
- **Quick Profile Launch**: Select a profile and quickly open Chrome using that profile.

## Requirements

- [Ulauncher](https://ulauncher.io/)
- [Google Chrome](https://www.google.com/chrome/)
- `python-gi` for GTK3 support.
- `ripgrep` or any other searching tool for faster search (optional).

## Installation

1. Install Ulauncher if it's not already installed:

   ```bash
   sudo add-apt-repository ppa:agornostal/ulauncher && sudo apt update && sudo apt install ulauncher
   ```

2. Install `python-gi` for GTK3 support:

   ```bash
   sudo apt-get install python3-gi
   ```

3. Clone this repository to your Ulauncher extensions folder:

   ```bash
   mkdir -p ~/.config/ulauncher/extensions
   cd ~/.config/ulauncher/extensions
   git clone https://github.com/your-repo/chrome-profile-ulauncher-extension.git
   ```

4. Restart Ulauncher:

   ```bash
   ulauncher --no-extensions --dev
   ```

## Usage

1. Launch Ulauncher using `Ctrl + Space` (or the configured shortcut).
2. Type the keyword associated with this extension (e.g., `chrome-profile`) to trigger the extension.
3. A list of Chrome profiles will appear, showing the profile name, email, and associated profile picture.
4. You can search for a profile by name or email.
5. Select a profile to launch Chrome using that profile.

## Development

To modify this extension:

1. Make changes to the Python files as needed.
2. Run the extension locally by restarting Ulauncher in development mode:

   ```bash
   ulauncher --no-extensions --dev
   ```

3. Test the changes by triggering the extension through Ulauncher.

## Known Issues

- The extension currently only works with Chrome profiles stored under `~/.config/google-chrome`.
- If profile directories are missing or inaccessible, the extension might fail to list some profiles.
- The extension relies on `google-chrome` being installed and available via the `which` command. Ensure Google Chrome is properly installed on your system.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change.
```

### Key Points:
- It includes an overview of the extension's features.
- Detailed installation instructions.
- Guidance on how to use the extension in Ulauncher.
- Mention of dependencies like `python-gi`.
- Suggestions for how to contribute or develop further.