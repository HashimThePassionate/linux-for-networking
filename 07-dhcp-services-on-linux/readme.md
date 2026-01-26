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