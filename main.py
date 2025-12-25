import os
import threading
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog
from moviepy import VideoFileClip


app = tb.Window(themename="flatly")
app.title("Extract Audio from Video")
app.geometry("560x420")
app.resizable(False, False)

video_path_var = tb.StringVar()
output_dir_var = tb.StringVar()
status_var = tb.StringVar(value="Select a video and output folder")


def select_video():
    path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov")],
    )
    if path:
        video_path_var.set(path)
        check_ready()


def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_dir_var.set(folder)
        check_ready()


def check_ready():
    if video_path_var.get() and output_dir_var.get():
        extract_btn.config(state=NORMAL)
        status_var.set("Ready to extract audio")


def extract_audio():
    extract_btn.config(state=DISABLED)
    progress.start(10)
    status_var.set("Extracting audio...")

    threading.Thread(target=process_audio, daemon=True).start()


def process_audio():
    try:
        video_path = video_path_var.get()
        output_dir = output_dir_var.get()

        video = VideoFileClip(video_path)

        filename = os.path.splitext(os.path.basename(video_path))[0]
        output_audio = os.path.join(output_dir, filename + ".mp3")

        video.audio.write_audiofile(output_audio)
        video.close()

        status_var.set("Audio extracted successfully!")

    except Exception as e:
        status_var.set(f"Error: {str(e)}")

    finally:
        progress.stop()
        extract_btn.config(state=NORMAL)


tb.Label(
    app,
    text="Audio Extractor",
    font=("Segoe UI", 20, "bold"),
).pack(pady=15)

card = tb.Frame(app, padding=20)
card.pack(fill=X, padx=20)

# Video selection
tb.Label(card, text="Video File").pack(anchor=W)
tb.Entry(card, textvariable=video_path_var, width=60).pack(pady=5)
tb.Button(
    card,
    text="Browse Video",
    command=select_video,
    bootstyle=PRIMARY,
).pack(pady=5)

# Output folder
tb.Label(card, text="Output Folder").pack(anchor=W, pady=(15, 0))
tb.Entry(card, textvariable=output_dir_var, width=60).pack(pady=5)
tb.Button(
    card,
    text="Browse Folder",
    command=select_output_folder,
    bootstyle=PRIMARY,
).pack(pady=5)

# Extract button
extract_btn = tb.Button(
    app,
    text="Extract Audio",
    bootstyle=SUCCESS,
    width=25,
    state=DISABLED,
    command=extract_audio,
)
extract_btn.pack(pady=15)

# Progress bar
progress = tb.Progressbar(
    app,
    mode="indeterminate",
    length=400,
)
progress.pack(pady=10)

# Status label
tb.Label(
    app,
    textvariable=status_var,
    font=("Segoe UI", 10),
).pack(pady=10)


app.mainloop()
