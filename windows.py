import subprocess
import os
import string
import math
import psutil
import shutil
import ctypes
import sys
import json
import time
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    script = sys.argv[0]
    params = ' '.join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script+" "+params, None, 1)

if not is_admin():
    run_as_admin()
    sys.exit()

check_process = subprocess.run(
    ["powershell", "-Command", "Confirm-SecureBootUEFI"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

shutdown_cmd = "shutdown /r /f /t 0"
if "True" in check_process.stdout:
    print("You may need to disable Secure Boot to prevent making the new OS unbootable.")
    if input("Do you want to enter the BIOS on restart? Once you have disabled Secure Boot, you can save and continue to boot. ").lower().startswith("y"):
        shutdown_cmd = shutdown_cmd + " /fw"


system_disk = "C:/"
total, used, free = shutil.disk_usage(system_disk)
wants_files = input("Do you want to create a new partition to put your files in so then you can access it on the new OS? ").lower().startswith("y")
files_size = 0
if wants_files:
    while True:
        amount = input("How big should the partition be? (specify in gigabytes)\n\n")
        try:
            if amount == "cancel":
                wants_files = False
                break

            files_size = int(amount) * 1024
            break
        except:
            print("Please enter a valid numerical input, type cancel to cancel.")
            time.sleep(1)



iso_path = input("Enter path to ISO: ")
if not iso_path.endswith(".iso") or not os.path.exists(iso_path):
    print("Invalid ISO path!")
    sys.exit(1)

prev_letters = []
def usedletters():
    used_letters = set()
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        if partition.device[0].isalpha():
            used_letters.add(partition.device[0].upper())
    
    return used_letters

def get_letter():
    used_letters = usedletters()
    for letter in string.ascii_uppercase:
        if letter not in used_letters:
            return letter
    
    return None

iso_mb = round(os.path.getsize(iso_path) / (1024 * 1024)) + 2
total_size = iso_mb + files_size
if (free / 1048576)-total_size < 0:
    print("You need to free up some space to leave room for the new OS and potentially your files.")
    sys.exit(1)

process = subprocess.Popen(
    ["diskpart"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
process.stdin.write("select disk 0\n")
process.stdin.write("select volume C\n")
process.stdin.write("shrink desired="+str(total_size)+"\n")
process.stdin.write("create partition primary size="+str(iso_mb)+"\n")
letter_assign = get_letter()
process.stdin.write("assign letter="+letter_assign+"\n")
process.communicate()
subprocess.run(["dd\\dd.exe", "if="+iso_path, "of=\\\\.\\"+letter_assign+":", "bs=4M", "--progress"])
prev_letters.append(letter_assign)
if wants_files:
    process = subprocess.Popen(
        ["diskpart"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    process.stdin.write("select disk 0\n")
    process.stdin.write("create partition primary size="+str(files_size)+"\n")
    process.stdin.write("format fs=exfat quick\n")
    letter_assign = get_letter()
    process.stdin.write("assign letter="+letter_assign+"\n")
    process.communicate()
    os.startfile(letter_assign+":\\")
    with open(letter_assign+":\\README.txt", 'w') as readmeFile:
        readmeFile.write("This is a temporary partition made to keep files along with the new OS.\n")

    input("Press Enter when you are done with transferring files.")
    input("Are you sure you're done? Press Enter again to confirm.")
    input("Final warning, are you really done? Press Enter once again to confirm.")

if input("Do you want to enter the BIOS now to boot into Linux from the boot menu? ").lower().startswith("y"):
    os.system(shutdown_cmd+" /fw")
elif input("WARNING: This method will destroy the Windows bootloader, so without going to the BIOS would straight boot into Linux. This is useful if you have trouble entering the BIOS. Do you want to continue? ").lower().startswith("y"):
    process1 = subprocess.run(
        ["powershell", "-Command", "Get-Partition | ConvertTo-Json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    process = subprocess.Popen(
        ["diskpart"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    process.stdin.write("select disk 0\n")
    efi_number = None
    for idx, partition in enumerate(json.loads(process1.stdout)):
        partition_number = str(partition["PartitionNumber"])+"\n"
        if partition["Type"] == "System" and not efi_number:
            efi_number = partition_number
        
    
    process.communicate()
    process = subprocess.Popen(
        ["diskpart"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    process.stdin.write("select disk 0\n")
    process.stdin.write("select partition "+efi_number)
    letter_assign = get_letter()
    process.stdin.write("assign letter="+letter_assign+"\n")
    process.communicate()
    os.system("rd "+letter_assign+":\\ /s /q")
    print("Restarting now will enter Linux.")
    if input("Do you want to restart now? ").lower().startswith("y"):
        os.system(shutdown_cmd)

else:
    print("You can still enter the BIOS to boot Linux from the boot menu..")
