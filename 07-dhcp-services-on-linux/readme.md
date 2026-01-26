# 📡 Basic DHCP Operation

## 📘 Overview

**DHCP (Dynamic Host Configuration Protocol)** is a system that allows network administrators to centrally manage and automate the network configuration of devices.

* **The Problem:** Without DHCP, an administrator would have to manually type in the IP address, Subnet Mask, Gateway, and DNS server for every single computer, printer, and phone in the building (Static IP).
* **The Solution:** DHCP allows devices to request these settings automatically when they turn on. The DHCP server holds a pool of addresses and assigns them to devices as needed.

---

## 🔄 The DORA Sequence

The communication process between a client (computer) and a DHCP server is known as the **DORA** sequence. This stands for **D**iscover, **O**ffer, **R**equest, and **A**cknowledgment.

Since DHCP uses the **UDP** protocol (which does not establish a persistent connection like TCP), the messages are broadcasted to the local network.

### 1️⃣ Discover (Client -> Server)

* **Concept:** The client wakes up. It has no IP address and doesn't know if a DHCP server exists. It yells out to the entire network.
* **Message:** "Are there any DHCP servers out there? Send me some details?"
* **Technical Details:**
* **Source IP:** `0.0.0.0` (Because the client doesn't have an IP yet).
* **Destination IP:** `255.255.255.255` (Broadcast to everyone).
* **Ports:** Senders from Client Port 68 to Destination Port 67.



### 2️⃣ Offer (Server -> Client)

* **Concept:** A DHCP server hears the shout. It checks its pool of available addresses and selects one for the client.
* **Message:** "I am your DHCP Server. Here is an address, subnet mask, gateway, and DNS info, for a lease time of XXXX Seconds."
* **Technical Details:**
* Sent from the Server's IP/MAC address to the Client's MAC address.



### 3️⃣ Request (Client -> Server)

* **Concept:** The client receives the offer. Even though the server "Offered" it, the client must formally "Request" to accept it. This seems redundant but is necessary because multiple servers might have sent offers; the client is announcing which offer it is accepting.
* **Message:** "Thanks for the DHCP Offer, it's a deal! Here's all that DHCP information you sent, does this look good?"
* **Technical Details:**
* The client essentially echoes the configuration back to the server for confirmation.



### 4️⃣ Acknowledgment (Server -> Client)

* **Concept:** The server finalizes the deal, marks that IP as "taken" in its database, and sends the final approval.
* **Message:** "We're all Good! Here's the DHCP Lease information again, just to be sure."
* **Technical Details:**
* The client can now configure its network interface with the assigned IP and begin communicating on the network.



---

## 📊 Analyzing the Traffic (Wireshark)

We can see this exact exchange in a packet capture. Below is a detailed explanation of the output shown in **Figure 7.2**.

| Source | Destination | Protocol | Info | Explanation |
| --- | --- | --- | --- | --- |
| **0.0.0.0** | **255.255.255.255** | DHCP | **DHCP Discover** | The client (0.0.0.0) broadcasts looking for a server. Note the **Transaction ID 0x494cdf16**. |
| **0.0.0.0** | **255.255.255.255** | DHCP | **DHCP Discover** | A second Discover packet (Transaction ID **0xe5cc873a**). This is a separate request, likely from a different process or retry. |
| **192.168.122.1** | **192.168.122.157** | DHCP | **DHCP Offer** | The server (`192.168.122.1`) replies to the *first* Discover (matching ID **0x494cdf16**). It offers the IP `192.168.122.157`. |
| **0.0.0.0** | **255.255.255.255** | DHCP | **DHCP Discover** | Another broadcast (Retry of ID **0xe5cc873a**). |
| **192.168.122.1** | **192.168.122.157** | DHCP | **DHCP Offer** | The server replies to the *second* Discover (ID **0xe5cc873a**). |
| **0.0.0.0** | **255.255.255.255** | DHCP | **DHCP Request** | The client accepts the offer for ID **0xe5cc873a**. It still uses Source `0.0.0.0` because the IP isn't officially assigned until the ACK is received. |
| **192.168.122.1** | **192.168.122.157** | DHCP | **DHCP ACK** | The server confirms the lease for ID **0xe5cc873a**. The process is complete. |

### 🔑 Key Technical Concepts

1. **Transaction ID:**
* Since UDP is stateless (packets don't know they belong to a stream), DHCP uses a **Transaction ID** (e.g., `0xe5cc873a`) to link the four packets together. The client generates this ID, and the server includes it in the reply so the client knows "This Offer is for *my* Discover request."


2. **Broadcast Addresses:**
* The "Important Note" in the text highlights that the client effectively has **no identity** (IP `0.0.0.0`) during the Discover and Request phases. Therefore, it must yell to the entire room (Broadcast `255.255.255.255`) to ensure the server hears it.


3. **Port Usage (From Figure 7.1):**
* **Client:** Listens/Sends on UDP Port **68**.
* **Server:** Listens/Sends on UDP Port **67**.

---

# 🌐 DHCP Requests from Other Subnets (Forwarders & Relays)

## 📘 The Problem: Broadcast Isolation

In most corporate networks, servers and workstations are separated into different VLANs or subnets for security and organization.

* **Workstations:** Vlan 10 (`192.168.10.x`)
* **Servers (inc. DHCP):** Vlan 20 (`192.168.20.x`)

**The Conflict:** The DHCP DORA sequence relies on **Broadcasts** (Destination `255.255.255.255`). By design, routers and switches **do not forward broadcast traffic** from one subnet to another. If they did, the entire internet would flood with noise.

* **Result:** The client yells "Is anyone there?" (Discover), but the DHCP server never hears it because the router blocks the shout.

---

## 🛠️ The Solution: DHCP Relay (IP Helper)

To fix this, we place a **DHCP Forwarder** (also called a Relay or Helper) on the network segment where the clients are.

* **Who is the Relay?** Almost always, this role is performed by the **Router** or **Layer 3 Switch** that acts as the client's Default Gateway.
* **Why the Router?** Since the router has a "leg" in the client's subnet and a path to the server's subnet, it is the perfect bridge.

### 🔄 How the Relay Works (Figure 7.3)

The relay converts the local broadcast into a targeted message.

1. **Client Broadcasts:** The client sends a normal `DHCP DISCOVER` (Broadcast) to the local network.
2. **Relay Intercepts:** The Router (configured as a Relay) hears this broadcast. Instead of dropping it, it captures it.
3. **Unicast Conversion:** The Router wraps the DHCP message in a new IP packet.
* **Source:** The Router's Interface IP (e.g., `192.168.10.1`).
* **Destination:** The specific IP of the remote DHCP Server (e.g., `10.10.10.10`).


4. **Forwarding:** The Router sends this **Unicast** packet directly to the server.
5. **Server Reply:** The server replies to the Router (Unicast).
6. **Broadcast Reply:** The Router receives the reply, strips the unicast headers, and broadcasts the `DHCP OFFER` back onto the local segment for the client to hear.

---

## ⚙️ Cisco Implementation

On Cisco devices, this feature is called an "IP Helper Address." It is applied to the interface facing the *clients*.

**Command:**

```cisco
interface VLAN <Client_VLAN_ID>
 ip helper-address 10.10.10.10
```

**Explanation:**

* **`interface VLAN ...`**: Selects the interface where the clients live.
* **`ip helper-address 10.10.10.10`**: Tells the router, "If you see a broadcast on this interface (like DHCP), grab it and forward it directly to the server at `10.10.10.10`."

---

## 📦 Packet Analysis: What Changes?

The text clarifies an important technical detail about how the packets change during this process.

* **Layer 3 (IP Headers):** These change significantly. Between the Client and Router, it is Broadcast (`255.255.255.255`). Between the Router and Server, it is Unicast (Real IPs).
* **Layer 7 (DHCP Payload):** The actual DHCP data inside the packet remains mostly unchanged. The DHCP protocol fields still contain the original **Client MAC Address** so the server knows who the lease is for.

---

# ⚙️ DHCP Options

## 📘 Overview

While the primary job of DHCP is to assign an IP address, its power extends far beyond that. **DHCP Options** allow the server to deliver specialized configuration parameters to devices during the boot process.

* **How it works:** When a client sends a `DISCOVER` packet, it includes a "Parameter Request List." This is the client saying, "I know how to handle these specific settings; please send them if you have them."
* **The Server's Role:** In the `OFFER` packet, the server tries to fill in as many of these requested details as possible.

### 📋 Common Options (The Basics)

Every standard workstation (PC/Laptop) requests these four core options:

1. **Subnet Mask** (Option 1)
2. **Router / Default Gateway** (Option 3)
3. **DNS Server List** (Option 6)
4. **DNS Domain Name** (Option 15)

---

## 📞 Advanced Usage: VoIP Phones & Special Devices

In corporate networks, devices like **VoIP Phones**, **Wireless Access Points (WAPs)**, and **PXE Boot** clients need more than just an IP address. They need to know *how* to function.

* **VoIP Phones:** Need to know the IP of the phone system (PBX) and where to download their configuration files (TFTP/HTTP server).
* **Wireless Access Points:** Need to find their central Wireless Controller.
* **PXE Clients:** Need to find a boot image to load an operating system over the network.

### 🏭 Vendor-Specific VoIP Options

Different phone manufacturers use different DHCP Option numbers to deliver this information. Below is a breakdown of common vendor requirements:

Fine. The table you pasted was trying very hard and still failed basic Markdown hygiene. Here’s a **clean, properly formatted Markdown table** that will actually render correctly instead of embarrassing you in front of GitHub or a wiki.

---

### 🏭 Vendor-Specific VoIP DHCP Options

| Vendor       | Option # | Function                                 | Syntax / Notes                                                |
| ------------ | -------- | ---------------------------------------- | ------------------------------------------------------------- |
| **Cisco**    | **150** or **66**  | Points to TFTP Server IP                 | Can list **multiple IP addresses**                            |                             |
| **Avaya**    | **176**  | VLAN & File Server config (older phones) | `MCIPADD=<pbx_ip>,MCPORT=1719,TFTPSRVR=<tftp_server>`         |
|              | **242**  | VLAN & File Server config (newer phones) | Same syntax as Option 176                                     |
| **Mitel**    | **156**  | Server IPs & VLAN tagging                | `ftpservers=<IP>,configservers=<IP>,layer2tagging=1,vlanid=x` |
| **Shoretel** | **156**  | Server config (vendor-specific format)   | `ftpservers=ip_address,country=n,language=n...`               |

---

> **Note:** Even though Mitel and Shoretel both use **Option 156**, the *syntax* (the format of the text inside the option) is different.

---

## 🔍 Troubleshooting DHCP Options

If a device (like a phone) gets an IP address but fails to register or download its config, the issue is often a missing or incorrect DHCP Option.

**The Golden Rule:** Always look at the **DHCP DISCOVER** packet (the first packet in the DORA sequence).

* **Why?** This packet contains the *client's* specific request list.
* **Diagnosis:** If the client requests Option 156 but the server sends Option 66, the phone will ignore it. You must configure the server to match exactly what the client is asking for.

---

# 🔒 Securing DHCP Services

## 📘 Overview

Securing DHCP is unique because the defense strategy rarely happens on the DHCP server itself. Since the DHCP protocol is designed to be open and "automagical" (allowing any device to plug in and get an IP), adding authentication or encryption directly to the protocol adds too much complexity.

Instead, the security burden falls on the **Network Switches**. We must control the "topology" of trust—defining *where* legitimate DHCP answers are allowed to come from.

---

## 🚨 Threat 1: The Rogue DHCP Server

This is the most common DHCP issue. It can be accidental or malicious.

### 1. The Accidental Rogue (Home Router Scenario)

* **Scenario:** An employee brings a Wi-Fi router from home and plugs it into the corporate network to get better signal.
* **The Problem:** The home router has its own DHCP server enabled (usually `192.168.1.x`). It starts racing the corporate server to answer DHCP requests.
* **The Impact:** Corporate workstations receive "home" IP addresses. They lose access to corporate file servers, printers, and the internet because they are on the wrong subnet.

### 2. The Malicious Rogue (Layer 3 MITM)

An attacker can intentionally set up a Rogue DHCP server to intercept traffic. This is a **Machine-in-the-Middle (MiTM)** attack.

* **Mechanism:** The attacker sets up a DHCP server that assigns the **Attacker's IP** as the **Default Gateway**.
* **The Flow (Figure 7.4):**
1. The **Malicious DHCP Server** answers the client's request *faster* than the legitimate server.
2. The Client sends all its traffic to the Attacker (thinking it is the Router).
3. The Attacker inspects/modifies the traffic and then forwards it to the real router so the user doesn't notice the interruption.



### 3. The WPAD Attack (Option 252)

This is a more sophisticated attack targeting web traffic specifically.

* **Mechanism:** The attacker uses **DHCP Option 252**. This option tells clients where to find a **Proxy Auto-Configuration (PAC)** file (e.g., `http://attacker.com/proxy.pac`).
* **The Flow (Figure 7.5):**
1. The **Malicious DHCP Server** wins the race and sends Option 252.
2. The Client downloads the malicious PAC file.
3. The Client sends its web traffic to the **Malicious Proxy Server** defined in the file.
4. The Attacker steals credentials (like banking logins) via fake websites before forwarding the traffic.



---

## 🛡️ The Defense: DHCP Snooping

The industry-standard defense against Rogue DHCP servers is **DHCP Snooping**. This feature turns the switch into a security guard that inspects DHCP packets.

### How it Works

1. **Untrusted Ports (Default):** All user-facing ports are considered "Untrusted." They are allowed to send DHCP Requests (asking for an IP), but if they try to send a **DHCP Offer** (giving an IP), the switch blocks the packet and shuts down the port.
2. **Trusted Ports:** We explicitly tell the switch which ports connect to legitimate DHCP servers (usually the **Uplink** ports connecting to the core network).

### ⚙️ Configuration (Cisco Example)

We enable snooping globally for specific VLANs, then trust the uplink.

```cisco
! Enable snooping for VLANs 1, 2, and 10
ip dhcp snooping vlan 1 2 10

! Configure the Uplink (Connection to Server)
interface e1/48
 ip dhcp snooping trust
```

### ⚙️ Configuration (HP/Aruba Example)

Some vendors allow you to trust the **Server IP Address** instead of just the port. This is easier to manage because you can copy/paste the same config to every switch without worrying about which specific port is the uplink.

```bash
dhcp-snooping
dhcp-snooping vlan 1 2 10
dhcp-snooping authorized-server <Legitimate_DHCP_IP>
```

### 🏢 Data Center Strategy

In the server room (where the actual DHCP server lives, likely as a Virtual Machine), we have two choices:

1. **Trust the Uplinks:** Configure snooping on the server switches, trusting the ports connecting to the Hypervisors.
2. **Physical Security:** Skip snooping in the data center entirely. Rely on the fact that the server cabinets are physically locked and only authorized admins can create VMs. This is the most common approach to reduce complexity.

---

## 🚨 Threat 2: The Rogue DHCP Client

This is when an unauthorized device (like a hacker's laptop or a "pwnplug") plugs into an open wall jack to get onto the network.

### 🚫 The Old Defense: Static MAC Filtering

* **Method:** Maintain a giant database of every allowed MAC address in the company. Manually approve every new laptop.
* **Why it fails:** It is an administrative nightmare. Nobody wants to manually register every new device.

### ✅ The Modern Defense: 802.1x Authentication

* **Method:** The network port itself is locked. When a device plugs in, it must prove its identity before the switch allows any traffic (including DHCP).
* **Technology:** Uses **RADIUS** and **Certificates**.
* The Client presents a Certificate.
* The RADIUS server validates it.
* If trusted, the switch port unlocks.
*(This topic is covered deeply in Chapters 8 and 9 of the text).*


---

# 🛠️ Installing and Configuring a DHCP Server

This guide details the process of setting up an **ISC DHCP Server** on Linux. We will cover the installation, global configuration, scope definition, and service verification.

---

## 📦 Step 1: Installation

We begin by installing the industry-standard DHCP server package using `apt`.

**Command:**

```bash
hashim@hashim-server:~$ sudo apt-get install isc-dhcp-server
```

* **`sudo`**: Runs the command with administrative privileges.
* **`apt-get install`**: The package manager command to download and install software.
* **`isc-dhcp-server`**: The specific package name for the Internet Systems Consortium DHCP server.

---

## ⚙️ Step 2: Basic Global Configuration

Once installed, we configure the global options in the main configuration file: `/etc/dhcp/dhcpd.conf`. These settings apply to the entire server unless overridden by a specific scope.

**Command:**

```bash
hashim@hashim-server:~$ sudo nano /etc/dhcp/dhcpd.conf
```

### 1. Global Parameters

Add or modify the following lines at the top of the file:

```nginx
default-lease-time 3600;
max-lease-time 7200;
ping-check true;
ping-timeout 2;
option domain-name-servers 10.0.2.15;
```

**Explanation of Settings:**

* **Lease Times (`default-lease-time` / `max-lease-time`):**
* These variables determine how long an IP address belongs to a client before it expires.
* **Why it matters:**
* **Incident Response:** Longer leases (e.g., 3-4 days) are preferred for internal networks. They ensure a specific IP stays associated with a specific user for a predictable time, making log analysis easier during investigations.
* **Guest Networks:** Shorter leases are better for guest Wi-Fi to prevent running out of IP addresses as transient users come and go.


* **Renewal:** Clients attempt to renew their lease when **50%** of the time has passed.


* **Ping Check (`ping-check true`):**
* This is a critical safety feature. Before the server assigns an IP to a client, it pings that IP address.
* **Goal:** To prevent **Duplicate IP Addresses**. If the ping gets a reply, the server knows someone else (perhaps with a static IP) is using that address and will not assign it.
* **Timeout:** We increased the `ping-timeout` to **2 seconds** (default is 1 second) to be safe.


* **DNS Servers (`option domain-name-servers`):**
* Defines the central DNS server (`10.0.2.15`) that all clients should use.



### 2. The Authoritative Directive

Further down in the file, you must uncomment this line:

```nginx
authoritative;
```

* **Meaning:** This tells the network, "I am the official DHCP server for this network." If a client requests an IP that is invalid for this segment, an authoritative server can explicitly deny it (sending a DHCPNAK), forcing the client to request a new, valid IP immediately.

---

## 🌐 Step 3: Defining the Scope (Subnet)

We must define the network range (subnet) we want to manage. Add this block to the end of `/etc/dhcp/dhcpd.conf`:

```nginx
# Specify the network address and subnet-mask
subnet 10.0.2.0 netmask 255.255.255.0 {
  # Specify the default gateway address
  option routers 10.0.2.1;
  # Specify the subnet-mask
  option subnet-mask 255.255.255.0;
  # Specify the range of leased IP addresses
  range 10.0.2.50 10.0.2.100;
}
```

**Explanation of Settings:**

* **`subnet 10.0.2.0`**: Defines the network ID.
* **Network Selection Advice:** The text advises **avoiding** `192.168.0.0/24` or `192.168.1.0/24` for corporate networks. Since most home networks use these IPs, remote users connecting via VPN might face routing conflicts (two identical networks).
* **`option routers`**: This is the **Default Gateway** (`10.0.2.1`) that clients will use to reach the internet.
* **`range 10.0.2.50 10.0.2.100`**: The **Pool** of addresses. The server will hand out IPs starting from `.50` up to `.100`.

---

## 🚀 Step 4: Restart and Verification

Finally, we apply the configuration and verify the service is running.

**1. Restart the Service**

```bash
hashim@hashim-server:~$ sudo systemctl restart isc-dhcp-server.service
```

**2. Check Service Status**

```bash
hashim@hashim-server:~$ sudo systemctl status isc-dhcp-server.service
```

**Output Analysis:**

```text
● isc-dhcp-server.service - ISC DHCP IPv4 server
     Loaded: loaded (/usr/lib/systemd/system/isc-dhcp-server.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-01-26 06:15:30 UTC; 5s ago
       Docs: man:dhcpd(8)
   Main PID: 6890 (dhcpd)
      Tasks: 1 (limit: 9198)
     Memory: 4.8M (peak: 5.2M)
        CPU: 12ms
     CGroup: /system.slice/isc-dhcp-server.service
             └─6890 dhcpd -user dhcpd -group dhcpd -f -4 -pf /run/dhcp-server/dhcpd.pid -cf /etc/dhcp/dhcpd.conf
```

* **`Loaded: loaded`**: The service configuration file exists and is recognized by the system.
* **`Active: active (running)`**: **Success!** The server is up and running correctly. The timestamp (`since Mon...`) shows it started 5 seconds ago.
* **`Main PID: 6890`**: The Process ID. This is the specific number the operating system uses to identify the running DHCP program.
* **`CGroup`**: Shows the exact command used to launch the daemon (`/usr/sbin/dhcpd`), pointing to the config file we just edited (`-cf /etc/dhcp/dhcpd.conf`).

---

## ➕ Optional: Dynamic DNS Integration

If you want clients to automatically update their DNS records when they get an IP, you can add these lines to the configuration:

```nginx
ddns-update-style interim;
# If you have fixed-address entries you want to use dynamic dns
update-static-leases on;
```

* **`ddns-update-style interim`**: Enables the interaction between DHCP and DNS.
* **`update-static-leases on`**: Ensures that even devices with fixed (static) IPs get their DNS names updated automatically.


---