# Advanced Video Downloader

## Description
Advanced Video Downloader is a GUI-based application that allows users to download videos from provided URLs with a real-time progress tracker, download speed display (in KB/s and MB/s), and a download history section. It ensures that only one active download runs at a time and allows users to cancel a download in progress.

## Features
- GUI built using Tkinter
- Video downloading using `yt-dlp`
- Live download progress tracking
- Display of real-time download speed
- Download history tracking
- Downloaded files are stored in the system's default **Downloads** folder
- Ability to cancel ongoing downloads

## Dependencies
Ensure the following dependencies are installed before running the application:

- Python 3.x
- `yt-dlp`
- `tkinter` (comes pre-installed with Python)
- `sqlite3` (comes pre-installed with Python)

### Installation of Dependencies
Run the following command to install missing dependencies:
```bash
pip install yt-dlp
```

## Installation & Usage

### Linux (.DEB Package)
For Linux users, you can install the `.deb` package by running:
```bash
sudo dpkg -i all-video-downloader.deb
```
Once installed, you can launch it from the applications menu.

### Windows (.EXE File)
For Windows users, the `.exe` file can be executed directly by double-clicking the `downld.exe` file.

## Setup for Development
1. Clone the repository:
   ```bash
   git clone https://github.com/Sammymullern/all-video-downloader.git
   cd advanced-video-downloader
   ```
2. Run the Python script:
   ```bash
   python downld.py
   ```

## Maintainer
**Samson Akach**  
Email: [mullerncybert@gmail.com](mailto:mullerncybert@gmail.com)


