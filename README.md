# Basic-Port-Forwarder

This is a port forwarding server that will forward incoming connection requests to specific ports/services from any IP address, to any user-specified IP address and port. The application provides both IPv4 and IPv6 functionality. TLS secured connections will be added in the future.

As an example, if you were to add this line to the conf file "65434!192.168.0.5!8443", the port forwarder would forward any connections to port 65434 to the IP & port of 
192.168.0.5:8443.
