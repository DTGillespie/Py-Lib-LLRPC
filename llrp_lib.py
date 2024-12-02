import ctypes
import os
import sys
from ctypes import c_char_p, c_int, c_void_p, POINTER

if sys.platform.startswith('win'):
  lib_filename = "llrp_lib.dll"
elif sys.platform.startswith('linux'):
  lib_filename = "llrp_lib.so"
elif sys.playform.startswith('darwin'):
  lib_filename = "llrp_lib.dylib"
else:
  raise OSError("Unsupported operating system")

lib_path = os.path.join(os.path.dirname(__file__), lib_filename)
llrp_lib = ctypes.CDLL(lib_path)

llrp_lib.initialize_client.argtypes = [c_char_p]
llrp_lib.initialize_client.restype = c_void_p

def initialize_client(config_path: str):
  client = llrp_lib.initialize_client(config_path.encode("utf-8"))
  if not client:
    error = get_last_error()
    raise Exception(f"Error initializing client: {error}")
  return client

llrp_lib.send_keep_alive.argtypes = [c_void_p]
llrp_lib.send_keep_alive.restype = c_int

def send_keep_alive(client):
  result = llrp_lib.send_keep_alive(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending KEEP_ALIVE: {error}")

llrp_lib.send_enable_events_and_reports.argtypes = [c_void_p]
llrp_lib.send_enable_events_and_reports.restype = c_int

def send_enable_events_and_reports(client):
  result = llrp_lib.send_enable_events_and_reports(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending ENABLE_EVENTS_AND_REPORTS: {error}")

_reader_capabilities_callback = None
ReaderCapabilitiesCallback = ctypes.CFUNCTYPE(None, c_char_p)
llrp_lib.set_reader_capabilities_callback.argtypes = [ReaderCapabilitiesCallback]
llrp_lib.set_reader_capabilities_callback.restype = None

def set_reader_capabilities_callback(callback):
  global _reader_capabilities_callback

  _reader_capabilities_callback = callback
  llrp_lib.set_reader_capabilities_callback(callback)

llrp_lib.send_get_reader_capabilities.argtypes = [c_void_p]
llrp_lib.send_get_reader_capabilities.restype = c_int

def send_get_reader_capabilities(client):
  result = llrp_lib.send_get_reader_capabilities(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending GET_READER_CAPABILITIES: {error}")

_reader_config_callback = None
ReaderConfigCallback = ctypes.CFUNCTYPE(None, c_char_p)
llrp_lib.set_reader_config_callback.argtypes = [ReaderConfigCallback]
llrp_lib.set_reader_config_callback.restype = None

def set_reader_config_callback(callback):
  global _reader_config_callback

  _reader_config_callback = callback
  llrp_lib.set_reader_config_callback(callback)

llrp_lib.send_get_reader_config.argtypes = [c_void_p]
llrp_lib.send_get_reader_config.restype = c_int

def send_get_reader_config(client):
  result = llrp_lib.send_get_reader_config(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending GET_READER_CONFIG: {error}")

llrp_lib.send_set_reader_config.argtypes = [c_void_p]
llrp_lib.send_set_reader_config.restype = c_int

def send_set_reader_config(client):
  result = llrp_lib.send_set_reader_config(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending SET_READER_CONFIG: {error}")

llrp_lib.send_add_rospec.argtypes = [c_void_p]
llrp_lib.send_add_rospec.restype = c_int

def send_add_rospec(client):
  result = llrp_lib.send_add_rospec(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending ADD_RO_SPEC: {error}")

llrp_lib.send_enable_rospec.argtypes = [c_void_p]
llrp_lib.send_enable_rospec.restype = c_int

def send_enable_rospec(client):
  result = llrp_lib.send_enable_rospec(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending ENABLE_RO_SPEC: {error}")

llrp_lib.send_start_rospec.argtypes = [c_void_p]
llrp_lib.send_start_rospec.restype = c_int

def send_start_rospec(client):
  result = llrp_lib.send_start_rospec(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending START_RO_SPEC: {error}")

llrp_lib.send_stop_rospec.argtypes = [c_void_p]
llrp_lib.send_stop_rospec.restype = c_int

def send_stop_rospec(client):
  result = llrp_lib.send_stop_rospec(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending STOP_RO_SPEC: {error}")

llrp_lib.send_delete_rospec.argtypes = [c_void_p, c_int]
llrp_lib.send_delete_rospec.restype = c_int

def send_delete_rospec(client, rospec_id):
  result = llrp_lib.send_delete_rospec(client, rospec_id)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending DELETE_RO_SPEC: {error}")

_ro_access_report_callback = None
ROAccessReportCallback = ctypes.CFUNCTYPE(None, c_char_p)
llrp_lib.set_ro_access_report_callback.argtypes = [ROAccessReportCallback]
llrp_lib.set_ro_access_report_callback.restype = None

def set_ro_access_report_callback(callback):
  global _ro_access_report_callback

  _ro_access_report_callback = callback
  llrp_lib.set_ro_access_report_callback(callback)

llrp_lib.await_ro_access_report.argtypes = [c_void_p]
llrp_lib.await_ro_access_report.restype = c_int

def await_ro_access_report(client):
  result = llrp_lib.await_ro_access_report(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error waiting for ROAccessReport: {error}")

llrp_lib.disconnect_client.argtypes = [c_void_p]
llrp_lib.disconnect_client.restype = c_int

def send_close_connection(client):
  result = llrp_lib.send_close_connection(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error sending CLOSE_CONNECTION: {error}")

llrp_lib.free_client.argtypes = [c_void_p]
llrp_lib.free_client.restype = c_int

def free_client(client):
  result = llrp_lib.free_client(client)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error deallocating client pointer: {error}")

llrp_lib.free_string.argtypes = [c_char_p]
llrp_lib.free_string.restype = c_int

def free_string(string):
  result = llrp_lib.free_string(string)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error deallocating string pointer: {error}")

llrp_lib.get_last_error.argtypes = []
llrp_lib.get_last_error.restype = c_char_p

def get_last_error():
  error_ptr = llrp_lib.get_last_error()
  if error_ptr:
    #error = ctypes.cast(error_ptr, ctypes.c_char_p).value.decode('utf-8')
    error = error_ptr.decode('utf-8')
    free_string(error_ptr)
    return error
  return None