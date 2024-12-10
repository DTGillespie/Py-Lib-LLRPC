import os
from llrp_lib import LLRPClient

def on_GetReaderCapabilitiesResponse(capabilities_ptr):
  capabilities = capabilities_ptr.decode('utf-8')
  print("Received GetReaderCapabilitiesResponse:", capabilities)

def on_GetReaderConfigResponse(config_ptr):
  config = config_ptr.decode('utf-8')
  print("Received GetReaderConfigResponse:", config)

def on_ROAccessReport(report_ptr):
  report = report_ptr.decode('utf-8')
  print("Received ROAccessReport:", report)

def main():
    
  cwd = os.path.dirname(os.path.abspath(__file__))
  config_path = os.path.join(cwd, "llrp_config.json")

  client = LLRPClient(config_path)

  client.set_reader_capabilities_callback(on_GetReaderCapabilitiesResponse)
  client.set_reader_config_callback(on_GetReaderConfigResponse)
  client.set_ro_access_report_callback(on_ROAccessReport)

  client.send_get_reader_capabilities()

  client.send_get_reader_config()

  client.read_ro_access_report()

  client.send_close_connection()
  client.free()

if __name__ == "__main__":
  main()