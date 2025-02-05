# Tune-Grabber---Youtube-Music-Downloader
Downloads Youtube videos as mp3 files

Basic GUI is included by default, but you can use the CLI program by using youtube-to-mp3.py by itself

In order for this to work, you must have python 3.12 or higher (older version may work, but no guarantee).
This is built heavily on yt_dlp

## Local Executable 

- Use the linux app with ffmpeg, ffplay, and ffprobe in the same directory
#### OR
- Use the windows app with ffmpeg, ffplay, and ffprobe in the same directory

#### AND
- Optionally create a shortcut

## Manual Instructions for Python Environments

### --WINDOWS USERS--

- Install python for command line from Microsoft Store

Run the following commands in command prompt:
```
python3 -m pip install yt_dlp.
python3 -m pip install --upgrade yt_dlp.
cd FILE_LOCATION
python3 Tune-Grabber.py
```

Optionally create .bat file to automate last two steps. Sample .bat is provided

### --LINUX USERS--

Run the following commands in the bash:
```
sudo apt update
sudo apt upgrade
sudo apt install yt-dlp
cd FILE_LOCATION
python3 Tune-Grabber.py
```

Optionally create script to automate last two steps.

#### IF YOU ARE USING UBUNTU, you may need to run
```
sudo apt install python3-tk
```
This is the tkinter library, which for most Python installations is included by default, but some Ubuntu Python packages
may not include it by default.
