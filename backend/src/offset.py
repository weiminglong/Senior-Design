import argparse
import io

#local
def transcribe_file_with_word_time_offsets(speech_file):
    """Transcribe the given audio file synchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        audio_channel_count = 2,
        language_code='en-US',
        enable_word_time_offsets=True)

    response = client.recognize(config, audio)

    for result in response.results:
        alternative = result.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))
        with open("Output1.txt", "a") as text_file:
            text_file.write(u'{} '.format(alternative.transcript))


        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds, #+ start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))
            with open('time.csv', 'a') as csv_file:
                csv_file.write('word:{} start_time:{}:{} end_time:{}:{}\n'.format(
                word,
                int(start_time.seconds)//60, #+ start_time.nanos * 1,
                int(start_time.seconds)%60,
                end_time.seconds//60,
                end_time.seconds%60))

#cloud storage
def transcribe_gcs_with_word_time_offsets(gcs_uri):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,#FLAC
        sample_rate_hertz=44100,#16000
        audio_channel_count = 2,
        language_code='en-US',
        #enableSpeakerDiarization = True,
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=900)

    for result in result.results:
        alternative = result.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))
        #print('Confidence: {}'.format(alternative.confidence))
        with open("Output1.txt", "a") as text_file:
                    text_file.write(u'{} '.format(alternative.transcript))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('word: {}, start_time: {}, end_time: {}'.format(
                word,
                int(start_time.seconds), #+ start_time.nanos * 1,
                end_time.seconds + end_time.nanos * 1e-9))
            with open('time.csv', 'a') as csv_file:
                csv_file.write('word:{} start_time:{}:{} end_time:{}:{}\n'.format(
                word,
                int(start_time.seconds)//60, #+ start_time.nanos * 1,
                int(start_time.seconds)%60,
                end_time.seconds//60,
                end_time.seconds%60))

#


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs_with_word_time_offsets(args.path)
    else:
        transcribe_file_with_word_time_offsets(args.path)
