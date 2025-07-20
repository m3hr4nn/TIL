# Linux Mint: Enabling Broadcom BCM43142A0 Bluetooth

This document describes the exact steps taken to get a Broadcom BCM43142A0 USB Bluetooth adapter working on Linux Mint. The firmware file was obtained from the winterheart GitHub repository.

---

## 1. Identify the Adapter

```bash
lsusb | grep -i bluetooth
# Bus 002 Device 004: ID 04ca:2006 Lite-On Technology Corp. Broadcom BCM43142A0 Bluetooth Device
```

- **Vendor ID:** 04ca
- **Product ID:** 2006
- **Chipset:** BCM43142A0

## 2. Download & Install Firmware

Create the firmware directory:

```bash
sudo mkdir -p /lib/firmware/brcm
```

Download the .hcd blob from GitHub:

```bash
cd /tmp
wget https://raw.githubusercontent.com/winterheart/broadcom-bt-firmware/master/brcm/BCM43142A0-04ca-2006.hcd
```

Copy the file into the firmware directory:

```bash
sudo cp BCM43142A0-04ca-2006.hcd /lib/firmware/brcm/
```

## 3. Reload the Bluetooth USB Driver

```bash
sudo modprobe -r btusb
sudo modprobe btusb
```

## 4. Verify Firmware Loading

```bash
dmesg | grep -i BCM43142A0
```

Expected output snippet:

```
Bluetooth: hci0: BCM: 'brcm/BCM43142A0-04ca-2006.hcd'
Bluetooth: hci0: BCM43142A0 patch completed
```

## 5. Unblock Bluetooth (rfkill)

Check block status:

```bash
rfkill list all
```

If "Soft blocked: yes", unblock:

```bash
sudo rfkill unblock bluetooth
```

If "Hard blocked: yes", toggle your laptop's Bluetooth/airplane-mode key or check BIOS.

Confirm both are no:

```bash
rfkill list all
# Soft blocked: no
# Hard blocked: no
```

## 6. Bring Up the HCI Interface

```bash
sudo hciconfig hci0 up
hciconfig -a
# Should show hci0 as UP RUNNING
```

## 7. Restart Bluetooth Service

```bash
sudo systemctl restart bluetooth
```

## 8. Pair & Connect via bluetoothctl

```bash
bluetoothctl
```

Inside the prompt:

```bash
power on
agent on
default-agent
scan on
# wait for your device to appear as [NEW] Device AA:BB:CC:DD:EE:FF <Name>
pair AA:BB:CC:DD:EE:FF
trust AA:BB:CC:DD:EE:FF
connect AA:BB:CC:DD:EE:FF
scan off
quit
```

## 9. (Optional) Audio Support for Headsets/Speakers

```bash
sudo apt install pulseaudio-module-bluetooth pavucontrol
```

Restart services:

```bash
pactl exit
sudo systemctl restart bluetooth
# Then use pavucontrol → Configuration to select A2DP
```

## 10. Final Check

- No more "Authentication Failed (0x05)" or timeout errors in dmesg/journalctl -u bluetooth
- Devices appear and connect successfully in both bluetoothctl and the Mint GUI
- Audio devices available in PulseAudio
