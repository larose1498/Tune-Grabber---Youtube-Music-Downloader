# Tune-Grabber---Youtube-Music-Downloader
Downloads Youtube videos as mp3 files

Basic GUI is included by default, but you can use the CLI program by using youtube-to-mp3.py by itself

In order for this to work, you must have python 3.12 or higher (older version may work, but no guarantee).
This is built heavily on yt_dlp

## Local Executable 

- Get all the files for your corresponding os
- Get all the zip files (ffmpeg, ffplay, and ffprobe) and unzip them
- Put all the files in the same directory of your choosing
- Run mainfile to run the program
- Optionally create a shortcut

#### If Using Linux
- Use chmod -x on mainfile

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

#### IF you want to compile this yourself in linux, you may need to run:

pyinstaller mainfile.py \
  --collect-submodules PIL \
  --collect-data PIL --onefile

