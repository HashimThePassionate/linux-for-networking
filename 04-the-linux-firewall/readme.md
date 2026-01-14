# 🔥 The Linux Firewall
Linux has almost always provided an integrated firewall for system administrators. While native tools allow for building traditional perimeter firewalls with **Address Translation (NAT)** or **Proxy Servers**, modern data centers typically use host firewalls differently.

This guide covers the modern use cases, technical requirements, and the core commands used to secure a Linux host.

---

## 🎯 Typical Use Cases in Modern Infrastructure

In a modern data center, host firewalls are primarily used for three specific purposes:

* **🛡️ Inbound Access Controls (Admin):** Limiting access to administrative interfaces (like SSH) to ensure only authorized personnel can connect.
* **🌐 Inbound Access Controls (Services):** Restricting access to specific installed services (like Web Servers or Databases) to ensure they are only accessible as intended.
* **📝 Incident Response Logging:** Logging access attempts. This is critical for post-incident analysis if a security breach or exposure occurs.

> **⚠️ A Note on Egress Filtering (Outbound Control)**
> While **Egress Filtering** (controlling traffic leaving the server) is highly recommended, it is rarely implemented directly on the host in modern setups. Instead, it is usually enforced at the **Network Perimeter**—on firewalls and routers located between VLANs or facing less-trusted networks (like the Public Internet).

---

## 🏗️ Project Scope & Objective

In this specific configuration guide, the focus is on implementing a set of rules for a realistic server scenario:

1. **Web Service:** Allowing general access for public users.
2. **SSH Service:** Allowing strict administrative access for managing the server.

The goal is to master the two primary topics:

* Configuring **iptables** (The legacy standard).
* Configuring **nftables** (The modern replacement).

---

## 💻 Technical Requirements

To follow along with these firewall configurations, you will need:

* **Primary Host:** An existing **Ubuntu** host or Virtual Machine (VM).
* **Secondary Host (Optional but Recommended):** A second machine to act as a "client" to test your firewall rules (e.g., trying to ping or SSH into the primary host).

---

## 🛠️ The Core Firewall Commands

We will focus on the two main Command Line Interface (CLI) tools used to manage Linux firewalls.

| Command | Description |
| --- | --- |
| `iptables` | The main command used to manipulate the legacy **iptables** firewall. |
| `nft` | The main CLI command used to manipulate the newer **nftables** firewall. |

---

### 🧐 Detailed Explanation of the Commands

#### 1. `iptables`

This is the traditional tool used for years in Linux. It works by managing tables of packet filter rules.

* **Usage:** It creates "chains" of rules that tell the kernel what to do with a network packet (Accept, Drop, or Reject).
* **Status:** While still widely used, it is being slowly replaced by `nftables`.

#### 2. `nft`

This is the command for **nftables**, which is the modern successor to iptables.

* **Usage:** It offers a simpler syntax, better performance, and combines the capabilities of IPv4 and IPv6 filtering into a single tool.
* **Status:** It is the future standard for Linux packet filtering.

---

# 🛡️ Configuring `iptables`: The Linux Host Firewall

## 📘 Overview: The State of Linux Firewalls

At the time of writing (2026), firewall architectures in Linux are in a state of flux.

* **`iptables`**: This is still the default host firewall on many distributions, including Ubuntu. It replaced the older `ipchains` (from 1999) around 2014.
* **`nftables` (Netfilter)**: This is the newer architecture. Industry giants like Red Hat and CentOS v8 have already made this their default. It offers better IPv6 support, a consistent command set, and better API support.

### 🕰️ Why Learn `iptables`?

Even though `nftables` is newer, `iptables` has "decades of inertia."

1. **Legacy Systems:** Linux devices often last for decades. Think about cash registers, medical devices, elevator controls, or factory equipment (PLCs). You might encounter systems running OS versions from 5, 10, or 15 years ago.
2. **Automation:** Many existing automation tools are built entirely on `iptables`.

While migration will happen, there will be a "long tail" of legacy hosts running `iptables` for years. Therefore, mastering it is essential.

---

## 🏗️ `iptables` High-Level Concepts

`iptables` is a command-line firewall utility. It organizes its configuration into **Tables**, which contain sets of rules called **Chains**.

### 🎯 Targets (Actions)

When a network packet matches a rule, the firewall assigns it a **Target**.

