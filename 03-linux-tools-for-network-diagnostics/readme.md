# 🛠️ Using Linux & Linux Tools for Network Diagnostics

Welcome to the new section! In this section, we will dive deep into the "how-it-works" of networking mechanics and explore how to turn your Linux workstation into a powerful network troubleshooting hub.

By the end of this module, you will have the skills to troubleshoot local and remote network services and effectively "inventory" your network environment.

---

## 🎯 What We Will Cover

We will break down network diagnostics into the following key areas:

* **🌐 Networking Basics:** Understanding the **OSI Model** foundation.
* **🔗 Layer 2 Operations:** Relating IP addresses to Physical (MAC) addresses using **ARP**, with a deep dive into how MAC addresses function.
* **📦 Layer 4 Protocols:** How **TCP** and **UDP** ports work, including the famous **TCP "Three-Way Handshake"** and how to spot it using Linux commands.
* **🔍 Local Enumeration:** Identifying listening TCP/UDP ports on your own machine and linking them to running services.
* **📡 Remote Enumeration:** Scanning remote hosts using both native system tools and advanced scanners like **Netcat** and **Nmap**.
* **📶 Wireless Troubleshooting:** The basics of Wi-Fi operations and diagnostics.

---

## ⚙️ Technical Requirements

To follow along with the examples, you will need:

* 🐧 **System:** Your existing **Ubuntu Host** or **Virtual Machine (VM)**.
* 📡 **Hardware (Optional):** A Wi-Fi adapter is recommended if you wish to practice the wireless troubleshooting examples (as standard VMs often treat network connections as wired Ethernet).

---

## 🧰 Your Network Diagnostic Toolkit

We will be utilizing a robust set of tools, ranging from native commands built into Linux to specialized installed applications.

### 🖥️ Native & Standard Linux Tools

| Tool | Description |
| --- | --- |
| **`arp`** | Works with the **Address Resolution Protocol**. Relates physical MAC addresses to IP addresses. |
| **`netplan`** | A YAML-based tool for configuring network settings on modern Ubuntu systems. |
| **`ip` & `ifconfig`** | Configure and display parameters for local network interfaces. |
| **`netstat` & `ss`** | View listening TCP/UDP ports and active conversation states. |
| **`telnet`** | A basic text-based tool used here for simple connectivity troubleshooting. |
| **`nc` (Netcat)** | The "Swiss Army Knife" of networking. Used to connect to, listen on, and "poke around" remote services. |

### 🔎 Advanced Scanning & Wireless Tools

| Tool | Description |
| --- | --- |
| **`Nmap`** | The industry standard for network discovery and security auditing. Enumerates ports and runs scripts against them. |
| **`Kismet`** | View details of local wireless networks *without* connecting to them (passive sniffing). |
| **`Wavemon`** | Displays signal strength and performance metrics for the Wi-Fi network you are currently connected to. |
| **`LinSSID`** | A graphical step-up from Kismet. visualizes signal strength and channel utilization in the local vicinity. |

---

# 🌐 Network Basics: The OSI Model

## 📘 Overview

To understand how networks and applications work, we use a conceptual framework called the **OSI Model** (Open Systems Interconnection model). This model breaks down the complex process of networking into **7 distinct layers**.

Think of it like a building:

* **Top Layers:** Handle "abstract" things like software, user interfaces, and applications.
* **Bottom Layers:** Handle "nuts and bolts" primitives like cables, electricity, and physical switches.

By using this model, we can isolate problems and understand exactly which part of the system is responsible for what task.

---

## 📊 The 7 Layers of the OSI Model

Below is a detailed breakdown of the OSI model. This data is extracted directly from the diagrams to give you a complete picture of how each layer functions and what protocols live there.

### 🏗️ Detailed Layer Breakdown (Extracted from Diagram)

| Layer Name | Layer No. | Description / Constructs | Examples |
| --- | --- | --- | --- |
| **Application** | 7 | The application the end user interacts with directly. | SMTP, HTTP, HTTPS, FTP, SSH, DNS |
| **Presentation** | 6 | Formats data for the application; handles encryption and decryption (making data readable). | ASCII, Unicode, SSL, TLS, HTTPS, IPSEC, DTLS |
| **Session** | 5 | Establishes, maintains, and ends connections (sessions) between hosts. | APIs, Netbios, Tunneling (GRE, MPLS, PPTP) |
| **Transport** | 4 | Manages End-to-End connections, transport protocols, and error handling. | TCP, UDP |
| **Network** | 3 | Handles Path Determination, Routing, IP Addresses, and Packets. | Routers, Layer 3 Switches, ICMP, Routing Protocols |
| **Data Link** | 2 | Manages communications on the local network (LAN), MAC Addresses, and Frames. | Switches, Wireless Access Points |
| **Physical** | 1 | Handles data encoding on the physical media (bits on the wire or wireless waves). | Cables, Network Cards (NICs), Wi-Fi, Media Converters |

---

## 🗣️ Common Usage in Troubleshooting

Network professionals often refer to these layers by their **number**, counting from the bottom (Physical) up to the top (Application).

* **Layer 2 Issue:** Usually involves **Switches** and **MAC addresses**.
* *Scope:* Confined to the local network (VLAN/Subnet).


* **Layer 3 Issue:** Usually involves **Routers**, **IP addresses**, and **Packets**.
* *Scope:* Involves connecting to distant networks or the internet.



### 🤔 The "Fuzzy" Areas

No model is perfect. In the real world, some technologies blur the lines between layers:

* **IPSEC:** It provides encryption (Layer 6 behavior) but is often considered a tunneling protocol (Layer 5 behavior).
* **TCP:** It lives in Layer 4 (Transport) because of "Ports," but it also manages "Sessions," which sounds like Layer 5.

### 😂 The "Layer 8" Joke

There is a common joke in the IT industry about **Layer 8**. Since the model only has 7 layers, Layer 8 refers to the **User** or **Politics**.

* *Example:* "We have a Layer 8 issue" means the problem is caused by a user making a mistake, budget constraints, or management decisions, not the computer itself!

---

## 🔄 Data Travel: Encapsulation & Decapsulation

One of the most important concepts is how data moves through these layers. This process is called **Encapsulation** (going down) and **Decapsulation** (going up).

The following table explains the flow of data as described in the system diagram.

### 📉 The Journey of Data (Down and Up)

| Direction | Layer | What Happens to the Data? |
| --- | --- | --- |
| **START** | **User** | **Person / Keyboard / Video / Mouse** initiates input. |
| ⬇️ **Sending** | **Application** | User interacts with an application (e.g., via HTTP/HTTPS). |
| ⬇️ | **Presentation** | Data is formatted into characters (ASCII/Unicode). |
| ⬇️ | **Session** | Sessions are maintained (often using cookies). |
| ⬇️ | **Transport** | TCP/UDP ports allow multiple sessions to run at once. |
| ⬇️ | **Network** | Frames are **encapsulated into Packets** (usually IP); Routing occurs here. |
| ⬇️ | **Data Link** | Bits are **encapsulated into Frames**. |
| ⬇️ | **Physical** | Data is encoded onto the physical media (electricity/light). |
| **TRANSIT** | **Media** | **Wire or Wireless Media** carries the signal. |
| ⬆️ **Receiving** | **Physical** | Signal is received and decoded back into bits. |
| ⬆️ | **Data Link** | Bits are decapsulated back into Frames. |
| ⬆️ | **...** | The process reverses (Decapsulation) all the way up. |
| **END** | **User** | Data is presented to the user on their screen. |

