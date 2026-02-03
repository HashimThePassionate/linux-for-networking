
# 🛡️ Enterprise HAProxy Load Balancer Setup Guide

<details>
<summary><strong>📋 Table of Contents</strong></summary>

1. [📖 Project Overview](#-1-project-overview)
2. [🏗️ Infrastructure Design](#️-2-infrastructure-design-network-architecture)
   - [The 3 Virtual Machines](#the-3-virtual-machines)
3. [⚙️ Step-by-Step Implementation](#️-3-step-by-step-implementation)
   - [Phase 1: Network Configuration](#phase-1-network-configuration-netplan)
   - [Phase 2: Web Server Preparation](#phase-2-web-server-preparation)
   - [Phase 3: Load Balancer Kernel Tuning](#phase-3-load-balancer-kernel-tuning-)
   - [Phase 4: Installing & Configuring HAProxy](#phase-4-installing--configuring-haproxy-)
4. [🧪 Testing & Verification](#-4-testing--verification)
5. [🔒 Security Summary](#-5-security-summary)
6. [🎓 Conclusion](#-conclusion)

</details>

**Project:** High Availability Web Infrastructure on Linux
**Author:** Hashim
**Date:** February 2026
**Environment:** Ubuntu 24.04 (VirtualBox)
**HAProxy Version:** 2.8+

---


## 📖 1. Project Overview

This project simulates a real-world Data Center environment. We built a **Layer 7 Load Balancer** using **HAProxy** that distributes secure traffic (HTTPS) across multiple backend web servers.

**Key Features Implemented:**

* **Load Balancing Algorithms:** Least Connections (Smart traffic distribution).
* **High Availability:** Automatic Failover (If one server dies, the other takes over).
* **Session Persistence:** Sticky Sessions (User stays on the same server).
* **Security:** SSL Termination (HTTPS), Dashboard Protection, and Kernel Tuning.

---

## 🏗️ 2. Infrastructure Design (Network Architecture)

We used **VirtualBox** to create a secure, isolated network.

### The 3 Virtual Machines:

1. **Main VM (Load Balancer & Gateway):**
* **Role:** The "Front Door". It talks to the Internet and the private servers.
* **Adapter 1:** `Bridged Adapter` (Public IP: `192.168.1.13`) - *Connects to Home WiFi.*
* **Adapter 2:** `Internal Network` (Private IP: `192.168.50.1`) - *Connects to Web Servers.*


2. **Web-01 (Backend Server 1):**
* **Role:** Hosts the website.
* **Adapter 1:** `Internal Network` (Private IP: `192.168.50.10`).


3. **Web-02 (Backend Server 2):**
* **Role:** Hosts the website (Replica).
* **Adapter 1:** `Internal Network` (Private IP: `192.168.50.11`).



---

## ⚙️ 3. Step-by-Step Implementation

### Phase 1: Network Configuration (Netplan)

We configured Static IPs to ensure servers always talk on the same lines.

#### 1. Configure Main VM (Load Balancer)

**Command:** `sudo nano /etc/netplan/01-netcfg.yaml`

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:  # Public Interface (Bridged)
      dhcp4: true
    enp0s8:  # Private Interface (Internal)
      dhcp4: no
      addresses: [192.168.50.1/24]

```

**Apply:** `sudo netplan apply`

#### 2. Configure Web-01 (Backend)

**Command:** `sudo nano /etc/netplan/01-netcfg.yaml`

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses: [192.168.50.10/24]
      routes:
        - to: default
          via: 192.168.50.1  # Traffic goes back through Main VM
      nameservers:
        addresses: [8.8.8.8]

```

*(Repeat for Web-02, changing IP to `.11`)*
**Apply:** `sudo netplan apply`

---

### Phase 2: Web Server Preparation

We prepared the backend servers to listen for requests.

**Perform these steps on both Web-01 and Web-02:**

1. **Install Apache Web Server:**
```bash
sudo apt update
sudo apt install apache2 -y

```


2. **Enable SSL (Port 443 Support):**
Even though the Load Balancer handles security, the backend needs to understand SSL traffic.
```bash
sudo a2enmod ssl
sudo a2ensite default-ssl
sudo systemctl restart apache2

```


3. **Create Unique Identity Pages:**
To visually test load balancing, we made each server say its name.
* **On Web-01:** 
```
sudo tee /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Portal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 100%; border-top: 5px solid #3498db; }
        h1 { color: #2c3e50; margin-bottom: 10px; }
        .server-badge { background-color: #3498db; color: white; padding: 10px 20px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 20px; }
        p { color: #7f8c8d; }
        .status { color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Welcome Hashim</h1>
        <p>This request is securely served by your private cloud infrastructure.</p>
        <div class="server-badge">WEB-01 (Primary)</div>
        <p style="margin-top: 20px;">System Status: <span class="status">● OPERATIONAL</span></p>
    </div>
</body>
</html>
EOF`
```

* **On Web-02:** 
```
sudo tee /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Portal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 100%; border-top: 5px solid #e67e22; }
        h1 { color: #2c3e50; margin-bottom: 10px; }
        .server-badge { background-color: #e67e22; color: white; padding: 10px 20px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 20px; }
        p { color: #7f8c8d; }
        .status { color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Welcome Hashim</h1>
        <p>This request is securely served by your private cloud infrastructure.</p>
        <div class="server-badge">WEB-02 (Replica)</div>
        <p style="margin-top: 20px;">System Status: <span class="status">● OPERATIONAL</span></p>
    </div>
</body>
</html>
EOF
```

---

### Phase 3: Load Balancer Kernel Tuning 🏎️

Before installing HAProxy, we optimized the Linux Kernel to handle high traffic and Virtual IPs.

**On Main VM:**

1. **Create Custom Config File:**
```bash
sudo nano /etc/sysctl.d/30-hapee-2.2.conf
```


2. **Add Tuning Parameters:**
```ini
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024 65023
net.ipv4.tcp_max_syn_backlog = 60000
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_synack_retries = 3
net.ipv4.ip_nonlocal_bind = 1
net.core.somaxconn = 60000
```


3. **Apply Settings:**
```bash
sudo sysctl --system
```

---

### Phase 4: Installing & Configuring HAProxy 🛡️

#### 1. Install HAProxy

```bash
# First, remove Nginx if installed (to free up Port 80)
sudo apt remove nginx -y

# Install HAProxy
sudo apt update
sudo apt install haproxy -y
```

#### 2. Generate SSL Certificate (HTTPS)

We created a Self-Signed Certificate to lock the traffic.

```bash
# Generate Key and CRT
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/haproxy.key \
  -out /etc/ssl/certs/haproxy.crt

# Combine into PEM file (Required format for HAProxy)
cat /etc/ssl/certs/haproxy.crt /etc/ssl/private/haproxy.key | sudo tee /etc/ssl/certs/haproxy.pem
```

#### 3. The Configuration File (The Brain) 🧠

We edited the main config to define our logic.

**Command:** `sudo nano /etc/haproxy/haproxy.cfg`

**Full Configuration Code:**

```haproxy
# --- GLOBAL SETTINGS ---
global
    log /dev/log local0
    log /dev/log local1 notice
    user haproxy
    group haproxy
    daemon
    # Admin Socket for internal commands
    stats socket /run/haproxy/admin.sock user haproxy group haproxy mode 660 level admin
    
    # Modern SSL Security Settings (TLS 1.2+)
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

# --- DEFAULTS ---
defaults
    log global
    mode http
    option httplog
    option dontlognull
    # Timeouts to prevent DDoS/Hanging connections
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

# --- FRONTEND (Client Side) ---
frontend http_front-80
    bind *:80
    # Auto-Redirect HTTP to HTTPS
    redirect scheme https if !{ ssl_fc }

    # --- Secure Dashboard ---
    stats uri /haproxy?stats
    stats auth admin:password123  # Password Protected
    stats refresh 10s

frontend http_front-443
    # Bind Port 443 using our PEM Certificate
    bind *:443 ssl crt /etc/ssl/certs/haproxy.pem
    default_backend http_back-80

# --- BACKEND (Server Side) ---
backend http_back-80
    mode http
    balance leastconn   # Use Least Connections Algorithm
    
    # Cookie Insertion for Sticky Sessions
    cookie SERVERUSED insert indirect nocache
    
    # Forward Client IP to Backend (So logs show real user IP)
    option forwardfor
    http-request set-header X-Forwarded-Proto https
    
    # Layer 7 Health Check (Checks if index.html exists)
    option httpchk HEAD / HTTP/1.0
    
    # Define Servers (WS01/WS02 are internal code names for cookies)
    server web-01 192.168.50.10:80 cookie WS01 check fall 3 rise 2
    server web-02 192.168.50.11:80 cookie WS02 check fall 3 rise 2
```

#### 4. Restart HAProxy

```bash
sudo systemctl restart haproxy
```

---

## 🧪 4. Testing & Verification

### Test 1: Dashboard Access (Control Room)

1. Open Browser: `https://192.168.1.13/haproxy?stats`
2. Login: `admin` / `password123`
3. **Result:** You see the HAProxy Statistics Report. Both servers should be **Green**.

### Test 2: Sticky Sessions (Persistence)

1. Open Browser: `https://192.168.1.13`
2. You see: **"I am Web Server 01"**.
3. Refresh page 10 times.
4. **Result:** It stays on **Server 01**. (Because `cookie SERVERUSED` is active).

### Test 3: Failover (High Availability)

1. Keep the browser open on "Web Server 01".
2. Go to VirtualBox and **Power Off** Web-01.
3. Refresh the browser immediately.
4. **Result:** The text changes to **"I am Web Server 02"**.
5. Check Dashboard: Web-01 turns **Red**, Web-02 stays **Green**.

---

## 🔒 5. Security Summary

* **Root Privileges Dropped:** HAProxy runs as a restricted user (`haproxy`), not root.
* **Encrypted Traffic:** All traffic is forced to HTTPS (TLS 1.2+).
* **Info Hiding:** We use Cookie Names (`WS01`) instead of IPs to hide internal network structure from hackers.
* **Access Control:** The Stats Dashboard is password-protected to prevent information leakage via Google Dorks.

---

### 🎓 Conclusion

This setup is **Production Grade**. It is not just a lab experiment; it uses the same configuration principles used by large companies to handle thousands of users securely and reliably.
