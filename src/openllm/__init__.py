# Copyright 2023 BentoML Team. All rights reserved.
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
"""
OpenLLM
=======

An open platform for operating large language models in production. Fine-tune, serve,
deploy, and monitor any LLMs with ease.

* Built-in support for StableLM, Llama, Dolly, Flan-T5, Vicuna
* Option to bring your own fine-tuned LLMs
* Online Serving with HTTP, gRPC, SSE(coming soon) or custom API
* Native integration with BentoML and LangChain for custom LLM apps
"""
from __future__ import annotations

import logging
import os
import typing as t
import warnings

from . import utils as utils
from .__about__ import __version__ as __version__
from .exceptions import MissingDependencyError


if utils.DEBUG:
    utils.set_debug_mode(True)
    utils.set_quiet_mode(False)

    utils.configure_logging()
    logging.basicConfig(level=logging.NOTSET)
else:
    # configuration for bitsandbytes before import
    os.environ["BITSANDBYTES_NOWELCOME"] = os.environ.get("BITSANDBYTES_NOWELCOME", "1")
    # The following warnings from bitsandbytes, and probably not that important
    # for users to see when DEBUG is False
    warnings.filterwarnings(
        "ignore", message="MatMul8bitLt: inputs will be cast from torch.float32 to float16 during quantization"
    )
    warnings.filterwarnings(
        "ignore", message="MatMul8bitLt: inputs will be cast from torch.bfloat16 to float16 during quantization"
    )
    warnings.filterwarnings(
        "ignore",
        message=(
            "The installed version of bitsandbytes was compiled without GPU support. 8-bit optimizers and GPU quantization"
            " are unavailable."
        ),
    )


_import_structure = {
    "_llm": ["LLM", "Runner", "LLMRunner"],
    "_configuration": ["LLMConfig"],
    "_package": ["build"],
    "exceptions": [],
    "_schema": ["GenerationInput", "GenerationOutput", "MetadataOutput"],
    "utils": [],
    "models": [],
    "client": [],
    "playground": [],
    "tests": [],
    "cli": ["start", "start_grpc"],
    # NOTE: models
    "models.auto": [
        "AutoConfig",
        "CONFIG_MAPPING",
        "MODEL_MAPPING_NAMES",
        "MODEL_FLAX_MAPPING_NAMES",
        "MODEL_TF_MAPPING_NAMES",
    ],
    "models.flan_t5": ["FlanT5Config"],
    "models.dolly_v2": ["DollyV2Config"],
    "models.falcon": ["FalconConfig"],
    "models.chatglm": ["ChatGLMConfig"],
    "models.starcoder": ["StarCoderConfig"],
    "models.stablelm": ["StableLMConfig"],
    "models.opt": ["OPTConfig"],
}

# NOTE: torch and cpm_kernels
try:
    if not (utils.is_torch_available() and utils.is_cpm_kernels_available()):
        raise MissingDependencyError
except MissingDependencyError:
    from .utils import dummy_pt_and_cpm_kernels_objects

    _import_structure["utils.dummy_pt_and_cpm_kernels_objects"] = [
        name for name in dir(dummy_pt_and_cpm_kernels_objects) if not name.startswith("_")
    ]
else:
    _import_structure["models.chatglm"].extend(["ChatGLM"])


try:
    if not (utils.is_torch_available() and utils.is_einops_available()):
        raise MissingDependencyError
except MissingDependencyError:
    from .utils import dummy_pt_and_einops_objects

    _import_structure["utils.dummy_pt_and_einops_objects"] = [
        name for name in dir(dummy_pt_and_einops_objects) if not name.startswith("_")
    ]
else:
    _import_structure["models.falcon"].extend(["Falcon"])

try:
    if not utils.is_torch_available():
        raise MissingDependencyError
except MissingDependencyError:
    from .utils import dummy_pt_objects

    _import_structure["utils.dummy_pt_objects"] = [name for name in dir(dummy_pt_objects) if not name.startswith("_")]
else:
    _import_structure["models.flan_t5"].extend(["FlanT5"])
    _import_structure["models.dolly_v2"].extend(["DollyV2"])
    _import_structure["models.starcoder"].extend(["StarCoder"])
    _import_structure["models.stablelm"].extend(["StableLM"])
    _import_structure["models.opt"].extend(["OPT"])
    _import_structure["models.auto"].extend(["AutoLLM", "MODEL_MAPPING"])

try:
    if not utils.is_flax_available():
        raise MissingDependencyError
except MissingDependencyError:
    from .utils import dummy_flax_objects

    _import_structure["utils.dummy_flax_objects"] = [
        name for name in dir(dummy_flax_objects) if not name.startswith("_")
    ]
else:
    _import_structure["models.flan_t5"].extend(["FlaxFlanT5"])
    _import_structure["models.opt"].extend(["FlaxOPT"])
    _import_structure["models.auto"].extend(["AutoFlaxLLM", "MODEL_FLAX_MAPPING"])

