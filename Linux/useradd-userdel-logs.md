---
title: "useradd/userdel Logs in Linux"
date: "2025-07-30"
tags: ["linux", "logging", "user-management", "system-administration"]
---

# useradd/userdel Logs in Linux

The `useradd` and `userdel` commands typically log their activities in several locations on Linux systems:

## Primary Log Locations

**`/var/log/auth.log`** - On Debian/Ubuntu systems, this contains authentication and authorization logs, including user account changes.

**`/var/log/secure`** - On Red Hat/CentOS/RHEL systems, this serves the same purpose as auth.log.

**`/var/log/messages`** - General system messages that may include user management activities.

## What Gets Logged

These logs typically record:
- User account creation/deletion timestamps
- Which command was executed
- The user who executed the command
- Success or failure of the operation
- Sometimes additional details like UID/GID assignments

## Example Log Entries

You might see entries like:
```
Jan 30 10:15:23 hostname useradd[1234]: new user: name=newuser, UID=1001, GID=1001, home=/home/newuser, shell=/bin/bash
Jan 30 10:20:15 hostname userdel[1235]: delete user 'olduser'
```

## Additional Considerations

- The exact log location can vary depending on your Linux distribution and syslog configuration
- Some systems may also log to `/var/log/syslog`
- You can check your `/etc/rsyslog.conf` or `/etc/syslog-ng.conf` to see the specific logging configuration
- Journal-based systems (systemd) may store these logs in the journal, viewable with `journalctl`

## Viewing Recent Activities

To view recent user management activities, you can use commands like:
```bash
grep -i "useradd\|userdel" /var/log/auth.log
```
or
```bash
journalctl | grep -i "useradd\|userdel"
```
