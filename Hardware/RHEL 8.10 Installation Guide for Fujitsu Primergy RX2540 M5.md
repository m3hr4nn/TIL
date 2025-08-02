# RHEL 8.10 Installation Guide for Fujitsu Primergy RX2540 M5

## Prerequisites

### Hardware Requirements
- Fujitsu Primergy RX2540 M5 server
- Minimum 2GB RAM (4GB+ recommended)
- At least 20GB available disk space
- DVD drive or USB port for installation media
- Network connectivity (optional but recommended)

### Software Requirements
- RHEL 8.10 ISO image
- USB flash drive (8GB+) or DVD for installation media
- Valid RHEL subscription or evaluation license

## Phase 1: Pre-Installation Setup

### Step 1: Download RHEL 8.10 ISO
1. Visit the Red Hat Customer Portal
2. Navigate to Downloads section
3. Select Red Hat Enterprise Linux
4. Download RHEL 8.10 Binary DVD ISO (rhel-8.10-x86_64-dvd.iso)

### Step 2: Create Installation Media
#### For USB Installation:
1. Insert USB drive into your workstation
2. Use `dd` command on Linux or Rufus on Windows:
   ```bash
   sudo dd if=rhel-8.10-x86_64-dvd.iso of=/dev/sdX bs=4M status=progress
   ```
3. Replace `/dev/sdX` with your USB device path

#### For DVD Installation:
1. Burn the ISO to a DVD using your preferred burning software
2. Verify the burn completed successfully

### Step 3: Prepare Server Hardware
1. Power on the Fujitsu Primergy RX2540 M5
2. Access iRMC (Integrated Remote Management Controller):
   - Default IP: Check server label or DHCP assignment
   - Default credentials: admin/admin
3. Configure RAID if required:
   - Access RAID configuration during boot (Ctrl+R for LSI controllers)
   - Create appropriate RAID arrays based on your requirements
4. Insert installation media (USB/DVD)

## Phase 2: BIOS/UEFI Configuration

### Step 4: Access System BIOS
1. Power on or restart the server
2. Press **F2** during POST to enter BIOS Setup
3. Navigate to Boot menu

### Step 5: Configure Boot Settings
1. Set boot mode to UEFI (recommended) or Legacy BIOS
2. Enable secure boot if required by your organization
3. Set boot priority:
   - First: USB/DVD drive
   - Second: Hard disk
4. Save settings and exit (F10)

## Phase 3: RHEL Installation

### Step 6: Boot from Installation Media
1. Restart server with installation media inserted
2. Select "Install Red Hat Enterprise Linux 8.10" from boot menu
3. Press Enter to begin installation

### Step 7: Language and Keyboard Selection
1. Select your preferred language (English recommended for servers)
2. Choose keyboard layout
3. Click "Continue"

### Step 8: Installation Summary Configuration

#### Network & Host Name
1. Click "Network & Host Name"
2. Enable network interface (toggle switch to ON)
3. Configure IP settings:
   - For DHCP: Leave as automatic
   - For static IP: Click "Configure" and set manual IP, netmask, gateway, DNS
4. Set hostname (e.g., primergy-rhel8.domain.com)
5. Click "Done"

#### Time & Date
1. Click "Time & Date"
2. Select appropriate timezone
3. Enable NTP if network is available
4. Add NTP servers if required
5. Click "Done"

#### Installation Destination
1. Click "Installation Destination"
2. Select target disk(s)
3. Choose partitioning scheme:
   - **Automatic**: Let installer create partitions
   - **Custom**: Create custom partition layout
4. For custom partitioning:
   - `/boot`: 1GB (ext4)
   - `/boot/efi`: 200MB (EFI System Partition) - UEFI only
   - `swap`: 2x RAM size or 8GB maximum
   - `/`: Remaining space (xfs recommended)
   - Optional: Separate `/home`, `/var`, `/tmp` partitions
5. Click "Done"

