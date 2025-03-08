import yt_dlp
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sqlite3
import os

# Get system's default download path
def get_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")

# Database setup
def setup_db():
    conn = sqlite3.connect("download_history.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history
                      (id INTEGER PRIMARY KEY, title TEXT, url TEXT, filepath TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# Function to save history
def save_to_history(title, url, filepath, status):
    conn = sqlite3.connect("download_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (title, url, filepath, status) VALUES (?, ?, ?, ?)",
                   (title, url, filepath, status))
    conn.commit()
    conn.close()

# Fetch history
def fetch_history():
    conn = sqlite3.connect("download_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, url, filepath, status FROM history")
    data = cursor.fetchall()
    conn.close()
    return data

# Global variable to store downloader instance and track active download
downloader = None
download_in_progress = False

# Download logic
def download_video(url, progress_label, progress_bar, speed_label, cancel_btn):
    global downloader, download_in_progress
    download_in_progress = True
    
    class MyLogger:
        def __init__(self):
            self.cancelled = False
        
        def debug(self, msg):
            pass
        
        def warning(self, msg):
            pass
        
        def error(self, msg):
            print(msg)
        
        def hook(self, d):
            if self.cancelled:
                raise Exception("Download Cancelled")
            
            if d['status'] == 'downloading':
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes', 1)
                speed = d.get('speed', 0)  # Speed in bytes/s
                speed_kb = speed / 1024  # Convert to KB/s
                speed_mb = speed_kb / 1024  # Convert to MB/s
                percent = (downloaded_bytes / total_bytes) * 100
                progress_label.config(text=f"Downloading: {percent:.2f}%")
                speed_label.config(text=f"Speed: {speed_kb:.2f} KB/s ({speed_mb:.2f} MB/s)")
                progress_bar['value'] = percent
            elif d['status'] == 'finished':
                progress_label.config(text="Download Complete!")
                speed_label.config(text="Speed: 0 KB/s (0.00 MB/s)")
                save_to_history(d['info_dict']['title'], url, d['info_dict']['filepath'], "Completed")
                refresh_history()
                cancel_btn.config(state=tk.DISABLED)
                download_in_progress = False
    
    download_path = get_download_path()
    logger = MyLogger()
    downloader = logger
    
    options = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'logger': logger,
        'progress_hooks': [logger.hook]
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        progress_label.config(text="Download Cancelled")
        speed_label.config(text="Speed: 0 KB/s (0.00 MB/s)")
        cancel_btn.config(state=tk.DISABLED)
        download_in_progress = False

# Start download in a thread
def start_download():
    global download_in_progress
    if download_in_progress:
        messagebox.showwarning("Warning", "A download is already in progress!")
        return
    
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a video link! 📎")
        return
    
    for widget in progress_frame.winfo_children():
        widget.destroy()
    
    progress_label = ttk.Label(progress_frame, text="Starting download...")
    progress_label.pack()
    
    progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
    progress_bar.pack()
    
    speed_label = ttk.Label(progress_frame, text="Speed: 0 KB/s (0.00 MB/s)")
    speed_label.pack()
    
    cancel_btn = tk.Button(progress_frame, text="Cancel", command=cancel_download)
    cancel_btn.pack()
    
    threading.Thread(target=download_video, args=(url, progress_label, progress_bar, speed_label, cancel_btn), daemon=True).start()

# Cancel download
def cancel_download():
    global downloader, download_in_progress
    if downloader:
        downloader.cancelled = True
    download_in_progress = False

# Refresh history list
def refresh_history():
    history_list.delete(*history_list.get_children())
    for item in fetch_history():
        history_list.insert("", "end", values=item)

# GUI Setup
root = tk.Tk()
root.title("Advanced Video Downloader ⬇️")
root.geometry("600x400")

setup_db()

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter Video URL 📎:").grid(row=0, column=0, padx=5)
url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, padx=5)

download_btn = tk.Button(frame, text="Download ⬇️", command=start_download)
download_btn.grid(row=0, column=2, padx=5)

progress_frame = tk.Frame(root)
progress_frame.pack(pady=10)

history_frame = tk.LabelFrame(root, text="Download History")
history_frame.pack(fill="both", expand="yes", padx=10, pady=10)

history_list = ttk.Treeview(history_frame, columns=("Title", "URL", "Path", "Status"), show="headings")
for col in ("Title", "URL", "Path", "Status"):
    history_list.heading(col, text=col)
    history_list.column(col, width=150)
history_list.pack(fill="both", expand=True)

refresh_history()
root.mainloop()