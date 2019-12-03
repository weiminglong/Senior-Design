import os
from gcloud import storage
#import script
import upload
import offset


def convert_auto():
    #gcloud authetification
    #os.system("export GOOGLE_APPLICATION_CREDENTIALS=\"/Users/mike/credentials/cloudkey.json\"")
    #script.printHello()

    #path variables
    videoPath = 'video/'
    audioPath = 'audio/'
    txtPath = 'txt/'

    #gcloud storage variables
    bucket = 'qaclassifier'
    fileName = 'Taxonomy Biology'#'Mitochondria'
    audioFile = 'Taxonomy Biology.flac'#'Mitochondria.flac'

    #ffmpeg extract audio from video
    os.system('ffmpeg -i video/Taxonomy.mp4 -f flac -ac 2 -vn ' + audioPath + audioFile)

    #call upload function in upload.py
    upload.upload_blob(bucket, audioPath + audioFile, audioFile)

    #call transcribe function in offset.py
    offset.transcribe_gcs_with_word_time_offsets('gs://' + bucket + '/' + audioFile, fileName)

    #os way
    #os.system('python offset.py gs://' + bucket + '/' + audioFile)
