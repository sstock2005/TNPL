from proxy import Proxy

proxy = Proxy('127.0.0.1', 2222, '127.0.0.1', 7777)

proxy.run_proxy()