* **ACCEPT**: The packet is allowed through.
* **DROP**: The packet is destroyed (not passed). The sender receives no notification.
* **RETURN**: Stops processing the current chain and goes back to the previous one.

### 📊 The `filter` Table

This is the default table used for host firewalling. It contains three built-in chains:

1. **INPUT**: Controls packets coming **INTO** the host.
2. **FORWARD**: Controls packets passing **THROUGH** the host (routing).
3. **OUTPUT**: Controls packets leaving **FROM** the host.

> **Note:** There are other tables like `NAT` and `Mangle`, but `filter` is the primary focus for basic security.

---

## 🚦 Basic Configuration & Verification

By default, `iptables` is usually not configured, meaning it allows all traffic.

### 💻 Viewing the Current Status

To list the current rules, we use the `-L` (List) and `-v` (Verbose) flags.

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -L -v
```

**Output:**

```text
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
```

**Observation:**

* All chains (INPUT, FORWARD, OUTPUT) are empty.
* The default **policy** is `ACCEPT`.
* Even though it is empty, you might see packet counts increasing on INPUT/OUTPUT chains, showing the service is active.

---

## 🛠️ Adding Rules: The Syntax

To add a rule, we typically use the **`-A`** (Append) parameter. Here are the common components of a rule:

| Parameter | Name | Description |
| --- | --- | --- |
| **`-I`** | **Interface** | Specifies which network card the rule applies to (e.g., `eth0` or `enp0s3`). "Yeh batata hai ke rule kis network card par lagana hai." |
| **`-p`** | **Protocol** | Defines the protocol (TCP, UDP, ICMP, or "all"). |
| **`-s`** | **Source** | The Source IP address or hostname (Where the traffic is coming from). |
| **`--dport`** | **Destination Port** | The target port (e.g., 22 for SSH, 443 for HTTPS). |
| **`-j`** | **Target (Jump)** | The action to take (ACCEPT, DROP, RETURN). |

### 💻 Practical Example: Allowing SSH and HTTPS

Let's add two rules:

1. Allow hosts from the `10.0.2.0/24` network to access SSH (Port 22).
2. Allow **anyone** to access HTTPS (Port 443).

**Commands:**

```bash
hashim@Hashim:~$ sudo iptables -A INPUT -i enp0s3 -p tcp -s 10.0.2.0/24 --dport 22 -j ACCEPT
hashim@Hashim:~$ sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

**Analysis:**
These rules only work if you actually have services (like an SSH server or Web Server) running on those ports. If nothing is listening, the rules do nothing useful.

---

## 📋 Verifying Rules with Numbers

