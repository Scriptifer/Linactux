import subprocess
import os
import string
import math
import shutil
import ctypes
import sys
import json
import platform
import time
platform_os = platform.system()
if platform_os != "Windows":
    print("This script is for switching from Windows to Linux without a USB easily, not from other systems. We are thinking about whether or not to add the ability to change Linux distributions.")
    sys.exit()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    script = sys.argv[0]
    params = ' '.join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f"{script} {params}", None, 1)

if not is_admin():
    run_as_admin()
    sys.exit()

check_process = subprocess.run(
    ["powershell", "-Command", "Confirm-SecureBootUEFI"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

shutdown_cmd = "shutdown /r /t 0"
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
prev_process = subprocess.run(
    ["powershell", "-Command", f"Get-Volume | Where-Object {{ $_.DriveType -eq 'CD-ROM' }} | ConvertTo-Json"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
prev_output = json.loads(prev_process.stdout.strip())
if isinstance(prev_output, dict):
    prev_output = [prev_output]

for idx, entry in enumerate(prev_output):
    prev_letters.append(entry['DriveLetter'])

def get_letter():
    letter_assign = ""
    for letter in string.ascii_uppercase:
        if not (os.path.exists(letter+":") or (letter in prev_letters)):
            letter_assign = letter
            break


    return letter_assign

mount_process = subprocess.run(
    ["powershell", "-Command", f"Mount-DiskImage -ImagePath '{iso_path}'; Get-Volume | Where-Object {{ $_.DriveType -eq 'CD-ROM' }} | ConvertTo-Json"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
mount_output = json.loads(mount_process.stdout.strip().split("\n\n")[1])
mounted = None
iso_mb = math.inf
for idx, entry in enumerate(mount_output):
    if not (entry['DriveLetter'] in prev_letters):
        mounted = entry


if not mounted:
    print("Couldn't find mounted drive from ISO.")
    sys.exit(1)

mounted_letter = mounted['DriveLetter']
size_measure_p = subprocess.run(
    ["powershell", "-Command", "(Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB"],
    cwd=mounted_letter+":\\",
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
iso_mb = round(float(size_measure_p.stdout.strip()))
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
fs_typelinux = "fat32"
if iso_mb > 3800:
    fs_typelinux = "exfat"

process.stdin.write("format fs="+fs_typelinux+" quick\n")
letter_assign = get_letter()
process.stdin.write("assign letter="+letter_assign+"\n")
process.communicate()
subprocess.run(["xcopy", mounted_letter+":\\*.*", letter_assign+":\\", "/s/e/f"])
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

print("Alright, let's go!")
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
    if partition["Type"] == "Recovery" or partition["Type"] == "Reserved":
        process.stdin.write("select partition "+partition_number)
        process.stdin.write("delete partition override\n")
    elif partition["Type"] == "System" and not efi_number:
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
os.system(r'''cmd /c "bcdedit /enum all | findstr /i "identifier" | for /f "tokens=2 delims={}" %a in ('more') do bcdedit /delete {%a} /f"''')
os.system("rd "+letter_assign+":\\ /s /q")
os.system(shutdown_cmd)
