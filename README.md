# Linactux  
Change OS *without* needing a USB.

> ⚠️ **Note:**  
> For best results, a USB installation is still recommended.

## 🔧 Instructions – Windows

1. **Download Puppy Linux ISO**  
   Choose and download, F96-CE is preferred for best hardware support, so you don't get stuck without internet.  
   https://f96.puppylinux.com/

2. **Install Python (if not already installed)**  
   Get it from the official site: [python.org/downloads/windows](https://www.python.org/downloads/windows)

3. **Download Linactux**  
   - Extract the ZIP.  
   - Open the extracted folder.  
   - Run `windows.py` and press Yes on the UAC prompt if it appears.

4. **Choose a Temporary Partition (Optional)**  
   You’ll have the option to create a temporary partition to store files needed during the Linux install.

5. **Enter the ISO Path**  
   Example: `C:\Users\yourname\Downloads\F96-CE_4.iso`

6. **Transfer Files (if using a partition)**  
   The script will wait for you to finish copying files into the partition, ensuring you’re ready before proceeding.

7. **Finalize Installation**  
   Once confirmed, Linactux will ask whether or not you want to skip entering the BIOS.  
   This method will **remove the Windows bootloader** and reboot your system directly into the Linux installer.

Now read the instructions for Puppy Linux.

---

## How to Paste Text into the Linux Terminal

If you're new to Linux, you might try pressing **Ctrl + V** to paste text into the terminal — but that usually won’t work because:

- **Ctrl + V** in the terminal is a special control key that tells the shell to treat the next character literally, not to paste text.

### To paste text into a terminal window, use:

- **Shift + Ctrl + V**  
- Or right-click inside the terminal and select **Paste**  
- Or click the middle mouse button (wheel) to paste the clipboard’s current selection

---

## 🔧 Instructions – Puppy Linux to install your Linux distribution

1. **Click Term in the desktop (single click)**  
   This will prepare you for commands for next steps.

2. **Find your internal disk**  
   Type `lsblk` and press Enter.  
   If you're using NVME, it should be `nvme0n1`.  
   If you're using SSD/HDD, it should be `sda`.

3. **Find the URL to the ISO, usually ends with `.iso`**  
   You can usually obtain the URL by right-clicking on the download and choosing **Copy Link Address**.

4. **Begin writing to internal disk**  
   Type `curl -L url-to-iso | dd of=/dev/(your internal disk, e.g. sda) bs=4M status=progress` and enter.
   e.g. `curl -L https://server/iso.iso | dd of=/dev/sda bs=4M status=progress`.'
   
   Make sure there is no network interruption during the write, otherwise, download fails, retry the command.
   
   Type `sync` and enter.
   Now reboot, or by using the terminal, type `reboot` and enter.

You do not need to save the session in Puppy Linux, just press No.
   
