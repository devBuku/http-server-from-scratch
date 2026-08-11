### `ss`

Linux command to inspect sockets and network connections.

```bash
sudo ss -tulpn
```

Flags:

* `-t` → TCP
* `-u` → UDP
* `-l` → listening
* `-p` → show process
* `-n` → show numeric IPs/ports

Example:

```text
tcp LISTEN 0 511 *:3000 *:* users:(("node",pid=4653,fd=22))
```

This means a process is **listening for TCP connections on port `3000`**.

* `pid` → process ID
* `fd` → file descriptor (Linux represents sockets with file descriptors)
