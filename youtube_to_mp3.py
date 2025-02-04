import os
import yt_dlp
import datetime
import platform

"""
TODO LIST:

- packaging (as .exe or as bundle of python like a zip)
- tagging mp3. May want to use mutagen library for that
- fix duplicate file naming
- add error when ffmpeg is not present

"""



def youtube_to_mp3(video_id):
    """
    Uses yt_dlp to download a video from YouTube

    The ffmpeg, ffplay, and ffprobe are used for mp3 conversion.
    May not need to have ffplay.
    They need to be in the same directory, or you can edit PATH variable
    (not sure what that is yet)

    ydl_opts is used for configuring the download parameters

    :PARAMS: the youtube video url
    :RETURNS: mp3 file in the same directory as the program

    """

    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        },
            {
              'key': 'FFmpegMetadata',
        }]
    }


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(video_id)

    except Exception as error:
        print(error)
        return False, error

    return True, None



def clean_files():
    """
    Moves the file downloaded to the Downloads folder

    Renames the default ouput from yt_dlp so the name does not contain brackets

    Had to change the date modified and date accessed because it was wrong
    and kept adding to the end of the Downloads folder

    TODO fix the duplicate file naming code
    """

    user = os.getlogin()
    current_path = os.getcwd()

    if platform.system() == "Windows":
        print("Running on Windows")
        download_path = "/Users/" + user + "/Downloads/"

    elif platform.system() == "Linux":
        print("Running on Linux")
        download_path = "/home/" + user + "/Downloads/"

    else:
        print(platform.system())
        print("Unsupported platform: Currently supported on only Linux and Windows")



    pwd = os.listdir()
    for file in pwd:
        if file.endswith(".mp3"):
            left_bracket = file.index("[")
            right_bracket = file.index("]")
            new_name = file[:left_bracket-1] + file[right_bracket + 1:]
            src = current_path + "\\" + file
            dst = download_path + new_name

            file_num = 1
            while os.path.exists(dst):  #loop to rename file end if it already exists (ex filename(1).mp3)
                if file_num == 1:
                    file_num = str(file_num)
                    end = dst[-4:]
                    dst = dst[:-4] + "(" + file_num + ")" + end
                else:
                    file_num = str(file_num)
                    end = dst[-5:]
                    dst = dst[:-6] + file_num + end

                file_num = int(file_num)
                file_num = file_num + 1

            now = datetime.datetime.now().timestamp()
            os.utime(src, (now, now))   #Changes the time modified and the time accessed to present
            os.rename(src, dst)     #renames and moves file
            print("The file was successfully downloaded")


    return



def read_config_file():
    """
    DEPRICATED -- GUI REPLACES IT

    Allows for multiple videos to be downloaded at once
    by using the config file

    File should be parsed by line and any line beginning
    with a pound symbol is ignored
    """


    config_file = "downloader.conf"
    with open(config_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                continue
            else:
                video = line

            youtube_to_mp3(video)
            clean_files()



def main():
    """
    DEPRICATED -- GUI REPLACES IT

    Main program loop
    """

    print("Youtube Audio Downloader")
    print("Use 'q' to exit and 'f' to specify the use of the downloader file \n")

    while True:
        video_url = input("Enter YouTube Video URL: ")
        if video_url == "q":
            break
        elif video_url == "f":
            read_config_file()
            continue


        youtube_to_mp3(video_url)
        clean_files()

if __name__ == "__main__":
    clean_files()
    main()