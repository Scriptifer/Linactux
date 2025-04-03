# Linactux (beta)
**It is still recommended to use a USB to switch from Windows to Linux, this tool should be used if too many options have been exhausted.**

Switch from Windows to Linux without a USB.

# Instructions - Windows
1. Download an ISO for your preferred Linux distribution.
2. Download Python for Windows if you haven't already.
3. Download the repository, extract it and go inside and run `main.py` as admin.
4. You can decide whether or not to create a partition to temporarily store files to go along with the Linux installation.
5. Then you can enter the path to the ISO, e.g. `C:/Users/user/Downloads/myiso.iso`.
6. After that, the script will begin and wait for you to transfer files onto the partition if you specifically did so, it will really make sure you're done.
7. Finally, it will destroy the Windows bootloader and reboot in order to prevent booting into Windows and straight into Linux.
