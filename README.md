# Mustang Presets Loader
I purchased a Fender Mustang LT25 and noticed that it came with 60 slots for preset tones. 30 of these were already populated with customized settings from the manufacturer. 

There is a newer and more expensive version of this amp with Bluetooth capabilities that can interface with the Fender Tone mobile app. Here, you can download community-made presets and upload them to your amp. However, this is not the case with my LT25.

With that, there *is* a microUSB port on the main I/O of the amp. Here, you may connect it to your computer and use the Fender Tone LT Desktop app to create presets on the interface and then upload them to your amp via the USB connection. Unfortunately, unlike the Fender tone app, you can't just directly download the community-made presets and upload them through the app. As a result, users have to manually transfer the tone settings from the community hub to the desktop app and then upload the preset.

With this project, I'm aiming to create an application that scrapes the community hub for the presets, grabs the tone setting info, and then uploads the preset in the same way that the desktop app does through its interface.

Current technologies/tools: USBPcap, Wireshark, Python, and anything else that pops up down the line.

This will require learning about USB sniffing and commands sent over USB connections which I have *zero* experience with.

- Current Progress (3/19/2024):
    Determined the endpoints on which the amp communicates
    Grabbed a .pcap of the commands sent when starting the desktop app and plugging the amp in
    Sent a test preset upload through the desktop app; grabbed the set of commands from the .pcap that indicate this transaction
    Attempted to edit some of the bytes and re-send the payload to the amp using the Python usb library
