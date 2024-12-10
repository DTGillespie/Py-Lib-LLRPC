import os
from llrp_lib import LLRPClient

def main():
    
  cwd = os.path.dirname(os.path.abspath(__file__))
  config_path = os.path.join(cwd, "llrp_config.json")

  client = LLRPClient(config_path)

  def on_GetReaderCapabilitiesResponse(capabilities_ptr):
    capabilities = capabilities_ptr.decode('utf-8')
    print("\nReceived GetReaderCapabilitiesResponse:", capabilities)

  def on_GetReaderConfigResponse(config_ptr):
    config = config_ptr.decode('utf-8')
    print("\nReceived GetReaderConfigResponse:", config)

  def on_ROAccessReport(report_ptr):
    report = report_ptr.decode('utf-8')
    print("\nReceived ROAccessReport:", report)
    
  client.set_reader_capabilities_callback(on_GetReaderCapabilitiesResponse)
  client.set_reader_config_callback(on_GetReaderConfigResponse)
  client.set_ro_access_report_callback(on_ROAccessReport)

  client.send_get_reader_capabilities()
  client.send_delete_rospec(0)
  client.send_set_reader_config()
  client.send_get_reader_config()
  client.send_enable_events_and_reports()
  client.send_add_rospec()
  client.send_enable_rospec()
  client.send_start_rospec()
  client.read_ro_access_report()
  client.send_stop_rospec()
  client.send_close_connection()
  client.free()

if __name__ == "__main__":
  main()