import ctypes
import os
from ctypes import c_char_p, c_int, c_void_p, POINTER

lib_path = os.path.join(os.path.dirname(__file__), "llrp_client.dll")
llrp_lib = ctypes.CDLL(lib_path)

# Define argument and return types for exposed functions
llrp_lib.get_last_error.restype = c_char_p

llrp_lib.initialize_client.argtypes = [c_char_p]
llrp_lib.initialize_client.restype = POINTER(c_void_p)

def initialize_client(config_path: str):
  client = llrp_lib.initialize_client(config_path.encode("utf-8"))
  if not client:
    error = llrp_lib.get_last_error()
    raise Exception(f"Error initializing client: {error.decode('utf-8')}")
  return client

llrp_lib.send_keep_alive.argtypes = [POINTER(c_void_p)]
llrp_lib.send_keep_alive.restype = c_int

def send_keep_alive(client):
  result = llrp_lib.send_keep_alive(client)
  if result != 0:
    error = llrp_lib.get_last_error()
    raise Exception(f"Error sending keep-alive: {error.decode('utf-8')}")

llrp_lib.send_enable_events_and_reports.argtypes = [POINTER(c_void_p)]
llrp_lib.send_enable_events_and_reports.restype = c_int

def send_enable_events_and_reports(client):
  result = llrp_lib.send_enable_events_and_reports(client)
  if result != 0:
    error = llrp_lib.get_last_error()
    raise Exception(f"Error enabling events and reports: {error.decode('utf-8')}")

llrp_lib.send_get_reader_capabilities.argtypes = [POINTER(c_void_p)]
llrp_lib.send_get_reader_capabilities.restype = c_int

def send_get_reader_capabilities(client):
  result = llrp_lib.send_get_reader_capabilities(client)
  if result != 0:
    error = llrp_lib.get_last_error()
    raise Exception(f"Error getting reader capabilities: {error.decode('utf-8')}")

llrp_lib.send_get_reader_config.argtypes = [POINTER(c_void_p)]
llrp_lib.send_get_reader_config.restype = c_int

llrp_lib.send_set_reader_config.argtypes = [POINTER(c_void_p)]
llrp_lib.send_set_reader_config.restype = c_int

llrp_lib.send_add_rospec.argtypes = [POINTER(c_void_p)]
llrp_lib.send_add_rospec.restype = c_int

llrp_lib.send_enable_rospec.argtypes = [POINTER(c_void_p)]
llrp_lib.send_enable_rospec.restype = c_int

llrp_lib.send_start_rospec.argtypes = [POINTER(c_void_p)]
llrp_lib.send_start_rospec.restype = c_int

llrp_lib.send_stop_rospec.argtypes = [POINTER(c_void_p)]
llrp_lib.send_stop_rospec.restype = c_int

llrp_lib.send_delete_rospec.argtypes = [POINTER(c_void_p), c_int]
llrp_lib.send_delete_rospec.restype = c_int

ROAccessReportCallback = ctypes.CFUNCTYPE(None, c_char_p)
llrp_lib.set_ro_access_report_callback.argtypes = [ROAccessReportCallback]
llrp_lib.set_ro_access_report_callback.restype = None

llrp_lib.await_ro_access_report.argtypes = [POINTER(c_void_p)]
llrp_lib.await_ro_access_report.restype = c_int

llrp_lib.disconnect_client.argtypes = [POINTER(c_void_p)]
llrp_lib.disconnect_client.restype = None

def disconnect_client(client):
  llrp_lib.disconnect_client(client)

llrp_lib.free_client.argtypes = [POINTER(c_void_p)]
llrp_lib.free_client.restype = None

def free_client(client):
  llrp_lib.free_client(client)