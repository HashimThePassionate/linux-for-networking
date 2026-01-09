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