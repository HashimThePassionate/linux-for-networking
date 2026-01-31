# 🔐 RADIUS Basics: What It Is and How It Works

## 📘 The Concept of AAA

Before diving into the protocol itself, it is essential to understand **AAA**, the industry-standard framework for controlling access to resources.

* **Authentication (Who are you?):** Proving your identity. While often just a User ID and password, modern systems frequently use Multi-Factor Authentication (MFA).
* **Authorization (What can you do?):** Determining access rights *after* identity is proven. This defines which subnets, hosts, or files a user can access. While "Authentication" and "Authorization" are often used interchangeably in casual conversation, in RADIUS, they are distinct steps.
* **Accounting (What did you do?):** A throwback to dial-up days when users were billed for time usage. Today, accounting tracks session duration and timestamps, primarily for troubleshooting or forensics rather than billing.

## 🛠️ How RADIUS Works

**RADIUS (Remote Authentication Dial-In User Service)** is a simple, widely supported protocol used to implement AAA.

### The Components

1. **Network Access Server (NAS):** This is the device the user actually connects to, such as a VPN gateway, Wireless Access Point, or Network Switch.
2. **RADIUS Server:** The central server that verifies credentials.
3. **Shared Secret:** A password shared between the NAS and the RADIUS server to authenticate the device itself.

### The Process

When a user attempts to connect, the NAS collects their login info and forwards it to the RADIUS server for verification. If the server validates the credentials, it authorizes access.

### 📡 Protocol Details & Ports

* **Transport:** RADIUS uses **UDP** (User Datagram Protocol). Because UDP is connectionless (stateless), the protocol must handle session tracking within the packet payload.
* **Ports:**
* **1812/udp:** Authentication.
* **1813/udp:** Accounting.
* *Legacy Support:* Many servers still support the older ports **1645** and **1646**.



## 📦 Anatomy of a RADIUS Packet

A typical RADIUS packet contains several critical fields:

* **Packet ID:** Since UDP has no session concept, this ID ties a specific Request packet to its corresponding Response packet.
* **Authenticator:** A unique, randomly generated field used to verify the integrity of the packet.
* **AV Pairs (Attribute-Value Pairs):** The payload consists of these pairs (labeled AVP). They make the protocol extensible, allowing vendors to add specific data (like distinguishing between a VPN user and an Admin user).
* **Code:** Identifies the type of packet (e.g., is this a request? an acceptance? a rejection?).

### RADIUS Packet Codes

The **Code field** is the first part of the packet and determines its function. The table below outlines the standard codes:

* **Code 1 (Access-Request):** The NAS asking the server to approve a user.
* **Code 2 (Access-Accept):** The server granting access.
* **Code 3 (Access-Reject):** The server denying access.
* **Code 4/5:** Used for Accounting (logging start/stop times).


---