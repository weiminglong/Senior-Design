import os
from gcloud import storage
#import script
import upload
import offset


def convert_auto(title, video_name, video_url):
    # gcloud authetification
    # os.system("export GOOGLE_APPLICATION_CREDENTIALS=\"/Users/mike/credentials/cloudkey.json\"")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/mike/credentials/cloudkey.json"
    # script.printHello()

    # path variables
    videoPath = 'video/'
    audioPath = 'audio/'
    txtPath = 'txt/'

    # gcloud storage variables
    bucket = 'qaclassifier'
    fileName = title  # change to title
    audioFile = title + '.flac'  # change this to title + .flac

    print(fileName)
    print(audioFile)
    print('ffmpeg -i video/' + video_name + ' -f flac -ac 2 -vn ' + audioPath + audioFile)

    # ffmpeg extract audio from video
    os.system('ffmpeg -i video/' + video_name + ' -f flac -ac 2 -vn ' + audioPath + audioFile)  # remove hard coded .mp4 and use video name

    # call upload function in upload.py
    upload.upload_blob(bucket, audioPath + audioFile, audioFile)

    # call transcribe function in offset.py
    offset.transcribe_gcs_with_word_time_offsets('gs://' + bucket + '/' + audioFile, fileName, video_url)

    # os way
    # os.system('python offset.py gs://' + bucket + '/' + audioFile)

if __name__ == '__main__':
    title = 'Taxonomy'
    video_name = 'Taxonomy.mp4'
    video_url = "https://qa-classifier.s3.amazonaws.com/Taxonomy.mp4"
    convert_auto(title, video_name, video_url)
