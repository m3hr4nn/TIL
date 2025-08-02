# Network Bonding Method of Procedure (MOP)
## Bonding eno1 & eno2 to bond0 with 802.3ad Protocol and MTU 2000

### Document Information
- **Purpose**: Configure network bonding using eno1 and eno2 interfaces
- **Bond Name**: bond0
- **Slave Interfaces**: eno1, eno2
- **Bond Mode**: 802.3ad (LACP)
- **MTU**: 2000
- **Target System**: RHEL 8.x/CentOS 8.x

---

## Prerequisites

### Pre-Execution Checklist
- [ ] Root or sudo access available
- [ ] Both network interfaces (eno1, eno2) are present and functional
- [ ] Switch supports 802.3ad (LACP) bonding
- [ ] Network configuration backup completed
- [ ] Maintenance window scheduled (network interruption expected)

### Verification Commands
```bash
# Check available network interfaces
ip link show

# Verify interfaces are up
nmcli device status

# Check current network configuration
nmcli connection show
```

---

## Method 1: Using nmcli (Command Line)

### Step 1: Remove Existing Connections (optional)
```bash
# List current connections
nmcli connection show

# Remove existing connections for eno1 and eno2 (if any)
nmcli connection delete "Wired connection 1" 2>/dev/null || true
nmcli connection delete "Wired connection 2" 2>/dev/null || true
nmcli connection delete eno1 2>/dev/null || true
nmcli connection delete eno2 2>/dev/null || true
```

### Step 2: Create Bond Master Interface
```bash
# Create bond0 master connection
nmcli connection add type bond \
    con-name bond0 \
    ifname bond0 \
    bond.options "mode=802.3ad,miimon=100,lacp_rate=1"
```

### Step 3: Configure Bond0 Network Settings
```bash
# Configure IP settings (adjust as needed for your network)
# For DHCP:
nmcli connection modify bond0 ipv4.method auto

# For Static IP (example - modify for your network):
# nmcli connection modify bond0 ipv4.method manual
# nmcli connection modify bond0 ipv4.addresses 192.168.1.100/24
# nmcli connection modify bond0 ipv4.gateway 192.168.1.1
# nmcli connection modify bond0 ipv4.dns "8.8.8.8,8.8.4.4"

# Set MTU to 2000
nmcli connection modify bond0 802-3-ethernet.mtu 2000
```

### Step 4: Create Bond Slave Connections
```bash
# Create bond0-port1 (slave connection for eno1)
nmcli connection add type ethernet \
    con-name bond0-port1 \
    ifname eno1 \
    master bond0 \
    slave-type bond

# Create bond0-port2 (slave connection for eno2)  
nmcli connection add type ethernet \
    con-name bond0-port2 \
    ifname eno2 \
    master bond0 \
    slave-type bond
```

### Step 5: Set MTU for Slave Interfaces
```bash
# Set MTU for bond0-port1
nmcli connection modify bond0-port1 802-3-ethernet.mtu 2000

# Set MTU for bond0-port2
nmcli connection modify bond0-port2 802-3-ethernet.mtu 2000
```

### Step 6: Activate Connections
```bash
# Bring up the bond master first
nmcli connection up bond0

# Bring up slave connections
nmcli connection up bond0-port1
nmcli connection up bond0-port2
```

### Step 7: Verification
```bash
# Check connection status
nmcli connection show --active

# Verify bond status
cat /proc/net/bonding/bond0

# Check interface status and MTU
ip link show bond0
ip link show eno1
ip link show eno2

# Test connectivity
ping -c 4 8.8.8.8
```

---

## Method 2: Using nmtui (Text User Interface)

### Step 1: Launch nmtui z
```bash
sudo nmtui
```

### Step 2: Remove Existing Connections
1. Select **"Edit a connection"**
2. Navigate to any existing connections for eno1/eno2
3. Select connection and press **Delete**
4. Confirm deletion
5. Repeat for all existing connections on eno1/eno2

### Step 3: Create Bond Master Connection
1. Select **"Add"**
2. Choose **"Bond"** from connection types
3. Configure bond0:
   - **Connection name**: `bond0`
   - **Device**: `bond0`
   - **Mode**: Select **"802.3ad"**
   - **Monitoring**: Set to **"MII (recommended)"**
   - **Monitoring frequency**: `100`
   - **Link up delay**: `0`
   - **Link down delay**: `0`

### Step 4: Configure Bond Network Settings
1. In the bond0 configuration:
   - **IPv4 CONFIGURATION**: 
     - Select **"Automatic"** for DHCP
     - OR Select **"Manual"** and configure static IP
   - **MTU**: Set to `2000`
2. Press **OK** to save

### Step 5: Create First Slave Connection (bond0-port1)
1. Select **"Add"** 
2. Choose **"Ethernet"**
3. Configure:
   - **Connection name**: `bond0-port1`
   - **Device**: `eno1`
   - **Slave to**: `bond0`
   - **MTU**: `2000`