---

## 📦 Media Layers vs. Host Layers

We can split the OSI model into two major groups:

1. **Media / Network Layers (1-3):**
* *Physical, Data Link, Network.*
* These layers handle the physical delivery of data across wires and routers.


2. **Host / Application Layers (4-7):**
* *Transport, Session, Presentation, Application.*
* These layers run on your computer (the host) and handle the software side.



### 🤝 Why This Matters (Interoperability)

This layered approach allows different vendors to work together.

* A **Cisco switch** (Layer 2) works perfectly with an **Intel network card** (Layer 1/2) because they both follow the same rules.
* **Application Developers** (Layer 7) don't need to know how electricity works (Layer 1) or how routers route (Layer 3). They just treat the network as a "Black Box"—they put data in, and it reliably comes out the other side.

---

# 🛡️ Layer 2: Relating IP and MAC Addresses Using ARP

## 📘 Chapter Overview

While many people stop understanding networks at **Layer 3** (IP Addresses), a true networking professional must master **Layer 2** (Data Link Layer). This layer handles the physical identification of devices using **MAC Addresses** and manages local communication using **ARP** (Address Resolution Protocol).

In this guide, we will explore how your specific Linux system handles these concepts, how to view the "hidden" tables that make networking work, and how to change your machine's identity (MAC spoofing).

---

## 🆔 Understanding MAC Addresses

### 🧠 What is a MAC Address?

A **MAC (Media Access Control)** address is a unique ID assigned to network interfaces. Ideally, it is "burned" into the hardware at the factory, but as you will see, it can be easily changed using software.

* **Size:** 48-bits (12 hexadecimal digits).
* **Format:** Usually written as pairs separated by colons (e.g., `00:0c:29...`) or dots.
* **Function:** It allows devices on the **same local network** (like your home Wi-Fi or a specific VLAN) to talk to each other.

### 🔄 How Communication Works (The ARP Process)

When your computer wants to talk to an IP address (like `10.0.2.2`), it cannot send data directly to an IP. It needs the MAC address.

1. **ARP Request:** Your computer shouts to the whole network: *"Who has IP `10.0.2.2`?"*
2. **ARP Reply:** The device with that IP replies: *"That's me! My MAC address is `52:55:0a:00:02:02`."*
3. **The Cache:** Your computer saves this answer so it doesn't have to ask again.

---

## 📋 The ARP Cache: Viewing Your Local Table

Your system keeps a list of known MAC addresses in the **ARP Table**. Let's look at the actual output from your system.

### 💻 Command: `arp -a`

```bash
hashim@Hashim:~$ arp -a
_gateway (10.0.2.2) at 52:55:0a:00:02:02 [ether] on enp0s3
```

### 🔍 Detailed Explanation of Your Output

* **`_gateway (10.0.2.2)`**: This is the device you are talking to (your Virtual Router).
* **`at 52:55:0a:00:02:02`**: This is the Layer 2 MAC address of that router.
* **`[ether]`**: The connection type is Ethernet.
* **`on enp0s3`**: This is your network interface card.

---

## ⏱️ ARP Timers & The `/proc` Directory

Network entries do not stay forever. If your computer stops talking to a device, it deletes the MAC address from the table to save space.

### 📂 What is `/proc`?

The `/proc` directory is a "Virtual Filesystem." These aren't real files on your hard drive; they are direct windows into the **kernel's memory**. Reading these files lets you see live system settings.

### 💻 Checking ARP Timeout

We can check how long an entry stays "stale" before being cleaned up.

```bash
hashim@Hashim:~$ cat /proc/sys/net/ipv4/neigh/enp0s3/gc_stale_time
60
```

**What this means:**

* **`60`**: Your system waits **60 seconds** before marking an inactive ARP entry as stale.
* **Comparison:** Switches usually wait 5 minutes. Routers can wait up to 4 hours!

> **Pro Tip:** If you replace a router but keep the same IP, your computer might try to talk to the *old* MAC address until this timer expires. Running the `arp` command to clear the table fixes this immediately.

---

## 📊 Viewing Network Statistics

You can also use `/proc` to see raw network performance data, including errors and drops.

### 💻 Command: `cat /proc/net/dev`

```bash
hashim@Hashim:~$ cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo:  162653     1851    0    0    0     0          0        0   162653     1851    0    0    0     0       0          0
enp0s3: 45364612   32641    0    0    0     0          0        0   612552     4890    0    0    0     0       0          0
```

### 🔍 Analysis of Your Stats

* **`enp0s3`**: This is your active interface.
* **`Receive bytes` (45364612)**: Your system has downloaded about 45 MB of data.
* **`Transmit bytes` (612552)**: Your system has uploaded about 600 KB.
* **`errs / drop` (0)**: You have **Zero** errors or dropped packets. This means your connection is healthy and stable.

---

## 🛠️ Managing ARP Entries Manually

Sometimes you need to manually control the ARP table.

### 1. Adding a Static Entry

This creates a permanent link between an IP and a MAC. It will never expire.

```bash
sudo arp -s 192.168.122.200 00:11:22:22:33:33
```

### 2. Deleting an Entry

This forces your computer to "forget" a device so it has to ask "Who has this IP?" again.

```bash
sudo arp -i enp0s3 -d 192.168.122.200
```

### 3. Masquerading (Proxy ARP)

This tells your computer to answer ARP requests on behalf of *another* IP address.

```bash
sudo arp -i enp0s3 -Ds 10.0.0.2 enp0s3 pub
```

---

## 🎭 Changing the MAC Address (Spoofing)

You demonstrated changing your MAC address. Let's look at why and how.

### ❓ Why Change a MAC Address?

* **Legitimate:** Your ISP might lock your internet to an old device's MAC. Spoofing lets your new router work.
* **Privacy:** Devices like iPhones randomize their MAC to stop shopping malls from tracking your movement.
* **Malicious:** Attackers spoof MACs to bypass security filters or impersonate trusted devices.

### 🔍 Finding Your MAC Address

You used `ip link show` to see your details.

```bash
hashim@Hashim:~$ ip link show enp0s3
...
link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff permaddr 08:00:27:55:08:5a
```

* **`link/ether`**: This is your **current** (spoofed) MAC: `00:11:22:33:44:55`.
* **`permaddr`**: This is your **permanent** (hardware) MAC: `08:00:27...`.

### ⚙️ Method 1: The Temporary Way (Command Line)

This change lasts until you restart the computer.

```bash
sudo ip link set dev enp0s3 down                 # Turn off interface
sudo ip link set dev enp0s3 address 00:11:22:33:44:55  # Change MAC
sudo ip link set dev enp0s3 up                   # Turn on interface
```

### ⚙️ Method 2: The Permanent Way (Netplan)

You used `netplan` to make the change stick even after a reboot.

**Your Configuration (`/etc/netplan/01-netcfg.yaml`):**

```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      match:
        macaddress: 08:00:27:55:08:5a  # Match the Real Card
      macaddress: 00:11:22:33:44:55    # Apply the Fake MAC
      dhcp4: true
```

