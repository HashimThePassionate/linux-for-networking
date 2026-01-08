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

