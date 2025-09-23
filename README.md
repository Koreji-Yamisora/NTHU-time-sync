# Group Free Time Scheduler

## Usage
```bash
python main.py
```

## Building Releases

This project includes GitHub Actions for automated cross-platform builds. When you push a version tag, it will automatically build Windows and macOS executables.

### Creating a Release

1. **Using the helper script** (recommended):
   ```bash
   python create_release.py 1.0.0
   ```

2. **Manual method**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

### What Happens

When you push a version tag (like `v1.0.0`), GitHub Actions will:

1. Build a Windows executable (`scheduler-windows-v1.0.0.exe`)
2. Build a macOS application bundle (`scheduler-macos-v1.0.0.zip`)
3. Create a GitHub release with both files attached

### Requirements

- The tag must start with `v` (e.g., `v1.0.0`, `v2.1.3`)
- You must be on the `main` branch
- All changes should be committed before creating the release

### Monitoring Builds

You can monitor the build progress at: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