### Apply the Configuration:

```bash
sudo netplan apply
```

# 🛠️ Changing MAC Address via Udev Rules

This method represents the **lowest-level** and most powerful way to change a MAC address. We utilize **`udev` (User Space Device Manager)** to achieve this.

When Linux boots up and detects hardware (such as your Network Interface Card), `udev` is the very first system that decides how to handle that hardware.

Below is the detailed explanation of this method in English.

---

## 📂 Purpose of the File

We create a new file located at: `/etc/udev/rules.d/75-mac-spoof.rules`.

Inside this file, we define a **Rule** for Linux:

> *"Whenever this specific Network Card is detected, immediately change its MAC address before any other software (like Netplan) takes control."*

---

## 💻 Code Breakdown

It is essential to understand the syntax of the rule. Let's break down the command into its components:

```bash
ACTION=="add", SUBSYSTEM=="net", ATTR{address}=="XX:XX:XX:XX:XX:XX", RUN+="/usr/bin/ip link set dev enp0s3 address YY:YY:YY:YY:YY:YY"

```

| Component | Description |
| --- | --- |
| **`ACTION=="add"`** | This triggers when a new device is **Added** to the system (e.g., when the computer boots or a cable is plugged in). |
| **`SUBSYSTEM=="net"`** | This ensures the rule only applies to devices within the **Network** category (ignoring other hardware like mice or keyboards). |
| **`ATTR{address}=="XX..."`** | Here, you replace **"XX"** with your **Original Hardware MAC**. This tells the system: *"Only target the specific card that has this physical address."* |
| **`RUN+="..."`** | If the conditions above are met, execute this **Command**. We use the `ip link` command here to swap the MAC address to **"YY"** (your Fake MAC). |

---

## 🚀 Step-by-Step Implementation

If you wish to use this method instead of Netplan, follow these steps using your specific system details:

### Step 1: Create the Rule File

Run the following command in your terminal:

```bash
sudo nano /etc/udev/rules.d/75-mac-spoof.rules

```

### Step 2: Add the Rule

Paste the following line into the file. The values have been updated to match your system:

* **Target (Real MAC):** `08:00:27:55:08:5a`
* **New (Fake MAC):** `00:11:22:33:44:55`
* **Interface:** `enp0s3`

```text
ACTION=="add", SUBSYSTEM=="net", ATTR{address}=="08:00:27:55:08:5a", RUN+="/usr/bin/ip link set dev enp0s3 address 00:11:22:33:44:55"

```

### Step 3: Save and Reboot

Save the file (`Ctrl+O`, `Enter`, `Ctrl+X`) and then restart your system.
When the system comes back online, the MAC address will have been changed automatically during the boot process.

---

## ⚖️ Netplan vs. Udev: Which is Better?

* **Netplan:** Easier to configure and is the standard for modern Ubuntu systems. **(Recommended for your current setup).**
* **Udev:** Slightly more complex, but useful if Netplan is failing, or if you require the MAC address to be changed at the absolute earliest moment during the system boot sequence.

---

# 🏷️ MAC Address OUI Values

## 📘 Overview

We have already covered **timeouts** and **ARP** (Address Resolution Protocol), but our journey through **Layer 2** is not finished yet. We must understand the **Organizationally Unique Identifier (OUI)**.

Just like an **IP address** is split into two parts (Network and Host) using a subnet mask, a **MAC address** has a very similar dividing line! A MAC address is not just a random string of numbers; it follows a strict structure that tells us who made the device.

---

## 🧩 The Structure of a MAC Address

A standard MAC address is **48 bits** long (6 bytes). It is usually split right in the middle.

### 1. The Manufacturer (OUI)

* **Location:** The **Leading Bits** (usually the first 3 bytes / 6 characters).
* **Name:** **OUI** (Organizationally Unique Identifier).
* **Purpose:** Identifying the company that manufactured the network card (e.g., Dell, Apple, Cisco).

### 2. The Device ID (NIC Specific)

* **Location:** The **Last 3 bytes**.
* **Purpose:** Uniquely identifying the specific device made by that manufacturer.

### 📉 Visual Breakdown

If we look at a MAC address like `00:0C:29:3B:73:CB`:

| Part | Value | Description |
| --- | --- | --- |
| **OUI (First Half)** | `00:0C:29` | **VMware, Inc.** (This tells us the device is a Virtual Machine). |
| **Device ID (Second Half)** | `3B:73:CB` | **Unique Serial Number** assigned to this specific card. |

> **Note:** While the standard split is 50/50 (24 bits for OUI, 24 bits for Device), organizations can sometimes purchase **longer OUIs** for a lower fee. This gives them a longer prefix but fewer available unique addresses to assign to devices.

---

## 📚 The Registries: Who Tracks This?

OUIs are not random; they must be registered. There are two main sources for this data:

### 1. The Official IEEE Registry

The **IEEE** (Institute of Electrical and Electronics Engineers) maintains the formal list of all assigned manufacturers.

