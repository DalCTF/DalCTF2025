## What Encryption

### Solution

This challenge contains a pcap. There is a lot of junk traffic, but the flag is hidden amongst all the filler packet. It can be found with the following method:

- Open the pcap in wireshark
- File \> Export Objects \> HTTP
- There are two interesting files mixed in with the junk, `key.pem` and `flag`
- Save them
- Key.pem contains an RSA private key
- RSA decrypt flag with online tools (such as cyberchef) or openssl with the following command:
  `openssl rsautl -oaep -decrypt -in flag.test -out test.txt -inkey key.pem`
- reveals the flag: `dalctf{pr1vat3_k3y_n0t_VeRy_prIva4te}`