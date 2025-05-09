# Linactux 
Switch from Windows to Linux *without* needing a USB.

> ⚠️ **Note:**  
While Linactux has been successfully tested on bare metal with Linux Mint, compatibility with all Linux distributions is *not* guaranteed. For best results, a USB installation is still recommended.

---

Non Ubuntu based distributions will experience mounting errors.

To fix this, (assuming you already installed Linux using this tool, works best in Alpine Linux diskless) make sure you are connected to the internet inside the Linux installation, test by e.g. `ping 1.1.1.1`.

Run this command as root and don't forget to set the URL and system disk: `wget -O - your-url-to-iso-file | dd of=your-system-disk bs=4M oflag=sync && reboot`.

After the reboot, you can safely begin the installation.


## 🔧 Instructions – Windows

1. **Download a Linux ISO**  
   Choose and download the ISO file of your preferred Linux distribution.

2. **Install Python (if not already installed)**  
   Get it from the official site: [python.org/downloads/windows](https://www.python.org/downloads/windows)

3. **Download Linactux**  
   - Extract the ZIP.  
   - Open the extracted folder.  
   - Run `main.py` and press Yes on the UAC prompt.

4. **Choose a Temporary Partition (Optional)**  
   You’ll have the option to create a temporary partition to store files needed during the Linux install.

5. **Enter the ISO Path**  
   Example: `C:/Users/yourname/Downloads/linuxmint.iso`

6. **Transfer Files (if using a partition)**  
   The script will wait for you to finish copying files into the partition, ensuring you’re ready before proceeding.

7. **Finalize Installation**  
   Once confirmed, Linactux will **remove the Windows bootloader** and reboot your system directly into the Linux installer.

---
