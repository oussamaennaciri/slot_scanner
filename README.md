# Slot Scanner

This is an automated script to check the earliest available DMV appointments across multiple locations near Denver, Colorado.  
It is specifically designed for first-time license or ID applications.

When an appointment in **May** is found, the script will:
- Alert you in the terminal
- Open the DMV website in your browser
- Play an audio file (`alarm.mp3`) to notify you

---

## Features

- ✅ Checks multiple locations asynchronously using Playwright
- ✅ Detects earliest available date for "First Time CO DL/ID/Permit"
- ✅ Plays a sound and opens the browser when a May appointment is found
- ✅ Stops searching when May 16th is available

---

## Requirements

- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- Audio file named `alarm.mp3` in the same directory
- macOS (for the `afplay` command to play audio)

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/colorado-dmv-checker.git
   cd colorado-dmv-checker
   ```

2. Install dependencies:
   ```bash
   pip install playwright
   playwright install
   ```

3. Make sure the alarm file is present:
   - File required: `alarm.mp3`

---

## Usage

Run the script using Python 3.8+:

```bash
python your_script_name.py
```

Make sure your terminal supports `asyncio` (e.g., VS Code, Terminal on macOS).

---

## Configuration

To use this script for other purposes (e.g., different services or locations), modify:
- The `locations_to_check` list
- The selector for the type of service (currently: "First Time CO DL/ID/Permit")

---

## License

This project is licensed for personal and non-commercial use only.  
See [LICENSE](./LICENSE) for full terms.
