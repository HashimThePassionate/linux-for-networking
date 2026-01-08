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

