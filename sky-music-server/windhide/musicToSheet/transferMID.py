import torch
import time

from piano_transcription_inference import PianoTranscription, sample_rate, load_audio


def inference(input_path,output_mid_path,_cuda=False,checkpoint_path=None):
    # Arugments & parameters
    device = 'cuda' if _cuda and torch.cuda.is_available() else 'cpu'

    # Load audio
    (audio, _) = load_audio(input_path, sr=sample_rate, mono=True)

    # Transcriptor
    transcriptor = PianoTranscription(device=device, checkpoint_path=checkpoint_path)

    # Transcribe and write out to MIDI file
    transcribe_time = time.time()
    transcribed_dict = transcriptor.transcribe(audio, output_mid_path)
    print('Transcribe time: {:.3f} s'.format(time.time() - transcribe_time))
