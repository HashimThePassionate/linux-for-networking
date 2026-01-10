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