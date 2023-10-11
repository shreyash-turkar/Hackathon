# import pcapy

# # Define the capture device, snap length, promiscuous mode, and timeout
# device = 'eth0'
# snaplen = 65535
# promisc = False
# timeout = 100

# # Open the capture device and create a connection object
# capture = pcapy.open_live(device, snaplen, promisc, timeout)
# conn = capture.getfd()

# # Set the filter (optional)
# capture.setfilter('tcp port 80')

# # Save packets to file (optional)
# filename = 'captured.pcap'
# dump = capture.dump_open(filename)

# # Loop through captured packets
# while True:
    # # Read the next packet
    # header, packet = capture.next()
    # # Write the packet to the output file
    # dump.dump(header, packet)
    # # Process the packet further or break the loop
    # if some_condition:
        # break

# # Close the output file and the capture connection
# dump.close()
# capture.close()

from scapy.all import sniff, wrpcap
import sys

filt, iface = "",""
if len(sys.argv)> 1:
    filt = sys.argv[1]
elif len(sys.argv) > 2:
    iface = sys.argv[2]
    
if filt == "":
    if iface == "":
        capture = sniff(prn= lambda x:x.summary(), count=100)
    else:
        capture = sniff(prn= lambda x:x.summary(), count=100, iface=iface)
else:
    if iface == "":
        capture = sniff(prn= lambda x:x.summary(), count=100, filter = filt)
    else:
        capture = sniff(prn= lambda x:x.summary(), count=100, iface=iface, filter = filt)

wrpcap('test.pcap', capture)