#### Software Selection
1. Click "Software Selection"
2. Choose base environment:
   - **Server**: Basic server installation
   - **Server with GUI**: Server with graphical interface
   - **Minimal Install**: Minimal installation
3. Select additional software add-ons as needed
4. Click "Done"

#### Security Policy
1. Click "Security Policy" (if available)
2. Select appropriate security profile or leave default
3. Click "Done"

### Step 9: User Configuration

#### Root Password
1. Click "Root Password"
2. Set a strong root password
3. Confirm password
4. Click "Done"

#### User Creation
1. Click "User Creation"
2. Create a regular user account:
   - Full name
   - Username
   - Password
   - Check "Make this user administrator" if needed
3. Click "Done"

### Step 10: Begin Installation
1. Review all settings in Installation Summary
2. Click "Begin Installation"
3. Wait for installation to complete (typically 15-30 minutes)

## Phase 4: Post-Installation Configuration

### Step 11: First Boot
1. Remove installation media
2. Restart the server
3. Complete initial setup wizard if GUI is installed
4. Log in as root or created user

### Step 12: System Registration
1. Register system with Red Hat:
   ```bash
   sudo subscription-manager register --username=your_username
   ```
2. Attach subscription:
   ```bash
   sudo subscription-manager attach --auto
   ```
3. Enable repositories:
   ```bash
   sudo subscription-manager repos --enable=rhel-8-for-x86_64-baseos-rpms
   sudo subscription-manager repos --enable=rhel-8-for-x86_64-appstream-rpms
   ```

### Step 13: System Updates
1. Update system packages:
   ```bash
   sudo dnf update -y
   ```
2. Restart if kernel updates were installed:
   ```bash
   sudo reboot
   ```

### Step 14: Fujitsu-Specific Drivers (if needed)
1. Download Fujitsu ServerView Suite from Fujitsu support site
2. Install management tools:
   ```bash
   sudo dnf install -y fujitsu-svs-*.rpm
   ```
3. Configure monitoring and management as required

### Step 15: Additional Configuration

#### Firewall Configuration
```bash
# Check firewall status
sudo firewall-cmd --state

# Enable required services
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

#### SELinux Configuration
```bash
# Check SELinux status
sestatus

# Modify if needed (not recommended to disable)
sudo vi /etc/selinux/config
```

#### Network Configuration
```bash
# Configure static IP if not done during installation
sudo nmtui
```

## Phase 5: Verification and Testing

### Step 16: System Verification
1. Check system information:
   ```bash
   hostnamectl
   uname -a
   cat /etc/redhat-release
   ```

2. Verify hardware detection:
   ```bash
   lscpu
   lsmem
   lsblk
   lspci
   ```

3. Check network connectivity:
   ```bash
   ip addr show
   ping 8.8.8.8
   ```

4. Verify services:
   ```bash
   systemctl status
   systemctl list-failed
   ```

### Step 17: Final Steps
1. Create system backup/snapshot if using virtualization
2. Document configuration settings
3. Set up monitoring and logging as required
4. Configure additional services (web server, database, etc.)

## Troubleshooting Common Issues

### Boot Issues
- Verify boot order in BIOS
- Check installation media integrity
- Ensure RAID configuration is proper

### Network Issues
- Verify cable connections
- Check switch/router configuration
- Validate IP settings and DNS

### Hardware Issues
- Update server firmware
- Check Fujitsu support documentation
- Verify hardware compatibility

## Useful Commands Reference

```bash
# System information
hostnamectl status
cat /etc/os-release
dmidecode -s system-product-name

# Hardware information
lscpu
free -h
df -h
lsblk

# Network configuration
nmcli device status
nmcli connection show

# Service management
systemctl status service_name
systemctl enable service_name
systemctl start service_name
```

## Additional Resources

- Red Hat Enterprise Linux 8 Installation Guide
- Fujitsu Primergy RX2540 M5 Documentation
- Red Hat Customer Portal
- Fujitsu Support Portal

---

**Note**: This guide provides general installation steps. Always consult your organization's specific requirements and security policies before installation.
