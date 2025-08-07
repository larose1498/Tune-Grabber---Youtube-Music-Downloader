import os
import yt_dlp
import datetime

"""
TODO LIST:

- packaging (as .exe or as bundle of python like a zip)
- tagging mp3. May want to use mutagen library for that
- fix duplicate file naming
- add error when ffmpeg is not present

"""



def youtube_to_mp3(video_id, ini):
    """
    Uses yt_dlp to download a video from YouTube

    The ffmpeg, ffplay, and ffprobe are used for mp3 conversion.
    May not need to have ffplay.
    They need to be in the same directory, or you can edit PATH variable
    (not sure what that is yet)

    ydl_opts is used for configuring the download parameters

    :PARAMS: the youtube video url, the ini data object for settings
    :RETURNS: mp3 file in the same directory as the program

    """

    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'noplaylist': bool(ini.find_value("NoPlaylist")),
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': ini.find_value("AudioQuality"),
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



def clean_files(ini):
    """
    Moves the file downloaded to the Downloads folder

    Renames the default ouput from yt_dlp so the name does not contain brackets

    Had to change the date modified and date accessed because it was wrong
    and kept adding to the end of the Downloads folder

    PARAM: the ini settings object

    TODO fix the duplicate file naming code
    TODO move the os detection to somewhere else
    TODO add protections and warnings if the user trys to move to a folder that doesn't exist
    """
    current_path = os.getcwd()


    pwd = os.listdir()
    for file in pwd:
        if file.endswith(".mp3"):
            left_bracket = file.index("[")
            right_bracket = file.index("]")
            new_name = file[:left_bracket-1] + file[right_bracket + 1:]
            src = current_path + "/" + file
            dst = ini.find_value("DownloadPath") + "/" + new_name

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
            print(src)
            print(dst)
            os.utime(src, (now, now))   #Changes the time modified and the time accessed to present
            os.rename(src, dst)     #renames and moves file
            print("The file was successfully downloaded")


