import usb.core
import usb.util

dev = usb.core.find(idVendor=0x1ED8, idProduct=0x0037)
if dev is None:
    raise ValueError('couldnt find device')

for cfg in dev:
    print('Config:', cfg.bConfigurationValue)
    for intf in cfg:
        print(' Interface:', intf.bInterfaceNumber, 'Altetnate Setting:', intf.bAlternateSetting)
        for ep in intf:
            print('Endpoint:', ep.bEndpointAddress)
            print('Type:', usb.util.endpoint_type(ep.bmAttributes))
            print('Direction:', usb.util.endpoint_direction(ep.bEndpointAddress))