To see what we just added, we list the rules again. We add `--line-numbers` to make management easier and `-n` to show numeric IPs instead of trying to resolve hostnames (which is faster).

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -L -n -v --line-numbers
```

**Output:**

```text
Chain INPUT (policy ACCEPT 55 packets, 4373 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1        0     0 ACCEPT     tcp  --  enp0s3 * 10.0.2.0/24          0.0.0.0/0             tcp dpt:22
2        0     0 ACCEPT     tcp  --  * * 0.0.0.0/0            0.0.0.0/0             tcp dpt:443
...

```

*(Note: Forward and Output chains remain empty).*

---

## 🛑 Specific Blocking & Rule Order

Rules are processed **sequentially from top to bottom**. The first rule that matches a packet "wins." This means order is critical.

### 💻 Inserting a Specific Drop Rule

Suppose we want to block a specific bad host (`10.0.2.5`) from accessing our HTTPS server, but allow everyone else. We must insert this block **before** the "Allow All" rule.

We use **`-I`** (Insert) to place the rule at position 2.

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -I INPUT 2 -i enp0s3 -p tcp -s 10.0.2.5 --dport 443 -j DROP
```

**Verification:**

```bash
hashim@Hashim:~$ sudo iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
ACCEPT     tcp  --  10.0.2.0/24          anywhere             tcp dpt:ssh
DROP       tcp  --  10.0.2.5             anywhere             tcp dpt:https
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:https
```

### 🧠 Logic Check

1. **Rule 1:** Allow SSH from subnet.
2. **Rule 2:** DROP HTTPS from `10.0.2.5`.
3. **Rule 3:** ACCEPT HTTPS from anywhere.

If `10.0.2.5` tries to connect, it hits Rule 2 and is dropped. It never reaches Rule 3.

---

## 🔐 Securing Admin Access (SSH)

Currently, we allow the local subnet to SSH, but we haven't explicitly blocked others. Let's add a rule to **DROP** SSH traffic from anyone else. We insert this at position 2 (after the allow rule).

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -I INPUT 2 -i enp0s3 -p tcp --dport 22 -j DROP
```

**Grouping Rules:**
It is good practice to group protocol rules together logically.

1. SSH Allow (Subnet)
2. SSH Drop (Everyone Else)
3. HTTPS Drop (Bad Host)
4. HTTPS Allow (Everyone Else)

**Verification:**

```bash
hashim@Hashim:~$ sudo iptables -L -n -v --line-numbers
Chain INPUT (policy ACCEPT 119 packets, 9643 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1        0     0 ACCEPT     tcp  --  enp0s3 * 10.0.2.0/24          0.0.0.0/0             tcp dpt:22
2        0     0 DROP       tcp  --  enp0s3 * 0.0.0.0/0            0.0.0.0/0             tcp dpt:22
3        0     0 DROP       tcp  --  enp0s3 * 10.0.2.5             0.0.0.0/0             tcp dpt:443
4        0     0 ACCEPT     tcp  --  * * 0.0.0.0/0            0.0.0.0/0             tcp dpt:443
```

> **Performance Tip:** Put the rules that get "hit" most frequently at the top. For a public web server, you might want the HTTPS allow rule at Rule #1 for speed.

---

## 🗑️ Deleting Rules

To remove a rule, use the **`-D`** (Delete) flag followed by the chain name and rule number.

**Example:** Deleting Rule 5 (hypothetically).

```bash
hashim@Hashim:~$ sudo iptables -D INPUT 5
```

---

## 📝 Logging & Commenting

### 1. Enable Logging

Firewalls should document activity. We use `-j LOG` to generate system logs for matched packets.

* **Log Scan Attempts:** Track people scanning your admin ports.
* **Log Blocks:** See who is trying to access blocked services.
* **Correlation:** Match firewall logs with web server logs for troubleshooting.

**Command (Log specific subnet):**

```bash
hashim@Hashim:~$ sudo iptables -A INPUT -s 10.0.2.0/24 -j LOG --log-level 3 --log-prefix '*SUSPECT Traffic Rule 9*'
```

* **Log Location:** `/var/log/kern.log` (Ubuntu) or `/var/log/messages` (Red Hat/Fedora).

### 2. Adding Comments

Self-documenting rules are easier to manage. Use `-m comment`.

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT -m comment --comment "Permit all Web Access"
```

**Output Verification:**

```text
6        0     0 ACCEPT     tcp  --  * * 0.0.0.0/0            0.0.0.0/0             tcp dpt:443 /* Permit all Web Access */

```

---

## 🔒 The Default Policy: ACCEPT vs. DROP

The **Default Policy** is the final rule. If a packet falls through all your rules without matching, the Default Policy decides its fate.

* **Default:** `ACCEPT` (Permit everything unless explicitly denied).
* **Secure:** `DROP` (Deny everything unless explicitly permitted).

### ⚠️ Critical Warning

**Do not saw off the branch you are sitting on!**
If you are connected via SSH and you change the policy to `DROP` before you have added a rule to allow your own SSH connection, you will lock yourself out immediately.

**Changing Policy to DROP:**

```bash
hashim@Hashim:~$ sudo iptables -P INPUT DROP
```

**Verification:**

```bash
hashim@Hashim:~$ sudo iptables -L -n -v --line-numbers
Chain INPUT (policy DROP 0 packets, 0 bytes)
```

---

## 💾 Saving Rules (Persistence)

`iptables` rules run in memory (RAM). If you reboot, they are lost. We must save them.

### 1. Install Persistent Package

On Debian/Ubuntu:

```bash
hashim@Hashim:~$ sudo apt install iptables-persistent
```

### 2. Save Command

**Incorrect Method (Permission Error):**

```bash
hashim@Hashim:~$ sudo iptables-save > /etc/iptables/rules.v4
bash: /etc/iptables/rules.v4: Permission denied
```

*Reason:* The redirection `>` runs as your user, not root.

**Correct Method:**

```bash
hashim@Hashim:~$ sudo netfilter-persistent save
```

*Output:*

```text
run-parts: executing /usr/share/netfilter-persistent/plugins.d/15-ip4tables save
run-parts: executing /usr/share/netfilter-persistent/plugins.d/25-ip6tables save

```

---

## 🛠️ Troubleshooting: Fixing DNS & Ping

After setting the policy to `DROP`, you might notice Ping and DNS stop working.

**Why?**

1. **State:** The server sends a request (e.g., DNS query), but the firewall blocks the *reply* because it doesn't know it belongs to an established conversation.
2. **Loopback:** The system blocks traffic to `127.0.0.1` (itself).

**Testing the Failure:**

```bash
hashim@Hashim:~$ ping -c 4 google.com
ping: google.com: Temporary failure in name resolution
```

### The Fixes

1. **Allow Established Connections:**
```bash
hashim@Hashim:~$ sudo iptables -I INPUT 1 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```


2. **Allow Loopback:**
```bash
hashim@Hashim:~$ sudo iptables -I INPUT 1 -i lo -j ACCEPT
```



**Retesting:**

```bash
hashim@Hashim:~$ ping -c 4 google.com
PING google.com (142.250.202.174) 56(84) bytes of data.
64 bytes from ... icmp_seq=1 ttl=255 time=75.6 ms
```

Success!

---

## 🗑️ Resetting & Clearing Firewall Rules

If you need to start fresh or disable the firewall for testing, follow this specific order to avoid lockouts.

### 1️⃣ Set Policies to ACCEPT

Ensure the default behavior allows traffic before deleting specific rules.

```bash
hashim@Hashim:~$ sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
```

### 2️⃣ Flush and Delete Chains

Remove all rules from memory.

* **`-F` (Flush)**: Deletes all rules.
* **`-X`**: Deletes custom chains.

```bash
hashim@Hashim:~$ sudo iptables -F
sudo iptables -X
```

### 3️⃣ Verify Empty State

```bash
hashim@Hashim:~$ sudo iptables -L -n -v
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
...
```

### 4️⃣ Save the Empty State (Permanent Reset)

The file `/etc/iptables/rules.v4` still has the old rules. We must overwrite it with the current empty state.

**Check old file:**

```bash
hashim@Hashim:~$ sudo cat /etc/iptables/rules.v4
# Generated by iptables-save ... :INPUT DROP [244:18796] ...
```

**Overwrite file:**

```bash
hashim@Hashim:~$ sudo netfilter-persistent save
```

*Or manually:*

```bash
hashim@Hashim:~$ sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

**Final Verification:**

```bash
hashim@Hashim:~$ sudo cat /etc/iptables/rules.v4
# Generated by iptables-save ...
*filter
:INPUT ACCEPT [0:0]
...
COMMIT

```

The firewall is now completely reset.

---

# 🌐 The NAT Table (Network Address Translation)

## 📘 Overview

**Network Address Translation (NAT)** is a technique used to modify the source or destination IP addresses of network packets as they pass through a router or firewall.

In simple terms: NAT translates traffic coming from (or going to) one IP address/subnet and makes it appear as if it is coming from another.

### 🏢 Common Use Case: Internet Gateways

This is most commonly seen in internet gateways or firewalls.

* **Inside Interface:** Connects to your local network using private addresses (RFC1918 ranges like `10.x.x.x` or `192.168.x.x`).
* **Outside Interface:** Connects to the public internet using a single routable IP address.

### 🔄 How Mapping Works (The Tuple)

When multiple internal devices access the internet, they are often "mapped" to the single public IP of the gateway. This is called **Overload NAT** (or PAT - Port Address Translation).

The gateway modifies the packet's **Tuple**:

* **Original Tuple:** `Source IP (Private), Source Port, Dest IP, Dest Port, Protocol`
* **New Tuple:** `Source IP (Public Gateway), Source Port (Next Available), Dest IP, Dest Port, Protocol`

The firewall keeps this translation record in a **NAT Table** in memory.

* **Return Traffic:** When the internet replies, the firewall looks up the table, reverses the translation, and sends the data back to the correct internal device.
* **Cleanup:**
* **TCP:** Entries are removed when the session ends (teardown).
* **UDP:** Entries expire after a period of inactivity.



---

## 🛠️ Configuring NAT: The `nat` Table

In `iptables`, NAT rules are stored in a specific table called `nat`. Let's explore how to configure this on a Linux gateway.

### 1️⃣ Step 1: Viewing the Default NAT Table

By default, the table is empty. We use the `-t nat` flag to specify we want to look at the NAT table (not the default filter table).

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -t nat -L -v
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

```

**Analysis:**

* **PREROUTING:** Handles packets *before* they are routed (DNAT).
* **POSTROUTING:** Handles packets *after* they are routed (SNAT/Masquerade).
* Currently, all chains are empty.

### 2️⃣ Step 2: Adding the Masquerade Rule

We want to allow our internal network to access the internet. To do this, we tell the firewall to **Masquerade** (hide) all internal traffic behind the IP address of the external interface (`enp0s3`).

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE

```

**Command Explanation:**

* **`-t nat`**: Use the NAT table.
* **`-A POSTROUTING`**: Append this rule to the **POSTROUTING** chain. We do this *after* the routing decision is made because we want to modify the packet right before it leaves the box.
* **`-o enp0s3`**: Applies only to traffic leaving **Out** of the interface `enp0s3`.
* **`-j MASQUERADE`**: The action. Automatically use the current IP address of the interface for translation.

### 3️⃣ Step 3: Verifying the Rule

Let's check the table again to confirm the rule exists.

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -t nat -L -n -v
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 MASQUERADE  all  --  * enp0s3  0.0.0.0/0            0.0.0.0/0

```

**Observation:** You can see the `MASQUERADE` target listed under `POSTROUTING`.

---

## 🧪 Testing the Configuration

To prove this works, we will verify our IP addresses and generate traffic.

### 1. Check Internal vs. External IP

First, we look at our local (private) IP, then we ask the internet what IP it sees.

**Command:**

```bash
hashim@Hashim:~$ ip -4 a show enp0s3 | grep inet
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3

```

* **Internal IP:** `10.0.2.15`

**Command:**

```bash
hashim@Hashim:~$ curl ifconfig.me
154.81.228.31

```

* **External IP:** `154.81.228.31`
* **Result:** Success! The internet sees us as the public IP, not our private `10.0.2.15` address.

### 2. Generate Traffic (Ping)

Now, we send some traffic through the firewall to trigger the counters.

**Command:**

```bash
hashim@Hashim:~$ ping -c 4 google.com
PING google.com (142.250.184.110) 56(84) bytes of data.
64 bytes from lcmcta-am-in-f14.1e100.net (142.250.184.110): icmp_seq=1 ttl=255 time=87.1 ms
64 bytes from lcmcta-am-in-f14.1e100.net (142.250.184.110): icmp_seq=2 ttl=255 time=75.9 ms
64 bytes from lcmcta-am-in-f14.1e100.net (142.250.184.110): icmp_seq=3 ttl=255 time=75.6 ms
64 bytes from lcmcta-am-in-f14.1e100.net (142.250.184.110): icmp_seq=4 ttl=255 time=84.3 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3009ms
rtt min/avg/max/mdev = 75.555/80.745/87.137/5.094 ms

```

### 3. Verify Packet Processing

Finally, we check the NAT table again to see if the counters increased. This proves the rule actually touched the packets.

**Command:**

```bash
hashim@Hashim:~$ sudo iptables -t nat -L POSTROUTING -v -n
Chain POSTROUTING (policy ACCEPT 3 packets, 220 bytes)
 pkts bytes target     prot opt in     out     source               destination
   22  1633 MASQUERADE  all  --  * enp0s3  0.0.0.0/0            0.0.0.0/0

```

**Observation:**

* **pkts:** `22`
* **bytes:** `1633`
* The counters are non-zero, confirming the NAT is active and working.

---

## 🔒 A Note on Routing Order & Encryption

The distinction between `PREROUTING` and `POSTROUTING` becomes critical when you introduce encryption (like VPNs).

* **Pre-Routing:** Happens before the routing decision.
* **Post-Routing:** Happens after the routing decision.

If you encrypt traffic *before* a NAT operation, the NAT sees encrypted garbage and cannot translate specific ports. If you encrypt *after*, the NAT works as expected. Defining the order ensures there is no confusion in complex setups.


---

# 🛠️ The Mangle Table & Order of Operations

## 📘 Overview

In the Linux firewalling world (`iptables`), most administrators spend their time in the `filter` table (blocking/allowing) or the `nat` table (routing). However, there is a third, powerful table called **`mangle`**.

The `mangle` table is used to **manually adjust specific values** inside an IP packet header as it passes through the Linux host. It is specialized and used less frequently, but for specific problems—like fixing packet size issues on complex networks—it is a lifesaver.

---

## 📉 The Problem: MTU and Packet Fragmentation

Standard Ethernet networks use a **Maximum Transmission Unit (MTU)** of **1500 bytes**. This is the largest packet size allowed.

However, some network links cannot handle 1500 bytes:

1. **DSL (Digital Subscriber Line):** Adds encapsulation headers (PPPoE), which eat up space.
2. **Satellite Links:** Often use smaller packets to reduce the impact of transmission errors.
3. **VPNs/Tunnels:** Encapsulation (IPSec, GRE) adds overhead, reducing the payload size.

### 🚫 When "Path MTU Discovery" Fails

Ideally, computers use **PMTUD (Path MTU Discovery)** to automatically figure out the max packet size.

* **How it works:** Hosts send packets with the "Don't Fragment" (DF) bit set. If a router can't pass it, it sends back an ICMP error ("Packet too big").
* **The Failure:** Many networks **block ICMP** for security. This breaks PMTUD.
* **The Result:** Users experience "Black Hole" connections—the handshake works (small packets), but as soon as data starts flowing (large packets), the connection hangs and dies.

---

## 🔧 The Solution: TCP MSS Clamping

We can use the `mangle` table to "hack" the negotiation process. We intercept the **SYN** packet (the start of the TCP handshake) and forcibly lower the **MSS (Maximum Segment Size)** value.

### 💻 The Command

This command tells the firewall: *"When you see a TCP SYN packet going through the Forward chain, change its MSS value to 1412."*

```bash
iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --set-mss 1412

```

**Breakdown:**

* **`-t mangle`**: Use the mangle table.
* **`-A FORWARD`**: Append to the Forward chain (traffic passing through the box).
* **`--tcp-flags SYN,RST SYN`**: Match only packets where the SYN flag is set (new connections).
* **`-j TCPMSS`**: Jump to the TCPMSS target extension.
* **`--set-mss 1412`**: Rewrite the value to 1412 bytes.

---

## 🔍 Finding the "Magic Number" (Packet Size)

How do you know to set it to 1412? You have to hunt for it using tools.

### 1️⃣ Method 1: Using `ping`

If ICMP is allowed, use ping to test the "Don't Fragment" limit.

**Command:**

```bash
ping –M do –s 1400 8.8.8.8

```

* **`-M do`**: Set the "Don't Fragment" bit.
* **`-s 1400`**: Send a payload of 1400 bytes.
* **8.8.8.8**: The target (Google DNS).

> **Calculation Note:** The total size is `Payload` + `IP Header (20 bytes)` + `ICMP Header (8 bytes)` = Payload + 28 bytes. So `-s 1400` creates a 1428-byte packet. You adjust the number until pings stop dropping.

### 2️⃣ Method 2: Using `nping`

If ICMP is blocked, use `nping` (part of the Nmap suite) to test TCP packet sizes.

**Command:**

```bash
$ sudo nping --tcp -p 53 -df --mtu 1400 -c 1 8.8.8.8

```

**Output Analysis:**

```text
Starting Nping 0.7.80 ( https://nmap.org/nping ) at 2021-04-22
...
SENT (0.0336s) TCP 192.168.122.113:62878 > 8.8.8.8:53 S ...
RCVD (0.0451s) TCP 8.8.8.8:53 > 192.168.122.113:62878 SA ...

```

* **`-df`**: Don't Fragment.
* **`--mtu 1400`**: Set MTU to 1400.
* **`RCVD`**: If you see a "RCVD" line, the packet made it through! Keep increasing the size until it fails to find the limit.

---

## 🚦 Order of Operations in `iptables`

Configuring complex firewalls requires understanding the **Packet Flow**. Rules are processed in a specific order across tables.

### ⚠️ Why Order Matters

1. **Encryption (IPSec):** You typically want to encrypt traffic *before* NAT happens.
2. **Policy Based Routing:** If you route backup traffic differently than web traffic, you must mark packets *before* the routing decision is made.
3. **NAT vs. Filter:** You generally filter (block) traffic first to save CPU, but sometimes you need to NAT first to know the real destination.

### 🔄 The Standard Flow

While complex, the general path for a packet traversing the system is:

1. **Mangle (PREROUTING):** Modify packet headers (TOS/DSCP).
2. **NAT (PREROUTING):** Change Destination IP (DNAT/Port Forwarding).
3. **Routing Decision:** Is this for me or for someone else?
4. **Filter (FORWARD):** Should I allow this packet to pass?
5. **Mangle (POSTROUTING):** Final adjustments.
6. **NAT (POSTROUTING):** Change Source IP (Masquerade/SNAT).

---

## 🚀 Advanced Usage & Next Steps

The `mangle` table is also used for **QoS (Quality of Service)**. You can set **DSCP (Differentiated Services Code Point)** bits to tell upstream routers, "This packet is Voice data, prioritize it!" or "This is bulk backup data, send it whenever."

### 📚 Where to Go Next?

* **Man Pages:** The `man iptables` documentation is roughly 100 pages of deep technical detail.
* **Distributions:** While you can build a router using raw Linux and `iptables`, in production data centers, most people use specialized distributions that handle this complexity for you:
* **VyOS:** A dedicated router OS.
* **pfSense / OPNsense:** Firewall appliances (BSD-based).
* **FRR / Zebra:** Routing packages for Linux.

---

# 🛡️ Configuring nftables: The Modern Linux Firewall

## 📘 Overview

As discussed, `iptables` is being deprecated in Linux and replaced by **nftables**. While `iptables` served us well for decades, `nftables` offers significant architectural improvements required for modern infrastructure.

### 🚀 Why Switch to nftables?

There are four major reasons to adopt the new standard:

1. **Speed:** Deploying rules is significantly faster. Unlike `iptables`, which modifies the kernel sequentially for each rule added, `nftables` updates rules atomically.
2. **API & Automation:** `nftables` includes a native API. This supports "Network as Code" tools like **Terraform**, **Ansible**, **Puppet**, or **Chef**, allowing administrators to automate deployments in minutes instead of hours.
3. **Efficiency:** It runs more efficiently within the Linux kernel, consuming less CPU. This is critical when scaling to hundreds of virtual machines or thousands of rules.
4. **Single Command:** A single command tool (`nft`) handles **both** IPv4 and IPv6 protocols. You no longer need separate commands like `iptables` and `ip6tables`.

---

## 🧱 Basic Configuration

Before starting, it is recommended to read the manual using `man nft`.

We will deploy the same **Input Firewall** configuration used in the previous section. This setup restricts access to the host, a common pattern in data centers.

### ⚠️ Important Pre-check

* **Document Existing Rules:** Always back up your current configuration.
* **Clear Old Rules:** Running `iptables` and `nftables` simultaneously is risky and confusing for future administrators. Ensure you clear the old system before starting the new one.

### 🔄 The Translation Tool: `iptables-translate`

If you already know `iptables` syntax, you don't need to relearn everything from scratch. Linux provides a tool to translate old commands into the new format.

**Command:**

```bash
hashim@Hashim:~$ sudo iptables-translate -A INPUT -i enp0s3 -p tcp -s 10.0.2.0/24 --dport 22 -j ACCEPT -m comment --comment "Permit Admin"
```

**Output:**

```bash
nft 'add rule ip filter INPUT iifname "enp0s3" ip saddr 10.0.2.0/24 tcp dport 22 counter accept comment "Permit Admin"'
```

**Explanation:**
The tool generated the exact `nft` string required to replicate the old rule. We can use this syntax to build our new ruleset.

---

### 🛠️ Building the Ruleset Step-by-Step

In `nftables`, tables and chains are **not** created by default. We must define the structure manually.

#### 1. Create the Table

We create a table named `filter` for the `ip` (IPv4) family.

```bash
hashim@Hashim:~$ sudo nft add table ip filter
```

#### 2. Create the Chain

We create a chain named `INPUT` inside the `filter` table. We must define its type, hook, and priority.

```bash
hashim@Hashim:~$ sudo nft add chain ip filter INPUT { type filter hook input priority 0 \; }
```

* **hook input:** This chain attaches to incoming traffic.
* **priority 0:** Determines order (similar to rule numbers).

#### 3. Add the Rules

Now we add the specific Allow/Block rules.

* **Rule 1: Permit Admin SSH** (Allow `10.0.2.0/24` on Port 22)
```bash
hashim@Hashim:~$ sudo nft add rule ip filter INPUT iifname "enp0s3" ip saddr 10.0.2.0/24 tcp dport 22 counter accept comment \"Permit Admin\"
```


* **Rule 2: Block Other SSH** (Block Port 22 for everyone else)
```bash
hashim@Hashim:~$ sudo nft add rule ip filter INPUT iifname "enp0s3" tcp dport 22 counter drop comment \"Block Admin\"
```


* **Rule 3: Block Specific Web Host** (Block `10.0.2.5` from Port 443)
```bash
hashim@Hashim:~$ sudo nft add rule ip filter INPUT iifname "enp0s3" ip saddr 10.0.2.5 tcp dport 443 counter drop comment \"Block inbound Web\"
```


* **Rule 4: Permit All Other Web** (Allow Port 443 for everyone else)
```bash
hashim@Hashim:~$ sudo nft add rule ip filter INPUT tcp dport 443 counter accept comment \"Permit all Web Access\"
```



---

## 📋 Verifying the Configuration

To view the structure we just created, we use the `list ruleset` command.

**Command:**

```bash
hashim@Hashim:~$ sudo nft list ruleset
```

**Output:**

```text
table ip filter {
	chain INPUT {
		type filter hook input priority filter; policy accept;
		iifname "enp0s3" ip saddr 10.0.2.0/24 tcp dport 22 counter packets 0 bytes 0 accept comment "Permit Admin"
		iifname "enp0s3" tcp dport 22 counter packets 0 bytes 0 drop comment "Block Admin"
		iifname "enp0s3" ip saddr 10.0.2.5 tcp dport 443 counter packets 0 bytes 0 drop comment "Block inbound Web"
		tcp dport 443 counter packets 0 bytes 0 accept comment "Permit all Web Access"
	}

	chain FORWARD {
		type filter hook forward priority filter; policy accept;
	}

	chain OUTPUT {
		type filter hook output priority filter; policy accept;
	}
}
```

**Observation:**

* The output is structured cleanly (similar to JSON or C code).
* Counters (`packets 0 bytes 0`) are automatically included because we added the `counter` keyword.

> **Note on Persistence:** Like `iptables`, these rules are stored in memory and will vanish on reboot. To make them permanent, save them to the default configuration file, usually located at `/etc/nftables.conf`.

---

## 📂 Advanced: Using Include Files & Maps

Complex server configurations can make the main configuration file messy. `nftables` allows us to organize rules into logical files and "Maps".

### 1. The Include Structure

Instead of one giant file, we can split rules into specific files based on their function.

**File 1: `/etc/nftables/webserver-rules.nft**`

```bash
# Rules specifically for Web Access
add rule ip filter INPUT iifname "enp0s3" ip saddr 10.0.2.5 tcp dport 443 counter drop comment "Block inbound Web"
add rule ip filter INPUT tcp dport 443 counter accept comment "Permit all Web Access"
```

**File 2: `/etc/nftables/admin-rules.nft**`

```bash
# Rules specifically for Admin SSH Access
add rule ip filter INPUT iifname "enp0s3" ip saddr 10.0.2.0/24 tcp dport 22 counter accept comment "Permit Admin"
add rule ip filter INPUT iifname "enp0s3" tcp dport 22 counter drop comment "Block Admin"
```

**Master File: `/etc/nftables.conf**`
We reference the smaller files using the `include` command.

```bash
#!/usr/sbin/nft -f

flush ruleset

table ip filter {
    chain INPUT {
        type filter hook input priority 0; policy accept;
        
        # Admin access restricted to admin VLAN only
        include "/etc/nftables/admin-rules.nft"

        # Webserver ruleset
        include "/etc/nftables/webserver-rules.nft"
    }
}
```

### 2. Using Maps (`vmap`) for Segmentation

Maps allow you to create efficient "Jump" logic. Instead of reading every rule linearly, the firewall can check the IP address and immediately "jump" to a specific chain meant for that network segment.

**Command Example:**

```bash
nft add rule ip Firewall Forward ip daddr vmap { \
 10.0.2.1-10.0.2.50 : jump chain-servers, \
 10.0.2.51-10.0.2.100 : jump chain-desktops \
}
```

**Explanation:**

* Traffic for IPs `.1` to `.50` immediately goes to the `chain-servers` rule list.
* Traffic for IPs `.51` to `.100` immediately goes to the `chain-desktops` rule list.
* This significantly reduces CPU usage on large networks.

---

## 🧹 Removing the Configuration (Clean Up)

Before finishing, we must clean up our test environment. We will flush both the old `iptables` rules (just in case) and our new `nftables` ruleset.

**Command:**

```bash
hashim@Hashim:~$ # Clear iptables first
sudo iptables -F INPUT
sudo iptables -F FORWARD

# Clear nftables next
sudo nft flush ruleset

```

**Verification:**

```bash
hashim@Hashim:~$ sudo nft list ruleset
```

*(The output will be empty, confirming the ruleset is successfully flushed).*

---