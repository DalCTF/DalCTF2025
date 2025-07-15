## We Have to Go Deeper
### Solution

This Steganography/Forensics challenge can be solved using the following steps:

- unzip the provided zip file and open the pcap in wireshark
- Filter SMTP traffic, there is an email that mentions a password for an image file. It mentions the password `pinaple_princess_892`
- File \> export objects \> HTML \> download kitten.jpg
- Use steghide and the password to extract data from the file:
  `steghide --extract -sf kitten.jpg`
- Result: Baby_Chicken.png
- use binwalk to extract data from the file:
  `binwalk -e Baby_Chicken.png`
- Result: a tar archive
- Unzip the archive to reveal content_beach.jpg
- Bruteforce the password to the file with a tool like stegbrute, the password is in rockyou.txt
- Password is 1234567
- Open the resulting png file in gimp, or use an online tool like stegonline
- In gimp, go to Colours \> Curves and mess with the values until the flag appears
- In StegOnline, click LSB Half
- Reveal the flag: `dalctf{i5_1T_0v3R_Y3t?}`