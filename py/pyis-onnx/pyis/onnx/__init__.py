__version__ = '0.1.dev2'

import platform
from packaging import version
import os
import platform

# It is no longer required to install onnxruntime. User could provide customized
# onnxruntime binaries instead.

#MINIMAL_ONNXRUNTIME_VERSION = "1.8.0"
#try:
#    import onnxruntime
#except ImportError:
#    raise ImportError("Please install onnxruntime >= " + MINIMAL_ONNXRUNTIME_VERSION )

#if version.parse(onnxruntime.__version__) < version.parse(MINIMAL_ONNXRUNTIME_VERSION):
#    raise ImportError("Please install onnxruntime >= " + MINIMAL_ONNXRUNTIME_VERSION )

# add the lib folder to env
if platform.system() == 'Windows':
    dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    dll_paths = [dll_path, os.environ['PATH']]
    os.environ['PATH'] = ';'.join(dll_paths)
if platform.system() == 'Windows':
    onnx_binding_library_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'lib/pyis_onnx.dll')
elif platform.system() == "Linux":
    onnx_binding_library_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'lib/libpyis_onnx.so')
else:
    raise NotImplementedError(f'platform {platform.system()} is not supported')

def get_onnx_extensions_lib():
    return str(onnx_binding_library_path)
