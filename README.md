## oui.py

Little program to lookup the vendor string for MAC addresses.
 
The first 3 octetts of a MAC address denote the manufacturer of the network card.
I use this at work, when analyzing unknown or unwanted traffic, to know who the culprit may be. 

Usage:

    python3 oui.py MAC [--force] [--file /var/tmp/oui.txt]
    --force - Forces the download of the file, ignoring the one week caching
    --file - Overrides the storage location and also uses an existing file.
    
This project is in the public domain.

<!--suppress HtmlDeprecatedAttribute -->
<p align="center">
<a href='https://ko-fi.com/L3L31HXRQ' target='_blank'><img height='36' style='border:0;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi2.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
</p>
