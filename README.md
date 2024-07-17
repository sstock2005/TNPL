## Terraria Network Protocol Library (TNPL)
A little project I've been working on without any thirdparty libraries. It attempts to allow developers to look into how the game Terraria interacts between it's client and server. With the library (packet.py) and the proxy server (proxy.py), a user can see the packets being sent in realtime and easily see their meaning and what information is inside of them. This project takes a lot of inspiration from [mrkite's terrafirma terraria network protocol](https://seancode.com/terrafirma/net.html).

## What does it do?
This project allows a user to start the proxy server and look at the data being transfered between the client and server and even save the sent packets to look at manually with packet.py.

Example:  
With the library we can take the raw bytes being sent to the server:
```
b'.\x00\x04\x00\x08x\x0bMalo Magnus\x00\x00\x00\x00\xee\xe3\xf1\xcc\x99\x8d\x00\x83\x7f\xff\xd7\x00\xff\xd7\x00\xff\xd7\x00\x96K\x00\x04\x10\x05(\x00D$1ec8fe94-c86a-4dd9-bb3a-9c6a253b0365'
```

and convert them into a python object you can easily view and reference.

```py
{'description': '$04 — Player Appearance (client ↔ server)', 'player_slot': 0, 'clothing_style': 8, 'hair_style': 120, 'player_name_len': 11, 'player_name': 'Malo Magnus', 'hair_color': '#EEE3F1', 'skin_color': '#CC998D', 'eye_color': '#0837F', 'undershirt_color': '#FFD70', 'shirt_color': '#FFD70', 'pants_color': '#FFD70', 'boots_color': '#964B0', 'player_difficulty': 'Unknown! Int: 4', 'last_byte': b'\x10'}
```

## Showcase
[Checkout the video showcase!](https://youtu.be/Sx5QAoem7Y0)
  
  
## How to use

### Installation
```
git clone https://github.com/sstock2005/TNPL.git
cd ./TNPL
```

OR 

Simply download the code from github!

Then create a new python script in the directory and paste one of these in!

### Usage
```py
from packet import Packet

info = Packet(b'.\x00\x04\x00\x08x\x0bMalo Magnus\x00\x00\x00\x00\xee\xe3\xf1\xcc\x99\x8d\x00\x83\x7f\xff\xd7\x00\xff\xd7\x00\xff\xd7\x00\x96K\x00\x04\x10\x05(\x00D$1ec8fe94-c86a-4dd9-bb3a-9c6a253b0365')

print(info.payload.player_name)
```

or to use the proxy
```py
from proxy import Proxy

proxy = Proxy('127.0.0.1', 2222, '127.0.0.1', 7777)

proxy.run_proxy()
```

### Proxy Setup
To use the proxy, there are a few settings you need to configure, it only takes a second.
```py
my_proxy = Proxy(
    listen_ip='127.0.0.1', # The ip you want to listen on
    listen_port=2222,      # The port you want to listen on
                               # You connect to this one in the game
    server_ip='127.0.0.1', # The ip of the real server
    server_port=7777,      # The port of the real server (7777)
    printout=True,         # Do you want to print known variables?
    print_packet=False,    # Do you want to print the raw packets to 
                               # use later?
    print_unknown=False,   # Do you want to print unknown packets?
)
```

## Plans for the future
I want to eventually reverse engineer all of the packets that Terraria uses to communicate and possibly create a terraria headless program as a proof of concept. This has been a fun past time of mine but I am getting busier so I am uploading it now to try and work on it!

## Todo
- Continue reverse engineering Packet ID 07 (I have a long way to go!)
- Check the player difficulty logic in Packet ID 04
- Allow bulk Packet ID 05
- Create setup.py and make it a legit python library!

## Credit
Again, a huge thanks to [mrkite's terrafirma tnp page](https://seancode.com/terrafirma/net.html). All other references can be found in [REFERENCES.md](https://github.com/sstock2005/tnp/blob/main/REFERENCES.md).
