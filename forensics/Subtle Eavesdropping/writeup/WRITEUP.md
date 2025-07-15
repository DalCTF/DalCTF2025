## Subtle Eavesdropping

### Solution

Information is hidden in POST packets. Solve by opening the pcap in wireshark and right clicking a POST packet \> follow HTTP stream

The end of each POST packet has data: "key=\<character\>"

Concatenating all characters reveals the flag: `dalctf{s0Me0n3_1s_L1sTeNInG??}`

