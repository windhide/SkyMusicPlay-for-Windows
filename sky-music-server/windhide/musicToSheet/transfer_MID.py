from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save
from windhide.utils.play_path_util import getResourcesPath

def inference(input_path):
    output_midi_path = getResourcesPath("translateMID")
    try:
        predict_and_save([  input_path ],
            output_midi_path,
            True,
            False,
            False,
            False,
            ICASSP_2022_MODEL_PATH
        )
    except Exception as e:
        print(e)
