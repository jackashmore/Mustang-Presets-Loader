import usb.core
import usb.util

def convert_hid_data_to_byte_array(hid_data):
    # Remove any non-hexadecimal characters (like spaces or colons)
    clean_data = ''.join(filter(str.isalnum, hid_data))

    # Convert the cleaned data to a byte array
    byte_array = bytes.fromhex(clean_data)

    return byte_array

# testing HID data sent
hid_data = "35070800ca0c0208011054455354484552454c4f4c202020202020101f70120e445542535f4f76657264726976654f202020101f010101010101010573746f6d"

# Convert and print the byte array
byte_array = convert_hid_data_to_byte_array(hid_data)
array_len = len(byte_array)
print(array_len)

# From Device Manager hardware ID: USB\VID_1ED8&PID_0037
# This is going to be different based on the machine and port being used...
# I used USBPcap and identified the type of USB device and port ('USB Composite Device' and Port 2, respectively)
# Maybe could do something similar to getting an environment variable if I wanted to make it compatible
# with other systems? TODO...
VENDORID = 0x1eD8
PRODUCTID = 0x0037

# using the vendor and product IDs, locate the device
dev = usb.core.find(idVendor=VENDORID, idProduct=PRODUCTID)
if dev is None:
    raise ValueError("Couldn't find USB device")

# this just sets the active configuration; since we pass no args here, the first
# config will be the active one. According to the doc, set_configuration just applies
# the first config it finds for the device. Some devices have multiple, others only have
# one; fingers crossed for now that this just has the one
dev.set_configuration()

# from the example code on the doc, this pulls an instance of an endpoint:
    # cfg = dev.get_active_configuration()
    # intf = cfg[(0,0)]
# Since I already know from Wireshark that the device is denoted 2.1.1 (bus 2, device # 1, going through endpoint 1),
# I can directly write to the endpoint:
# dev.write(1, 'test')
# ^ this writes the string 'test' to endpoint 1...

# The packets that are transmitted to the amp are formatted like a JSON object
# For example, the following was pulled from a packet where I was setting a test
# preset on slot 31 with name 'Random HERE':
    # 0000   1b 00 f0 24 83 87 07 bf ff ff 00 00 00 00 09 00   ...$............
    # 0010   00 02 00 01 00 01 01 40 00 00 00 34 3d 4e 61 6d   .......@...4=Nam
    # 0020   65 22 3a 22 52 61 6e 64 6f 6d 20 20 48 45 52 45   e":"Random  HERE
    # 0030   20 20 20 20 22 2c 22 69 73 5f 66 61 63 74 6f 72       ","is_factor
    # 0040   79 5f 64 65 66 61 75 6c 74 22 3a 74 72 75 65 2c   y_default":true,
    # 0050   22 70 72 65 73 65 74 5f 69 64 00                  "preset_id.

# As such, I'll structure packets like so and hopefully there's some uniformity to how they're
# structured. Then, write it to the endpoint; NEVERMIND

# It's sending HID reports back and forth so gonna try that approach by just sending byte arrays
# similar to those in the pcap

# grab endpoint
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)] 

# match 1st OUT endpoint
ep = usb.util.find_descriptor(
    intf,
    match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

if ep is None:
    raise ValueError('Couldnt find endpoint')

ep.write(byte_array)