import threading
import time
import os

import llrp_lib

def main():

  client = None
  try:

    cwd = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cwd, "llrp_config.json")

    client = llrp_lib.initialize_client(config_path)
    
    get_reader_capabilities(client)
    get_reader_config(client)
    
    initialize_ro_spec(client)

    llrp_lib.await_ro_access_report(client)
    llrp_lib.send_stop_rospec(client)

  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    if client:
      try:
        llrp_lib.disconnect_client(client)
        llrp_lib.free_client(client)
        print("Client disconnected and deallocated")
      except Exception as cleanup_error:
        print(f"An error occured during cleanup: {cleanup_error}")

def get_reader_capabilities(client):

  def reader_capabilities_callback(capabilities_ptr):
    capabilities = capabilities_ptr('utf-8')
    print(f"Received ReaderCapabilities: {capabilities}")
  
  callback_func = llrp_lib.ReaderCapabilitiesCallback(reader_capabilities_callback)
  llrp_lib.set_reader_capabilities_callback(callback_func)
  print("ReaderCapabilities callback set successfully")

  llrp_lib.send_get_reader_capabilities(client)

def get_reader_config(client):

  def reader_config_callback(config_ptr):
    config = config_ptr('utf-8')
    print(f"Received ReaderConfig: {config}")

  callback_func = llrp_lib.ReaderConfigCallback(reader_config_callback)
  llrp_lib.set_reader_config_callback(callback_func)
  print("ReadeerConfig callback set successfully")

  llrp_lib.send_get_reader_config(client)

def initialize_ro_spec(client):

  def ro_access_report_callback(report_ptr):
    report = report_ptr('utf-8')
    print(f"Received ROAccessReport: {report}")

  callback_func = llrp_lib.ROAccessReportCallback(ro_access_report_callback)
  llrp_lib.set_ro_access_report_callback(callback_func)
  print("ROAccessReport callback set successfully")

  llrp_lib.send_delete_rospec(client, 0)
  llrp_lib.send_set_reader_config(client)
  llrp_lib.send_enable_events_and_reports(client)
  llrp_lib.send_add_rospec(client)
  llrp_lib.send_enable_rospec(client)
  llrp_lib.send_start_rospec(client)

if __name__ == "__main__":
  main()