4. Press **OK** to save

### Step 6: Create Second Slave Connection (bond0-port2)
1. Select **"Add"**
2. Choose **"Ethernet"**
3. Configure:
   - **Connection name**: `bond0-port2`
   - **Device**: `eno2`
   - **Slave to**: `bond0`
   - **MTU**: `2000`
4. Press **OK** to save

### Step 7: Activate Connections
1. Select **"Activate a connection"**
2. Select and activate **bond0**
3. Select and activate **bond0-port1**
4. Select and activate **bond0-port2**
5. Exit nmtui

---

## Post-Configuration Verification

### Step 1: Verify Bond Status
```bash
# Check bond configuration
cat /proc/net/bonding/bond0

# Expected output should show:
# - Bonding Mode: IEEE 802.3ad Dynamic link aggregation
# - Slave Interface: eno1 (Active)
# - Slave Interface: eno2 (Active)
```

### Step 2: Verify Network Connectivity
```bash
# Check IP configuration
ip addr show bond0

# Test connectivity
ping -c 4 -I bond0 8.8.8.8

# Check MTU settings
ip link show bond0 | grep mtu
ip link show eno1 | grep mtu  
ip link show eno2 | grep mtu
```

### Step 3: Verify Connection Persistence
```bash
# Check NetworkManager connections
nmcli connection show

# Verify configuration files
ls -la /etc/sysconfig/network-scripts/ifcfg-*
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Bond interface not coming up
```bash
# Check NetworkManager service
systemctl status NetworkManager

# Restart NetworkManager if needed
systemctl restart NetworkManager

# Manually bring up interfaces
ip link set eno1 up
ip link set eno2 up
nmcli connection up bond0
```

#### Issue: Slave interfaces not joining bond
```bash
# Check for conflicting connections
nmcli connection show --active

# Ensure slave connections are properly configured
nmcli connection show bond0-port1
nmcli connection show bond0-port2

# Restart connections
nmcli connection down bond0-port1
nmcli connection down bond0-port2
nmcli connection up bond0-port1
nmcli connection up bond0-port2
```

#### Issue: MTU not applied correctly
```bash
# Check current MTU
ip link show | grep mtu

# Manually set MTU if needed
ip link set bond0 mtu 2000
ip link set eno1 mtu 2000
ip link set eno2 mtu 2000

# Update connection MTU
nmcli connection modify bond0 802-3-ethernet.mtu 2000
nmcli connection modify bond0-port1 802-3-ethernet.mtu 2000
nmcli connection modify bond0-port2 802-3-ethernet.mtu 2000
```

---

## Rollback Procedure

### Emergency Rollback Steps
```bash
# Bring down bond connections
nmcli connection down bond0
nmcli connection down bond0-port1
nmcli connection down bond0-port2

# Delete bond connections
nmcli connection delete bond0
nmcli connection delete bond0-port1
nmcli connection delete bond0-port2

# Recreate individual interface connections
nmcli connection add type ethernet con-name eno1 ifname eno1
nmcli connection add type ethernet con-name eno2 ifname eno2

# Bring up individual interfaces
nmcli connection up eno1
nmcli connection up eno2
```

---

## Configuration Files Reference

### Bond Master Configuration (/etc/sysconfig/network-scripts/ifcfg-bond0)
```bash
TYPE=Bond
BONDING_MASTER=yes
BOOTPROTO=dhcp  # or 'static' for manual IP
ONBOOT=yes
BONDING_OPTS="mode=802.3ad miimon=100 lacp_rate=1"
MTU=2000
NAME=bond0
DEVICE=bond0
```

### Slave Configuration Examples
**ifcfg-bond0-port1:**
```bash
TYPE=Ethernet
BOOTPROTO=none
ONBOOT=yes
MASTER=bond0
SLAVE=yes
MTU=2000
NAME=bond0-port1
DEVICE=eno1
```

**ifcfg-bond0-port2:**
```bash
TYPE=Ethernet
BOOTPROTO=none
ONBOOT=yes
MASTER=bond0
SLAVE=yes
MTU=2000
NAME=bond0-port2
DEVICE=eno2
```

---

## Validation Checklist

### Post-Implementation Verification
- [ ] Bond0 interface is active and configured
- [ ] Both eno1 and eno2 are enslaved to bond0
- [ ] MTU is set to 2000 on all interfaces
- [ ] 802.3ad mode is active
- [ ] Network connectivity is functional
- [ ] Configuration persists after reboot
- [ ] Switch shows LACP negotiation successful
- [ ] Performance testing completed (if required)

### Documentation Updates
- [ ] Network diagram updated
- [ ] Configuration management system updated
- [ ] Monitoring systems configured for bond0
- [ ] Documentation shared with team

---

**Note**: Always test in a non-production environment first and ensure your network switch supports 802.3ad (LACP) before implementing in production.
