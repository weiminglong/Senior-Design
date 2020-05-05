import os
import upload
import offset


def convert_auto(title, video_name, video_url, category):
    # gcloud authentication
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Add Cloud Key"

    # path variables
    audio_path = 'audio/'

    # gcloud storage variables
    bucket = 'qaclassifier'
    file_name = title  # change to title
    audio_file = title + '.flac'  # change this to title + .flac

    print(file_name)
    print(audio_file)
    print('ffmpeg -i video/' + video_name + ' -f flac -ac 2 -vn ' + audio_path + audio_file)

    # ffmpeg extract audio from video
    os.system('ffmpeg -i video/' + video_name + ' -f flac -ac 2 -vn ' + audio_path + audio_file)  # remove hard coded .mp4 and use video name

    # call upload function in upload.py
    upload.upload_blob(bucket, audio_path + audio_file, audio_file)

    # call transcribe function in offset.py
    offset.transcribe_gcs_with_word_time_offsets('gs://' + bucket + '/' + audio_file, file_name, video_url, category)
