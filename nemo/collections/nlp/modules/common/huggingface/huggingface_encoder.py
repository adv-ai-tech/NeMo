# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nemo.collections.nlp.modules.common.huggingface.huggingface_utils import get_huggingface_pretrained_lm_models_list
from typing import Optional
from nemo.collections.nlp.modules.common.encoder_module import EncoderModule
from nemo.utils import logging
from transformers import AutoConfig, AutoModel
from hydra.utils import instantiate


class HuggingFaceEncoderModule(EncoderModule):
    """ Class for using HuggingFace encoders in NeMo NLP."""

    def __init__(
        self,
        model_name: Optional[str] = None,
        pretrained: bool = False,
        config_dict: Optional[dict] = None,
        checkpoint_file: Optional[str] = None,
    ):
        super().__init__()

        # TODO: argument correctness checker

        model = None
        if model_name is not None:
            if model_name in get_huggingface_pretrained_lm_models_list():
                if pretrained:
                    model = AutoModel.from_pretrained(model_name)
                else:
                    cfg = AutoConfig.from_pretrained(model_name)
                    model = AutoModel.from_config(cfg)
            else:
                logging.error(f'{model_name} not found in list of HuggingFace pretrained models')
        else:
            cfg = instantiate(config_dict)
            model = AutoModel.from_config(cfg)
        self._hidden_size = model.config.hidden_size
        self._vocab_size = model.config.vocab_size

        self._encoder = model

    # @typecheck()
    def forward(self, input_ids, encoder_mask):
        encoder_hidden_states = self._encoder.forward(input_ids=input_ids, attention_mask=encoder_mask)[0]
        return encoder_hidden_states

    @property
    def hidden_size(self) -> Optional[int]:
        return self._hidden_size

    @property
    def vocab_size(self) -> Optional[int]:
        return self._vocab_size
