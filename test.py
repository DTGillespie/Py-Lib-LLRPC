import threading
import time
import os

import lib_llrpc

def main():

  client = None
  try:

    cwd = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cwd, "llrp_config.json")

    client = lib_llrpc.initialize_client(config_path)

    initialize_ro_spec(client)
    lib_llrpc.await_ro_access_report(client)
    lib_llrpc.send_stop_rospec(client)

  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    if client:
      try:
        lib_llrpc.disconnect_client(client)
        lib_llrpc.free_client(client)
        print("Client disconnected and deallocated")
      except Exception as cleanup_error:
        print(f"An error occured during cleanup: {cleanup_error}")
  
def initialize_ro_spec(client):

  def ro_access_report_callback(report_ptr):
    report = report_ptr('utf-8')
    print(f"Received ROAccessReport: {report}")

  callback_func = lib_llrpc.ROAccessReportCallback(ro_access_report_callback)
  lib_llrpc.set_ro_access_report_callback(callback_func)
  print("Callback set successfully")

  lib_llrpc.send_delete_rospec(client, 0)
  lib_llrpc.send_set_reader_config(client)
  lib_llrpc.send_enable_events_and_reports(client)
  lib_llrpc.send_add_rospec(client)
  lib_llrpc.send_enable_rospec(client)
  lib_llrpc.send_start_rospec(client)

if __name__ == "__main__":
  main()