* **Source:** [http://standards-oui.ieee.org/oui.txt](http://standards-oui.ieee.org/oui.txt)

### 2. The Wireshark Registry

The **Wireshark** project (a famous network analysis tool) maintains a more complete and practical listing.

* **Source:** [https://gitlab.com/wireshark/wireshark/-/raw/master/manuf](https://gitlab.com/wireshark/wireshark/-/raw/master/manuf)

---

## 🔍 Practical Use: Network Troubleshooting

Why should a network administrator care about OUIs? They are incredibly valuable for **troubleshooting**.

* **Identifying "Culprits":** If an unknown device is causing problems on your network (like flooding traffic), looking at the OUI tells you what *kind* of device it is.
* *Example:* If the MAC starts with `B8:27:EB`, you know it is a **Raspberry Pi**. If it starts with `00:11:22`, it might be a specific router brand.


* **Security Scanning:** Tools like **Nmap** (Network Mapper) use OUI values to guess the operating system and hardware of devices they scan. We will explore this further in later chapters.

---

## 🛠️ Tools for OUI Lookup

You do not need to memorize these codes. There are tools available to help you look them up instantly.

### 🌐 Web-Based Lookup

Wireshark provides an easy-to-use web application where you can paste a MAC address to find the manufacturer.

* **Tool:** [https://www.wireshark.org/tools/oui-lookup.html](https://www.wireshark.org/tools/oui-lookup.html)

### 💻 Command-Line Parser

If you prefer working in the terminal (Linux or Windows) and want to parse OUIs via scripts, there is a dedicated tool available on GitHub.

* **Repository:** [https://github.com/robvandenbrink/ouilookup](https://github.com/robvandenbrink/ouilookup)

---

## 🚀 Next Steps: Moving Up the Stack

This concludes our deep dive into **Layer 2 (Data Link Layer)** of the OSI model. We have covered:

* MAC Addresses and hardware identity.
* ARP (Address Resolution Protocol).
* The relationship between Layer 2 and Layer 3.

Now, we are ready to venture higher into the stack. Next, we will explore **Layer 4 (Transport Layer)**, specifically focusing on the **TCP** and **UDP** protocols and the services they provide.


---

# 🚦 Layer 4: How TCP and UDP Ports Work

## 📘 Overview

When networking professionals discuss **Layer 4** (the Transport Layer), they are almost always talking about two specific protocols: **TCP** (Transmission Control Protocol) and **UDP** (User Datagram Protocol).

The most critical concept at this layer is the **Port**. While IP addresses (Layer 3) get traffic to the right computer, **Ports** (Layer 4) get traffic to the right *application* (like your web browser, email client, or game) running on that computer.

---

## 🔗 The Connection Process

When your computer (Station A) wants to talk to a server (Station B), a specific sequence of events happens:

1. **Layer 2/3 Check:** First, the system identifies the target IP. It checks its **ARP Cache** to see if it has the MAC address. If not, it sends a broadcast ARP request to find it.
2. **Layer 4 Handshake:** Once the physical path is known, the Transport Layer takes over to establish a **Port-to-Port** connection.

### 🎲 Ephemeral Ports (The Source)

Your computer needs a "return address" so the server knows where to send replies.

* It picks a random available port number.
* **Range:** Usually between **1024** and **65535**.
* **Name:** This is called an **Ephemeral Port** (meaning temporary).

### 🎯 Server Ports (The Destination)

The server listens on a fixed, well-known port number so everyone knows where to find it (e.g., Port 80 for a Web Server).

---

## 🧩 The "5-Tuple" Concept

How does the network keep millions of connections straight without getting them mixed up? It uses a unique identifier called a **Tuple**.

Every connection is uniquely identified by these **5 values** (The 5-Tuple):

1. **Source IP Address**
2. **Destination IP Address**
3. **Source Port** (The random ephemeral port)
4. **Destination Port** (The fixed server port)
5. **Protocol** (TCP or UDP)

Because the Source Port is always chosen randomly, this combination is mathematically guaranteed to be unique for every single connection.

> **Note:** In advanced networking (like NetFlow), this tuple can be expanded to include other data like **VLANs**, **QoS** (Quality of Service), or **ASNs** (Autonomous System Numbers).

---

## 🔢 Port Number Ranges

Port numbers are divided into three specific ranges based on their purpose:

| Range | Name | Description |
| --- | --- | --- |
| **0 – 1023** | **System / Well-Known Ports** | Reserved for core services (e.g., Web, Email). On Linux/Unix, you need **Root privileges** to run an app on these ports. |
| **1024 – 49151** | **User Ports** | Used for less critical services and registered applications. |
| **49152 – 65535** | **Dynamic / Private Ports** | Usually used for ephemeral (temporary) source ports. |

> **Historical Note:** While databases and custom apps often use ports above 1024, the range 0-1023 is historically reserved for the "founding" services of the internet.

---

## 📋 Common Standard Ports

Below is a list of commonly used services and their assigned ports:

| Service | Port / Protocol | Description |
| --- | --- | --- |
| **DNS** | `udp/53`, `tcp/53` | Domain Name System (Resolves names to IPs) |
| **Telnet** | `tcp/23` | Unencrypted remote terminal access |
| **SSH** | `tcp/22` | Secure (Encrypted) Remote Shell |
| **FTP** | `tcp/20`, `tcp/21` | File Transfer Protocol |
| **HTTP** | `tcp/80` | Standard Unencrypted Web Traffic |
| **HTTPS** | `tcp/443` | Secure (Encrypted) Web Traffic |
| **SNMP** | `udp/162` | Simple Network Management Protocol |
| **Syslog** | `tcp/443` | System Logging (Note: Standard is 514, but 443 is often used for secure tunneling) |

---

## 🏛️ The IANA Registry vs. Reality

The **IANA** (Internet Assigned Numbers Authority) maintains the official list of port assignments (documented in **RFC6335**).

* **The Rule:** You *should* use these assigned ports.
* **The Reality:** It is more of a "Strong Suggestion."
* It would be foolish to run a Web Server on Port 53 (confusing it with DNS).
* However, many vendors pick random unassigned ports or "borrow" ports assigned to obscure, unused services for their own applications.



As long as you don't use a famous port (like 80 or 443) for something weird, it usually works fine.

---

# 🤝 Layer 4: TCP and the Three-Way Handshake

## 📘 Overview: UDP vs. TCP

At Layer 4, two main protocols dominate the internet: **UDP** (User Datagram Protocol) and **TCP** (Transmission Control Protocol). They handle data very differently.

### 🚀 UDP: The "Fire and Forget" Protocol

UDP is simple. Once it determines the **5-tuple** (Source IP, Dest IP, Source Port, Dest Port, Protocol), it just starts sending data.

* **No Overhead:** It does not check if data arrived safely.
* **Use Case:** Ideal for **Time-Critical Applications** like **VoIP (Voice over IP)** and **Video Streaming**.
* **Why?** If a packet of audio is lost during a phone call, it is better to just skip it. Stopping to "retry" (backtracking) would cause a noticeable lag or freeze for the user.

### 🛡️ TCP: The Reliable Protocol

TCP is different. It values reliability over raw speed.

* **Sequence Numbers:** It assigns a number to every packet.
* **Error Checking:** It tracks dropped or corrupted packets and resends them automatically.
* **The Cost:** This requires a setup phase before any data can be sent. This setup is called the **Three-Way Handshake**.

---

## 🤝 The TCP Three-Way Handshake

Before a TCP conversation starts, the Client and Server must agree on "Sequence Numbers" to track the data. This negotiation happens in three specific steps.

### 1️⃣ Step 1: The Client Says "Hello" (SYN)

The client (your computer) initiates the connection using an **Ephemeral Port** to the server's **Fixed Port**.

* **Flag:** **SYN** (Synchronize).
* **Sequence Number:** The client generates a random number (e.g., `5432`).
* **Meaning:** "I want to sync with you. My tracking number starts at 5432."

### 2️⃣ Step 2: The Server Replies (SYN-ACK)

The server receives the request and replies. This is technically two steps combined into one packet.

* **Flag 1:** **ACK** (Acknowledge). It confirms the client's number by adding 1 (`5433`).
* **Flag 2:** **SYN** (Synchronize). The server sends its *own* random tracking number (e.g., `6543`).
* **Meaning:** "I hear you (ACK 5433). I am ready to sync, and my tracking number starts at 6543."

### 3️⃣ Step 3: The Client Confirms (ACK)

The client acknowledges the server's tracking number.

* **Flag:** **ACK**. It confirms the server's number by adding 1 (`6544`).
* **Meaning:** "I hear you (ACK 6544). Connection established."

### 4️⃣ Step 4: Data Transfer

Once this is done, the connection is **Established**. Both sides now trust each other and track every byte sent. All future packets will be ACK packets that increment these numbers.

---

## 🛑 Ending the Connection

Just as there is a formal way to start a chat, there is a formal way to end it.

### 🍂 Graceful Termination (The Polite Goodbye)

When the conversation is done, the parties shut it down cleanly.

1. **Sender:** Sends a **FIN** (Finish) packet.
2. **Receiver:** Replies with a **FIN-ACK**.
3. **Sender:** Sends a final **ACK**.
4. **Result:** The connection is closed, and resources are released.

### 💥 Ungraceful Termination (The "Hang Up")

Sometimes, a connection must be killed instantly (e.g., if an error occurs or a firewall blocks it).

* **Packet Type:** **RST** (Reset).
* **Result:** The conversation ends immediately. The other party should not reply.

---

# 🔍 Local Port Enumeration: What Am I Connected To?

## 📘 Overview 

One of the most fundamental troubleshooting steps in networking is checking the status of ports on your local machine. If a web server isn't working, the first question is: "Is the process actually running and listening on the correct port?"

To answer this, we use the **`netstat`** command. It allows us to assess the state of network conversations and services on the local host.

---

## 💻 The Command: `netstat -tuan`

The traditional method to list all listening ports and active connections is `netstat`. We use a specific set of flags to get the most useful information.

### 🛠️ Command Breakdown

The command `netstat -tuan` is composed of four specific options. Here is what each letter does:

| Flag | Meaning | Description |
| --- | --- | --- |
| **-t** | **TCP** | Show only TCP ports. |
| **-u** | **UDP** | Show only UDP ports. |
| **-a** | **All** | Show **all** ports (both those currently connected and those just "listening" for new connections). |
| **-n** | **Numeric** | Do **not** try to resolve DNS names. This makes the command much faster because it shows IP addresses (e.g., `8.8.8.8`) instead of trying to look up names (e.g., `google-public-dns-a.google.com`). |

---

## 📊 Analyzing the Output

Let's look at the practical output provided in your example and break down what it means.

**Example Output:**

```bash
hashim@Hashim:~$ netstat -tuan
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.54:53           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:53            0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:53            0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:953           0.0.0.0:*               LISTEN     
tcp        0      0 10.0.2.15:53            0.0.0.0:*               LISTEN     
tcp        0      0 10.0.2.15:53            0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN     
tcp6       0      0 :::111                  :::*                    LISTEN     
tcp6       0      0 ::1:53                  :::*                    LISTEN     
tcp6       0      0 ::1:53                  :::*                    LISTEN     
tcp6       0      0 ::1:631                 :::*                    LISTEN     
tcp6       0      0 ::1:953                 :::*                    LISTEN     
udp        0      0 0.0.0.0:5353            0.0.0.0:*                          
udp        0      0 10.0.2.15:53            0.0.0.0:*                          
udp        0      0 10.0.2.15:53            0.0.0.0:*                          
udp        0      0 127.0.0.1:53            0.0.0.0:*                          
udp        0      0 127.0.0.1:53            0.0.0.0:*                          
udp        0      0 127.0.0.54:53           0.0.0.0:*                          
udp        0      0 127.0.0.53:53           0.0.0.0:*                          
udp        0      0 0.0.0.0:67              0.0.0.0:*                          
udp        0      0 10.0.2.15:68            10.0.2.2:67             ESTABLISHED
udp        0      0 0.0.0.0:111             0.0.0.0:*                          
udp        0      0 10.0.2.15:123           0.0.0.0:*                          
udp        0      0 127.0.0.1:123           0.0.0.0:*                          
udp        0      0 0.0.0.0:123             0.0.0.0:*                          
udp        0      0 0.0.0.0:37297           0.0.0.0:*                          
udp6       0      0 :::5353                 :::*                               
udp6       0      0 ::1:53                  :::*                               
udp6       0      0 ::1:53                  :::*                               
udp6       0      0 :::111                  :::*                               
udp6       0      0 ::1:123                 :::*                               
udp6       0      0 :::123                  :::*                               
udp6       0      0 :::35105                :::* 
```

### 🔍 Column Explanation

1. **Proto:** The protocol used (TCP or UDP).
2. **Local Address:** The IP and Port on **your** computer.
* `0.0.0.0:22` means "Listen on **all** network cards on port 22 (SSH)."
* `127.0.0.1:53` means "Listen only internally (localhost) on port 53 (DNS)."


3. **Foreign Address:** The IP and Port of the **remote** computer you are talking to.
* `0.0.0.0:*` means "I am not connected to anyone specific yet; I am just waiting."


4. **State:** The current status of the connection (Explained below).

---

## 🚦 Understanding TCP States

TCP is a stateful protocol. It doesn't just send data; it tracks the life of the connection.

### 1️⃣ Common States (Stable)

These are the states you will see most often. If you see these, everything is usually normal.

* **LISTEN:** There is a service (like a Web Server or SSH) running on your computer, waiting for someone to connect to it.
* **ESTABLISHED:** The connection is active! The **3-way handshake** is complete, and both you and the server are ready to trade data.
* *Tip:* You can tell who is the client and who is the server by the ports. If the "Local" port is a random high number and the "Foreign" port is 80 (Web), you are the client.


* **TIME_WAIT:** The session is closed, but your computer is keeping the socket open for a few seconds just in case any lost packets arrive late. This prevents old data from mixing with a new connection.

### 2️⃣ Transient States (Connection Setup)

These states happen during the **3-way handshake**. They should happen so fast (milliseconds) that you rarely see them. If you see a lot of these sticking around, you might have a problem.

* **SYN_SENT:** You (the client) sent a "Hello" (SYN) packet and are waiting for a reply..
* **SYN_RECV:** You (the server) received a "Hello" (SYN) and replied with "Hello/Ack" (SYN-ACK). You are waiting for the final confirmation.

**Diagram: The Connection Handshake**
As the connection moves from `LISTEN` to `ESTABLISHED`, it follows this path:

1. **Client** sends SYN -> **Server** sees `SYN_RCVD`.
2. **Server** sends SYN/ACK -> **Client** sees `ESTABLISHED`.
3. **Client** sends ACK -> **Server** sees `ESTABLISHED`.

### 3️⃣ Transient States (Connection Teardown)

Closing a connection is more complex than starting one. These states appear when "tearing down" a session.

* **FIN_WAIT1 and 2:** The connection is shutting down. You are waiting for the other party to say "Goodbye" (FIN packet).
* **CLOSE_WAIT:** The remote side said "Goodbye," and your computer is waiting for the **Application** (Layer 7) to stop working so it can close the socket.
* *Troubleshooting:* If you see a lot of `CLOSE_WAIT`, it often means a poorly written application is hanging and not closing connections properly.


* **LAST_ACK:** You are almost closed. You sent the final "Goodbye" and are waiting for the very last acknowledgment.
* **CLOSING:** Both sides tried to hang up at the exact same time, but data transfers weren't quite finished.

**Diagram: The Teardown**
Notice how many steps are required to disconnect cleanly compared to connecting:

* The initiator sends `FIN` (enters `FIN_WAIT_1`).
* The receiver sends `ACK` (enters `CLOSE_WAIT`) and then sends its own `FIN` (enters `LAST_ACK`).
* The initiator replies with `ACK` (enters `TIME_WAIT`) before finally closing.

---

# 🛠️ Advanced Port Enumeration: Linking Processes to Ports

## 📘 Overview

In the previous section, we used `netstat` to see which ports were "listening." However, knowing that *something* is listening on Port 80 isn't enough. We need to know **exactly which program** is responsible.

This section covers:

1. Using flags to identify Process IDs (PIDs) and Program Names.
2. Using the modern alternative command `ss`.
3. Advanced text processing (piping, cutting, and translating) to format output.
4. Using `lsof` to view network connections as "files."

---

## 🔍 Identifying the Process: `netstat -tulpn`

To relate listening ports back to the specific services running them, we add the **`-p`** flag (Program) to our `netstat` command.

> **Note:** You must run this with `sudo` (root privileges). If you don't, the system hides the process names for security reasons.

### 💻 Command Execution

```bash
hashim@Hashim:~$ sudo netstat -tulpn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.53:53           0.0.0.0:* LISTEN      339/systemd-resolve 
tcp        0      0 0.0.0.0:22              0.0.0.0:* LISTEN      1/init              
tcp        0      0 127.0.0.1:631           0.0.0.0:* LISTEN      1410/cupsd          
...
udp        0      0 0.0.0.0:5353            0.0.0.0:* 699/avahi-daemon: r 
```

### 📊 Output Analysis

The `-p` flag adds a crucial new column: **PID/Program name**.

* **`339/systemd-resolve`**: The system DNS resolver (PID 339) is listening on port 53.
* **`1410/cupsd`**: The printing service (CUPS, PID 1410) is listening on port 631.
* **`699/avahi-daemon`**: The Avahi service (for network discovery) is listening on UDP port 5353.

This tells you exactly what to kill or reconfigure if a port is busy.

---

## 🚀 The Modern Alternative: `ss`

Just as `ip` replaced `ifconfig`, the **`ss`** (Socket Statistics) command is the modern replacement for `netstat`. It is faster and provides more detail.

### 💻 Command: `ss -tulpn`

```bash
hashim@Hashim:~$ sudo ss -tulpn
Netid      State       Recv-Q      Send-Q           Local Address:Port            Peer Address:Port      Process                                                                                                  
udp        UNCONN      0           0                      0.0.0.0:5353                 0.0.0.0:* users:(("avahi-daemon",pid=699,fd=12))                                                                  
udp        UNCONN      0           0                    10.0.2.15:53                   0.0.0.0:* users:(("named",pid=1419,fd=35))                                                                        
tcp        LISTEN      0           4096                   0.0.0.0:22                   0.0.0.0:* users:(("sshd",pid=1480,fd=3),("systemd",pid=1,fd=267))                                                 
...
```

### 🔍 Comparison: `ss` vs `netstat`

* **Syntax:** Almost identical flags (`-tulpn`).
* **Detail:** `ss` shows the "users" in a more structured format: `users:(("process_name",pid=123,fd=4))`.
* **Accuracy:** `ss` queries the kernel directly, making it faster on busy systems.

---

## ✂️ Advanced Formatting: Piping & Cutting

The output of `ss` can be wide and messy. We can use Linux command-line magic to clean it up.

### The Goal

We want to extract **only** specific columns (Netid, State, Local Address, Peer Address) and format them into a neat table.

### The Tools

1. **`tr -s ' '`**: The `tr` (translate) command with the squeeze (`-s`) option. It takes multiple spaces (which look messy) and squeezes them into a single space.
2. **`cut -d ' ' -f 1,2,5,6`**: The `cut` command splits each line using the space as a delimiter (`-d ' '`) and keeps fields 1, 2, 5, and 6.
3. **`--output-delimiter=$'\t'`**: This inserts a **Tab** character between the columns, making them line up perfectly.

### 💻 The Magic Command

```bash
hashim@Hashim:~$ sudo ss -tuap | tr -s ' ' | cut -d ' ' -f 1,2,5,6 --output-delimiter=$'\t'
```

### 📤 Clean Output

```text
Netid	State	Local	Address:Port
udp	UNCONN	0.0.0.0:mdns	0.0.0.0:*
udp	ESTAB	10.0.2.15:55031	8.8.8.8:domain
tcp	LISTEN	0.0.0.0:ssh	0.0.0.0:*
...

```

Now, the output is readable and aligned!

### 💾 Exporting to a File (Redirection)

We can save this clean output to a file (like a spreadsheet CSV or TSV) using the **`>`** operator.

```bash
hashim@Hashim:~$ sudo ss -tuap | ... > ports.tsv
```

You can now open `ports.tsv` in Excel or LibreOffice.

---

## ⚡ Power User Trick: `tee` and `grep`

What if you want to see the output on screen **AND** save it to a file at the same time? Use **`tee`**.
What if you only care about **active** connections? Use **`grep`**.

### 💻 Command

```bash
hashim@Hashim:~$ sudo ss -tuap | ... | grep "EST" | tee ports.out
```

### 📤 Output

```text
udp	ESTAB	10.0.2.15%enp0s3:bootpc	10.0.2.2:bootps

```

This filters for lines containing "EST" (Established) and saves the result to `ports.out`.

---

## 🕵️ Troubleshooting with `ss` Options

Sometimes connections hang. Firewalls often kill idle connections silently. You can use `ss` to investigate this.

### 💻 Command: `ss -to`

* **`-t`**: TCP only.
* **`-o`**: Show **Timer** options.

```text
ESTAB 0 0 192.168.122.22:42502 44.227.121.122:https timer:(keepalive,6min47sec,0)

```

**Why is this useful?**
It shows the **Keepalive Timer** (`6min47sec`). If you have a backup job failing after exactly 10 minutes, and the firewall has a 10-minute timeout, this timer confirms the connection is idle and likely being killed by the firewall.

---

## 📂 The "Everything is a File" Concept: `lsof`

In Linux, **everything is treated as a file**, including network connections. This allows us to use the **`lsof`** (List Open Files) command for networking.

### 💻 Command: `lsof -i :port`

This lists all "files" (connections) using a specific network port.

**Example 1: Who is using Port 443 (HTTPS)?**

```bash
$ lsof -i :443
COMMAND PID  USER  FD   TYPE DEVICE SIZE/OFF NODE NAME
firefox 4627 robv  162u IPv4 93018  0t0      TCP  ... (ESTABLISHED)
```

* **Result:** Firefox (PID 4627) is browsing the web.

**Example 2: Who is using Port 22 (SSH)?**

```bash
$ lsof -i :22
COMMAND PID  USER  FD   TYPE DEVICE SIZE/OFF NODE NAME
ssh     5832 robv  3u   IPv4 103832 0t0      TCP  ... (ESTABLISHED)
```

* **Result:** The SSH client (PID 5832) is connected.

---

## ❓ Why Does This Matter?

Why are we obsessed with knowing exactly which process is on which port?
**Answer: The "Single Tenant" Rule.**

**Only one service can listen on a specific port at a time.**

* If Apache Web Server is running on Port 80, and you try to start Nginx on Port 80, Nginx will crash immediately.
* Using `netstat`, `ss`, or `lsof` lets you instantly identify the conflict ("Oh, Apache is already running!") so you can stop the old service and start the new one.

---

# 🛠️ Remote Port Enumeration Using Native Tools

## 📘 Introduction

We have learned how to check our **local** listening ports. Now, the question is: How do we check ports on **other** computers (remote hosts)?

Knowing which ports are open on a remote server is critical for troubleshooting.

* **Is the web server running?**
* **Is the firewall blocking my connection?**

We often use "Native Tools" (tools already installed on the system) for this because we might not have permission to install fancy scanners like Nmap.

---

## 📞 Tool 1: Telnet (The Quick Check)

`telnet` is an old protocol, but it is excellent for a quick "ping" test on a specific port. If `telnet` connects, the port is Open. If it hangs or refuses, the port is Closed or Filtered.

### 💻 Practical Example: Telnetting to Google

You tried connecting to Google's web server on port 80.

**Command:**

```bash
hashim@Hashim:~$ telnet google.com 80
```

**Your Output Analysis:**

```text
Trying 142.250.201.238...
Connected to google.com.
Escape character is '^]'.
GET / HTTP/1.1
Host: google.com

HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
...

```

**What happened here?**

1. **`Connected to google.com`**: This is the most important line. It proves **TCP Port 80 is OPEN**.
2. **`HTTP/1.1 301 Moved Permanently`**: You manually typed a web request (`GET /...`). The server replied saying, "I have moved." This is standard behavior—Google redirects unencrypted HTTP traffic to encrypted HTTPS.
3. **Cursor Blinking:** The connection stayed open because you didn't send a "Connection: close" header, so the server waited for more input until you closed it.

**The Downside:**
`telnet` is clumsy. You often get stuck in a session and have to mash `Ctrl+C` or `Ctrl+]` then type `quit` to get out.

---

## 🐱 Tool 2: Netcat (`nc`) - The Swiss Army Knife

**Netcat (`nc`)** is a much better tool. It is designed for scripting and raw network connections. We use specific flags to make it a port scanner.

### 🚩 Key Flags

* **`-z` (Zero-I/O mode):** Connect, check status, and disconnect immediately. Do not send data.
* **`-v` (Verbose):** Print results to the screen (tell me if it worked).

### 💻 Scenario 1: Scanning Specific Ports

You scanned Google for Web (80) and Secure Web (443).

**Command:**

```bash
hashim@Hashim:~$ nc -zv google.com 80
hashim@Hashim:~$ nc -zv google.com 443
```

**Output:**

```text
Connection to google.com (142.250.201.238) 80 port [tcp/http] succeeded!
Connection to google.com (142.250.201.238) 443 port [tcp/https] succeeded!

```

**Result:** Both ports are open. Simple and clean.

---

### 💻 Scenario 2: Scanning a Port Range (1-1024)

You can scan a whole range of ports to see what services a server is running.

**Command:**

```bash
hashim@Hashim:~$ nc -zv 127.0.0.1 1-65535 2>&1 | grep -v refused
```

**Detailed Breakdown of this Trick:**

1. **`1-65535`**: Scans every possible port number.
2. **`2>&1`**: This is the magic part.
* Linux sends "Success" messages to **Standard Output (1)**.
* Linux sends "Connection Refused" (Errors) to **Standard Error (2)**.
* `grep` only filters Standard Output.
* This command redirects Error messages into the Output stream so `grep` can see them.


3. **`| grep -v refused`**: This filters *out* (removes) any line containing "refused," leaving only the success stories.

**Output:**

```text
Connection to 127.0.0.1 22 port [tcp/ssh] succeeded!
Connection to 127.0.0.1 53 port [tcp/domain] succeeded!
Connection to 127.0.0.1 631 port [tcp/ipp] succeeded!
...

```

**Result:** You found SSH (22), DNS (53), and Printing (631) running on your local machine.

---

### 💻 Scenario 3: Scanning UDP Ports

Scanning **UDP** is harder because UDP doesn't send "Acknowledgements" (it's fire-and-forget). We use the **`-u`** flag.

**Command:**

```bash
hashim@Hashim:~$ nc -u -zv 8.8.8.8 53
```

**Output:**

```text
Connection to 8.8.8.8 53 port [udp/domain] succeeded!
```

**Warning:** UDP scanning is **slow** and unreliable. Scanning 1024 ports can take 18+ minutes because the scanner has to wait for a timeout on every single port to decide if it is open or closed.

---

## 🏗️ Netcat as a Server: Creating a Fake Website

Netcat can also **listen** (`-l`). This is amazing for testing firewalls. You can start a "fake" web server on port 1500 to see if traffic can get through.

### 1️⃣ The "Permission Denied" Error

You tried to listen on Port 80:

```bash
echo "<h1>Hello Hashim! This is my Netcat Server</h1>" > index.html
$ while true; do cat index.html | nc -l -p 80 –q 1; done
nc: Permission denied
```

**Reason:** In Linux, ports **0-1023** are reserved for the root user. You cannot open port 80 as a standard user `hashim`.

### 2️⃣ The Solution: Use High Ports

You switched to Port **1500**, which worked.

**Command:**

```bash
hashim@Hashim:~$ while true; do echo -e "HTTP/1.1 200 OK\n\n $(cat index.html)" | nc -l -p 1500 -q 1; done
```

* **`while true; do ... done`**: Keeps the server running. If a client connects and disconnects, `nc` normally quits. This loop forces it to restart instantly.
* **`echo -e ...`**: Manually creates a fake HTTP Header so web browsers understand the reply.
* **`nc -l -p 1500`**: Listen on Port 1500.

---

**Success Output:**

```bash
hashim@Hashim:~$ curl --http0.9 http://127.0.0.1:1500
<h1>Hello Hashim! This is a Netcat Server</h1>
```

You also added dynamic content (the date):

```bash
hashim@Hashim:~$ curl --http0.9 http://127.0.0.1:1500
 Fri Jan  9 07:11:19 PM PKT 2026
```

---

## 📂 Transferring Files with Netcat

Finally, you used `nc` to copy a file from one computer (or terminal window) to another. This is the simplest "file transfer" protocol in existence.

### 📥 Step 1: The Receiver (Start this first)

The receiver opens a port and directs all incoming data into a file.

**Command:**

```bash
hashim@Hashim:~$ nc -l -p 1234 > received.txt
```

* **`>`**: Redirects output to a file named `received.txt`.
* The cursor blinks, waiting for data.

### 📤 Step 2: The Sender

The sender connects to the receiver and pushes a file *into* the connection.

**Command:**

```bash
hashim@Hashim:~$ echo "Hashim data has been transfered!" > sent-file.txt
hashim@Hashim:~$ nc 127.0.0.1 1234 < sent-file.txt
```

* **`<`**: Takes input from `sent-file.txt` and pushes it into the `nc` command.

### ✅ Step 3: Verification

You checked the file content on the receiving end.

**Command:**

```bash
hashim@Hashim:~$ cat received.txt
"hashim data has been transfered!"
```

**Conclusion:**
Netcat is incredibly versatile. It can:

1. Scan ports.
2. Act as a web server.
3. Transfer files.
4. Act as a chat client.

However, for scanning thousands of hosts professionally, we need something faster. That tool is **Nmap**, which we will discuss next.


---

# 📜 Nmap Scripting Engine (NSE) & Advanced Scanning

## 📘 Overview

We have mastered basic port scanning. Now, we unlock the full power of **Nmap** using its **Scripting Engine (NSE)**.

Nmap is not just a scanner; it is a platform. It uses a built-in scripting engine based on **Lua** (a simple programming language). This allows Nmap to:

* Detect advanced service information (like software versions).
* Check for specific vulnerabilities (like "WannaCry").
* Automate complex networking tasks.

Nmap comes with **hundreds** of pre-written scripts that are invaluable for network administrators.

---

## 🛡️ Case Study: Scanning for SMB Vulnerabilities

A classic use case for Nmap scripts is checking the **SMB (Server Message Block)** protocol. This is the protocol Windows uses to share files.

### ❓ The Problem: SMBv1 & EternalBlue

Microsoft has urged the world to stop using **SMBv1** (an old version of the protocol).

* **Why?** It is insecure. In 2017, the **EternalBlue** exploit used SMBv1 to launch the massive **WannaCry** ransomware attack.
* **The Goal:** We need to scan our network to see if any computers are still using this dangerous protocol.

### 🧪 Practical Example 1: Checking SMB Protocols

We use the script `smb-protocols` to ask the server, "Which versions of SMB do you speak?"

**Command:**

```bash
hashim@Hashim:~$ sudo nmap -p 139,445 --script smb-protocols 10.0.2.0/24
```

**Output Analysis:**

```text
Nmap scan report for _gateway (10.0.2.2)
Host is up (0.0010s latency).

PORT    STATE    SERVICE
139/tcp filtered netbios-ssn
445/tcp open     microsoft-ds

Host script results:
| smb-protocols: 
|   dialects: 
|     2:0:2
|     2:1:0
|     3:0:0
|     3:0:2
|_    3:1:1

```

**🔍 Explanation:**

1. **The Target:** We scanned the `_gateway` (10.0.2.2).
2. **The Port:** TCP Port 445 is **open** (This is the standard SMB port).
3. **The Result:** The script lists the supported dialects:
* `2:0:2` (SMBv2)
* `3:1:1` (SMBv3)
* **Crucial Observation:** It does **NOT** list `NT LM 0.12` (which is SMBv1).
* **Conclusion:** This host is **Safe** from SMBv1 risks.



---

### 🧪 Practical Example 2: Checking for Specific Vulnerabilities

We can be more aggressive. Instead of just asking for versions, we can ask, "Are you vulnerable to the MS17-010 (EternalBlue) exploit?"

**Command:**

```bash
hashim@Hashim:~$ sudo nmap -p 445 --script smb-vuln-ms17-010 10.0.2.0/24
```

**Output Analysis:**

```text
Nmap scan report for _gateway (10.0.2.2)
Host is up (0.00073s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

```

**🔍 Explanation:**

* The scan ran against the gateway.
* **No Script Output:** Notice that there is no "Host script results" section.
* **Meaning:** Nmap typically only prints script output if it finds something positive (i.e., if it found the vulnerability).
* **Conclusion:** The gateway is **not vulnerable** to EternalBlue.


# 🧰 Essential Nmap Scripts for Administrators

Here are the most useful scripts for finding **"Rogue"** or **"Shadow" IT** on your network.

---

## 🏴‍☠️ 1. Finding "Shadow IT" (Unexpected Servers)

These scripts help you find database servers or developer tools that shouldn't be running on a regular network.

| What to look for? | Description & Risk | Scripts to Use |
| :--- | :--- | :--- |
| **Unlicensed / Hidden Databases** | Finds database servers (SQL, Oracle, MongoDB) installed without permission. Often insecure. | `broadcast-ms-sql-discover`<br>`broadcast-sybase-asa-discover`<br>`oracle-tns-version`<br>`broadcast-db2-discover`<br>`couchdb-databases`<br>`mongodb-info` |
| **Personal Jenkins Servers** | Jenkins is a powerful automation tool. Finding one running on a random laptop is a major security risk. | `broadcast-jenkins-discover` |

---

## 🕸️ 2. Unexpected or Malicious Infrastructure

Detects networking gear that might be intercepting your traffic.

| What to look for? | Description & Risk | Scripts to Use |
| :--- | :--- | :--- |
| **Rogue Routers** | Malicious routers can use protocols like RIP or OSPF to redirect traffic (**Man-in-the-Middle**). | `broadcast-eigrp-discovery`<br>`broadcast-igmp-discovery`<br>`broadcast-ospf2-discover`<br>`broadcast-rip-discover`<br>`broadcast-ripng-discover` |
| **Rogue Proxies** | Finds **WPAD** (Web Proxy Auto-Discovery) issues. Hackers use this to steal credentials. | `broadcast-wpad-discover` |
| **Open SNMP** | Finds devices leaking system info via **SNMP**. | `snmp-info` |

---

## 💻 3. Workstation Issues

Scripts to identify weak configurations on regular employee laptops.

| What to look for? | Description & Risk | Scripts to Use |
| :--- | :--- | :--- |
| **UPnP (Universal Plug and Play)** | Devices that automatically open holes in the firewall, creating security risks. | `broadcast-upnp-info` |
| **LLMNR Protocol** | Used by Windows when DNS fails. Easily exploited by hackers to steal credentials. | `llmnr-resolve` |

---

## 🏰 4. Network Perimeter & Server Problems

Scripts to check your "Front Door" (Internet-facing security).

| What to look for? | Description & Risk | Scripts to Use |
| :--- | :--- | :--- |
| **VPN Audit** | Finds VPNs using old, insecure encryption (**IKEv1**) or unauthorized VPN hosts. | `ike-version`<br>`http-cisco-anyconnect` |
| **Rogue DNS Servers** | Finds DNS servers running on your network that you didn't know existed. | `broadcast-dns-service-discovery`<br>`dns-srv-enum` |
| **DNS Recursion** | Checks if your DNS server answers queries for *anyone*. Allows **DDoS attacks**. | `dns-recursion` |
| **Rogue DHCP** | Finds unauthorized routers (like home Wi-Fi routers) handing out bad IP addresses. | `dhcp-discover`<br>`broadcast-dhcp-discover` |

---

## 📏 5. Network Path Troubleshooting (MTU)

| What to look for? | Description & Risk | Script to Use |
| :--- | :--- | :--- |
| **Path MTU** | Calculates largest packet size allowed. Essential for troubleshooting **VPNs** or **WAN links**. | `path-mtu` |

---

## 🛠️ 6. Certificates & Encryption Audits

Scripts to ensure your encryption isn't expired or obsolete.

| What to look for? | Description & Risk | Scripts to Use |
| :--- | :--- | :--- |
| **Certificate Expiry** | Checks if SSL/TLS certificates are about to expire (or already have). | `ssl-cert`<br>`ssl-date` |
| **Weak Encryption (SSL/TLS)** | Finds servers supporting old protocols like **SSLv1** or **TLSv1.0**. | `ssl-dh-params`<br>`ssl-enum-ciphers` |
| **Weak RDP/SSH** | Checks remote access servers for weak encryption settings. | `rdp-enum-encryption`<br>`ssh2-enum-algos`<br>`sshv1` |
| **Bitcoin Mining** | Detects unauthorized crypto mining software. | `bitcoin-info` |



## ⏳ The Limits of Nmap

Nmap is amazing, but it has one major limitation: **Performance**.

### 1. The Scaling Problem

* **Time:** Scanning a small subnet takes seconds. Scanning a large corporate network (or the internet) can take days or weeks.
* **Accuracy:** If a scan takes 24 hours, employees will turn off their laptops before you finish. You miss data.
* **IPv6:** The IPv6 address space is so huge (millions of addresses) that scanning it traditionally is impossible. It would take decades.

### 2. Solutions for Speed

* **Optimization:** You can tune Nmap's timing (`-T4`), parallelism, and timeouts to make it faster. (See `man nmap` or the performance book).
* **Alternative Tools:** For massive scans, professional researchers use **MASSCAN**.
* **MASSCAN** is built for pure speed. It can scan the **entire Internet** (IPv4) in under 10 minutes.


* **Strategy:** "Chain" your tools. Use MASSCAN to quickly find *which* hosts are alive, then feed that list into Nmap for detailed scanning.

---

