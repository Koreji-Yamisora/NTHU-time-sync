# Group Free Time Scheduler

A modern, cross-platform desktop application for managing schedules and finding common free times among groups of people. Built with Python and PyQt6, featuring an intuitive GUI and automated cross-platform builds.

## Features

- **Schedule Management**: Add and manage people with their individual schedules
- **Course Integration**: Track courses and their time slots
- **Common Time Finder**: Automatically identify overlapping free time slots
- **JSON Data Operations**: 
  - Save encrypted data for security
  - Export plain JSON for sharing
  - Open both encrypted and plain JSON files
  - Create blank schedules on first run
- **Modern GUI**: Clean, intuitive interface built with PyQt6
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **One-Click Builds**: Automated executable generation for easy distribution

## Quick Start

### Download Pre-built Executable (Recommended)

**Note**: This repository is currently private. Pre-built executables are available through the automated release system.

1. **Go to the Releases page** (requires repository access):
   - [**Original Repository**](https://github.com/IcyB1ue/Time-Table-Intersection-for-NTHU/releases) - `IcyB1ue/Time-Table-Intersection-for-NTHU`
   - [**NTHU-time-sync**](https://github.com/Koreji-Yamisora/NTHU-time-sync/releases) - `Koreji-Yamisora/NTHU-time-sync`
2. **Download the appropriate file** for your operating system:
   - **Windows**: `scheduler-windows-v*.exe` (latest version)
   - **macOS**: `scheduler-macos-v*.zip` (extract and run the `.app` file)
3. **Run the executable** - no installation required!

## JSON Data Operations

The application uses JSON files to store and manage schedule data. Here's how to work with them:

### **File Operations (Menu Bar & Toolbar)**
- **New**: Create a blank schedule (creates `schedule_data.json`)
- **Open...**: Load an existing JSON file (supports both encrypted and plain JSON)
- **Save**: Save current data in encrypted JSON format
- **Save As...**: Save current data with a new filename (encrypted)
- **Export...**: Export current data as plain JSON (unencrypted)

### **Data File Handling**
- **First Run**: If no `schedule_data.json` exists, the app creates a blank one
- **File Selection**: Use "Open..." to select any JSON file from your system
- **Encryption**: Save/Save As automatically encrypts your data for security
- **Compatibility**: Open recognizes both encrypted and plain JSON files

### **Security Features**
- **Encrypted Saves**: Your data is automatically encrypted when using Save/Save As
- **Plain Exports**: Use Export for sharing or backup (unencrypted)
- **Auto-Detection**: Open automatically detects and handles both formats

## Usage

### GUI Mode (Default)
When you run the application, it will launch the graphical interface where you can:
- Add people and their schedules
- Manage courses and time slots
- View common free times in an intuitive table format
- Import/export schedule data

### Console Mode
The application also supports console mode for quick operations:
- View all schedules
- Find common free times
- Access the GUI from the command line

## Requirements

- **Python**: 3.13 or higher
- **Dependencies**:
  - PyQt6 >= 6.9.1 (GUI framework)
  - PyInstaller >= 6.15.0 (for building executables)

## Issues & Support

- **Bug Reports**: Create an issue (requires repository access)
- **Feature Requests**: Start a discussion (requires repository access)
- **Questions**: Ask in discussions (requires repository access)

## Version History

- **Latest**: Removed embedded JSON, added encryption/decryption, optimized with uv
- **v2.0.x**: Fixed Windows executable attachment in releases
- **v2.0.0**: Added automated cross-platform builds with GitHub Actions
- **v0.1.0**: Initial release with basic schedule management

---

## Development

### Project Structure
```
scheduler/
├── main.py              # Main application entry point
├── gui/                 # GUI components
│   ├── main_window.py   # Main window
│   ├── schedule_tab.py  # Schedule management
│   ├── people_tab.py    # People management
│   └── ...
├── models.py            # Data models
├── storage.py           # Data persistence
├── schedule.py          # Schedule logic
└── main.spec           # PyInstaller configuration
```

### Building from Source

**Prerequisites:**
- Python 3.13 or higher
- uv package manager (install from https://docs.astral.sh/uv/getting-started/installation/)

**Installation:**
```bash
# Clone the repository (requires repository access)
git clone https://github.com/IcyB1ue/Time-Table-Intersection-for-NTHU.git
cd Time-Table-Intersection-for-NTHU

# Install dependencies and create virtual environment
uv sync

# Run the application
uv run python main.py
```

**Build Executable:**
```bash
# Install build dependencies
pip install pyinstaller

# Build executable
pyinstaller main.spec
```

The built executable will be available in the `dist/` directory.

## Automated Releases

This project includes GitHub Actions for automated cross-platform builds. When you push a version tag, it automatically builds Windows and macOS executables.

### Creating a Release

**Using the helper script (recommended):**
```bash
python create_release.py 2.1.0
```

**Manual method:**
```bash
git tag v2.1.0
git push origin v2.1.0
```

### Release Process

When you push a version tag (like `v2.1.0`), GitHub Actions will:

1. **Build Windows executable** (`scheduler-windows-v*.exe`)
2. **Build macOS application bundle** (`scheduler-macos-v*.zip`)
3. **Create a GitHub release** with both files attached
4. **Generate release notes** with download instructions

### Requirements for Releases

- Tag must start with `v` (e.g., `v1.0.0`, `v2.1.3`)
- Must be on the `main` branch
- All changes should be committed before creating the release

### Monitoring Builds

Track build progress at: Actions page (requires repository access)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is currently private. Please check the repository for license details.

---

**Made for efficient schedule management**