try:
    if not utils.is_tf_available():
        raise MissingDependencyError
except MissingDependencyError:
    from .utils import dummy_tf_objects

    _import_structure["utils.dummy_tf_objects"] = [name for name in dir(dummy_tf_objects) if not name.startswith("_")]
else:
    _import_structure["models.flan_t5"].extend(["TFFlanT5"])
    _import_structure["models.opt"].extend(["TFOPT"])
    _import_structure["models.auto"].extend(["AutoTFLLM", "MODEL_TF_MAPPING"])


# declaration for OpenLLM-related modules
if t.TYPE_CHECKING:
    from . import cli as cli
    from . import client as client
    from . import exceptions as exceptions
    from . import models as models
    from . import playground as playground
    from . import tests as tests

    # Specific types import
    from ._configuration import LLMConfig as LLMConfig
    from ._llm import LLM as LLM
    from ._llm import LLMRunner as LLMRunner
    from ._llm import Runner as Runner
    from ._package import build as build
    from ._schema import GenerationInput as GenerationInput
    from ._schema import GenerationOutput as GenerationOutput
    from ._schema import MetadataOutput as MetadataOutput
    from .cli import start as start
    from .cli import start_grpc as start_grpc
    from .models.auto import CONFIG_MAPPING as CONFIG_MAPPING
    from .models.auto import MODEL_FLAX_MAPPING_NAMES as MODEL_FLAX_MAPPING_NAMES
    from .models.auto import MODEL_MAPPING_NAMES as MODEL_MAPPING_NAMES
    from .models.auto import MODEL_TF_MAPPING_NAMES as MODEL_TF_MAPPING_NAMES
    from .models.auto import AutoConfig as AutoConfig
    from .models.chatglm import ChatGLMConfig as ChatGLMConfig
    from .models.dolly_v2 import DollyV2Config as DollyV2Config
    from .models.falcon import FalconConfig as FalconConfig
    from .models.flan_t5 import FlanT5Config as FlanT5Config
    from .models.opt import OPTConfig as OPTConfig
    from .models.stablelm import StableLMConfig as StableLMConfig
    from .models.starcoder import StarCoderConfig as StarCoderConfig

    # NOTE: torch and cpm_kernels
    try:
        if not (utils.is_torch_available() and utils.is_cpm_kernels_available()):
            raise MissingDependencyError
    except MissingDependencyError:
        from .utils.dummy_pt_and_cpm_kernels_objects import *
    else:
        from .models.chatglm import ChatGLM as ChatGLM

    # NOTE: torch and einops
    try:
        if not (utils.is_torch_available() and utils.is_einops_available()):
            raise MissingDependencyError
    except MissingDependencyError:
        from .utils.dummy_pt_and_einops_objects import *
    else:
        from .models.falcon import Falcon as Falcon

    try:
        if not utils.is_torch_available():
            raise MissingDependencyError
    except MissingDependencyError:
        from .utils.dummy_pt_objects import *
    else:
        from .models.auto import MODEL_MAPPING as MODEL_MAPPING
        from .models.auto import AutoLLM as AutoLLM
        from .models.dolly_v2 import DollyV2 as DollyV2
        from .models.flan_t5 import FlanT5 as FlanT5
        from .models.opt import OPT as OPT
        from .models.stablelm import StableLM as StableLM
        from .models.starcoder import StarCoder as StarCoder

    try:
        if not utils.is_flax_available():
            raise MissingDependencyError
    except MissingDependencyError:
        from .utils.dummy_flax_objects import *
    else:
        from .models.auto import MODEL_FLAX_MAPPING as MODEL_FLAX_MAPPING
        from .models.auto import AutoFlaxLLM as AutoFlaxLLM
        from .models.flan_t5 import FlaxFlanT5 as FlaxFlanT5
        from .models.opt import FlaxOPT as FlaxOPT

    try:
        if not utils.is_tf_available():
            raise MissingDependencyError
    except MissingDependencyError:
        from .utils.dummy_tf_objects import *
    else:
        from .models.auto import MODEL_TF_MAPPING as MODEL_TF_MAPPING
        from .models.auto import AutoTFLLM as AutoTFLLM
        from .models.flan_t5 import TFFlanT5 as TFFlanT5
        from .models.opt import TFOPT as TFOPT

else:
    import sys

    sys.modules[__name__] = utils.LazyModule(
        __name__,
        globals()["__file__"],
        _import_structure,
        module_spec=__spec__,
        extra_objects={
            "__version__": __version__,
            # The below is a special mapping that allows openllm to be used as a dictionary.
            # This is purely for convenience sake, and should not be used in performance critcal
            # code. This is also not considered as a public API.
            "__openllm_special__": {"flax": "AutoFlaxLLM", "tf": "AutoTFLLM", "pt": "AutoLLM"},
        },
    )
