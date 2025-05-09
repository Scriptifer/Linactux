# Linactux 
Switch from Windows to Linux *without* needing a USB.

> ⚠️ **Note:**  
While Linactux has been successfully tested on bare metal with Linux Mint, compatibility with all Linux distributions is *not* guaranteed. For best results, a USB installation is still recommended.

---

Ubuntu based distributions should work. ✅

Linux Mint was tested and worked.

Most distributions will experience mounting issues, we currently don't know the solution.
However to properly create the installation, after you have used this tool to boot into Linux (as root):
`wget -O - your-url-to-iso-file | dd of=yoursystemdisk bs=4M`
`sync`
`reboot`
After the reboot, you can safely begin the installation without any errors.

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
