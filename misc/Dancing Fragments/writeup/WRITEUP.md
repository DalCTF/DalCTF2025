## Dancing Fragments

### Solution

This challenge contains a .gif file. The gif displays a guy dancing, with some multicoloured pixels moving around him. Every few frames, there are some ascii characters visible.

Steps:

- Open the gif in an image editor such as gimp, and open the frames as layers
- Look at each frame individually, and extract the ascii characters
- Arranging them in order starting from the first frame gives the following string:
    `ZGFsY3Rme2cwdHQ0X0cwVFQ0X2NVdF9MME9zRX0`
- Converting this from base64 gives the flag:
    `dalctf{g0tt4_G0TT4_cUt_L0OsE}`