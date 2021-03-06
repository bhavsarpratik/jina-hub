import os
import shutil
import numpy as np
from .. import BigTransferEncoder
from jina.executors.metas import get_default_metas
from jina.executors import BaseExecutor


def rm_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, ignore_errors=False, onerror=None)


def get_encoder():
    metas = get_default_metas()
    if 'JINA_TEST_GPU' in os.environ:
        metas['on_gpu'] = True
    return BigTransferEncoder(model_path='pretrained', channel_axis=1, metas=metas)




# def test_encoding_results():
#     input_dim = 48
#     output_dim = 2048
#     encoder = get_encoder()
#     test_data = np.random.rand(2, 3, input_dim, input_dim)
#     encoded_data = encoder.encode(test_data)
#     assert encoded_data.shape == (2, output_dim)
#     rm_files([encoder.save_abspath, encoder.config_abspath])
#
#
# def test_save_and_load():
#     encoder = get_encoder()
#     encoder.touch()
#     encoder.save()
#     assert os.path.exists(encoder.save_abspath)
#     encoder_loaded = BaseExecutor.load(encoder.save_abspath)
#     assert encoder_loaded.channel_axis == encoder.channel_axis
#     rm_files([encoder.save_abspath, encoder.config_abspath])


def test_save_and_load_config():
    encoder = get_encoder()
    encoder.save_config()
    assert os.path.exists(encoder.config_abspath)
    encoder_loaded = BaseExecutor.load_config(encoder.config_abspath)
    assert encoder_loaded.model_path == encoder.model_path
    # rm_files([encoder.save_abspath, encoder.config_abspath])