# Flash

<hr>

## Description
Flash is a Command-Line Hacking Tool written in Python Version 3. It includes <b>port scanning</b>, <b>directory scanning (gobuster-like)</b>, <b>Reverse Shells</b> and much more.

## Port Scanning
For Port Scanning, run the following command from the terminal:
```python3 src/main.py ps <IP> <PORT RANGE>```
### How to port scan
Flash will start scanning all the ports in the given port range.
A port range is defined with a "-" in the middle.
Let's say you want to scan every port from 0-100 at localhost, this is how you would do it:
```python3 src/main.py ps localhost 0-100```
