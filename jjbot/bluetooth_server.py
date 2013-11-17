import bluetooth
from uuid import getnode as get_mac


def get_mac_address():
    mac = get_mac()
    return "%012X"%mac



server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_socket.bind(("",bluetooth.PORT_ANY))
server_socket.listen(1)
port = server_socket.getsockname()[1]
print "listening on port %d" %port

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

mac = get_mac_address()

bluetooth.advertise_service( server_socket, "Lilybot %s" %mac,
                   service_id = uuid,
                   service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                   profiles = [ bluetooth.SERIAL_PORT_PROFILE ], 
                    )

print "Waiting for connection on RFCOMM channel %d" % port

client_sock, client_info = server_socket.accept()
print "Accepted connection from ", client_info

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print "received [%s]" % data
except IOError:
    pass

print "disconnected"

client_sock.close()
server_socket.close()
print "all done"