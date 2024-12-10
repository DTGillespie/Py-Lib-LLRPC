import ctypes
import os
import sys
from ctypes import c_char_p, c_int, c_void_p

if sys.platform.startswith('win'):
  lib_filename = "llrp_lib.dll"
elif sys.platform.startswith('linux'):
  lib_filename = "llrp_lib.so"
elif sys.platform.startswith('darwin'):
  lib_filename = "llrp_lib.dylib"
else:
  raise OSError("Unsupported operating system")

lib_path = os.path.join(os.path.dirname(__file__), lib_filename)
llrp_lib = ctypes.CDLL(lib_path)

llrp_lib.initialize_client.argtypes = [c_char_p]
llrp_lib.initialize_client.restype = c_void_p

llrp_lib.client_set_reader_capabilities_callback.argtypes = [c_void_p, ctypes.CFUNCTYPE(None, c_char_p)]
llrp_lib.client_set_reader_capabilities_callback.restype = c_int

llrp_lib.client_set_reader_config_callback.argtypes = [c_void_p, ctypes.CFUNCTYPE(None, c_char_p)]
llrp_lib.client_set_reader_config_callback.restype = c_int

llrp_lib.client_set_ro_access_report_callback.argtypes = [c_void_p, ctypes.CFUNCTYPE(None, c_char_p)]
llrp_lib.client_set_ro_access_report_callback.restype = c_int

llrp_lib.send_keep_alive.argtypes = [c_void_p]
llrp_lib.send_keep_alive.restype = c_int

llrp_lib.send_enable_events_and_reports.argtypes = [c_void_p]
llrp_lib.send_enable_events_and_reports.restype = c_int

llrp_lib.send_get_reader_capabilities.argtypes = [c_void_p]
llrp_lib.send_get_reader_capabilities.restype = c_int

llrp_lib.send_get_reader_config.argtypes = [c_void_p]
llrp_lib.send_get_reader_config.restype = c_int

llrp_lib.send_set_reader_config.argtypes = [c_void_p]
llrp_lib.send_set_reader_config.restype = c_int

llrp_lib.send_add_rospec.argtypes = [c_void_p]
llrp_lib.send_add_rospec.restype = c_int

llrp_lib.send_enable_rospec.argtypes = [c_void_p]
llrp_lib.send_enable_rospec.restype = c_int

llrp_lib.send_start_rospec.argtypes = [c_void_p]
llrp_lib.send_start_rospec.restype = c_int

llrp_lib.send_stop_rospec.argtypes = [c_void_p]
llrp_lib.send_stop_rospec.restype = c_int

llrp_lib.send_delete_rospec.argtypes = [c_void_p, c_int]
llrp_lib.send_delete_rospec.restype = c_int

llrp_lib.read_ro_access_report.argtypes = [c_void_p]
llrp_lib.read_ro_access_report.restype = c_int

llrp_lib.send_close_connection.argtypes = [c_void_p]
llrp_lib.send_close_connection.restype = c_int

llrp_lib.free_client.argtypes = [c_void_p]
llrp_lib.free_client.restype = c_int

llrp_lib.free_string.argtypes = [c_char_p]
llrp_lib.free_string.restype = c_int

llrp_lib.get_last_error.argtypes = []
llrp_lib.get_last_error.restype = c_char_p

def get_last_error():
  error_ptr = llrp_lib.get_last_error()
  if error_ptr:
    error = error_ptr.decode('utf-8')
    free_string(error_ptr)
    return error
  return None

def free_string(string_ptr):
  result = llrp_lib.free_string(string_ptr)
  if result != 0:
    error = get_last_error()
    raise Exception(f"Error deallocating string pointer: {error}")

ReaderCapabilitiesCallback = ctypes.CFUNCTYPE(None, c_char_p)
ReaderConfigCallback       = ctypes.CFUNCTYPE(None, c_char_p)
ROAccessReportCallback     = ctypes.CFUNCTYPE(None, c_char_p)

class LLRPClient:
    
  def __init__(self, config_path: str):
    self._handle = llrp_lib.initialize_client(config_path.encode("utf-8"))
    if not self._handle:
      error = get_last_error()
      raise Exception(f"Error initializing client: {error}")

  def set_reader_capabilities_callback(self, callback):
    cb = ReaderCapabilitiesCallback(callback)
    result = llrp_lib.client_set_reader_capabilities_callback(self._handle, cb)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error setting reader capabilities callback: {error}")

  def set_reader_config_callback(self, callback):
    cb = ReaderConfigCallback(callback)
    result = llrp_lib.client_set_reader_config_callback(self._handle, cb)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error setting reader config callback: {error}")

  def set_ro_access_report_callback(self, callback):
    cb = ROAccessReportCallback(callback)
    result = llrp_lib.client_set_ro_access_report_callback(self._handle, cb)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error setting RO access report callback: {error}")

  def send_keep_alive(self):
    result = llrp_lib.send_keep_alive(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending KEEP_ALIVE: {error}")

  def send_enable_events_and_reports(self):
    result = llrp_lib.send_enable_events_and_reports(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending ENABLE_EVENTS_AND_REPORTS: {error}")

  def send_get_reader_capabilities(self):
    result = llrp_lib.send_get_reader_capabilities(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending GET_READER_CAPABILITIES: {error}")

  def send_get_reader_config(self):
    result = llrp_lib.send_get_reader_config(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending GET_READER_CONFIG: {error}")

  def send_set_reader_config(self):
    result = llrp_lib.send_set_reader_config(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending SET_READER_CONFIG: {error}")

  def send_add_rospec(self):
    result = llrp_lib.send_add_rospec(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending ADD_RO_SPEC: {error}")

  def send_enable_rospec(self):
    result = llrp_lib.send_enable_rospec(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending ENABLE_RO_SPEC: {error}")

  def send_start_rospec(self):
    result = llrp_lib.send_start_rospec(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending START_RO_SPEC: {error}")

  def send_stop_rospec(self):
    result = llrp_lib.send_stop_rospec(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending STOP_RO_SPEC: {error}")

  def send_delete_rospec(self, rospec_id: int):
    result = llrp_lib.send_delete_rospec(self._handle, rospec_id)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending DELETE_RO_SPEC: {error}")

  def read_ro_access_report(self):
    result = llrp_lib.read_ro_access_report(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error reading ROAccessReport: {error}")

  def send_close_connection(self):
    result = llrp_lib.send_close_connection(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error sending CLOSE_CONNECTION: {error}")

  def free(self):
    result = llrp_lib.free_client(self._handle)
    if result != 0:
      error = get_last_error()
      raise Exception(f"Error deallocating client pointer: {error}")
    self._handle = None