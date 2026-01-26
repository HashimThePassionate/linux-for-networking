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