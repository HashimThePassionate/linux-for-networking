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

# 📡 RADIUS Packet Analysis: The Authentication Exchange

## 📘 Overview

Now that we understand the structure of a RADIUS packet (Codes, IDs, Authenticators), let's analyze a real-world authentication attempt. This exchange involves a client sending credentials and the server replying with a definitive "Yes" or "No."

---

## 📤 1. The Access-Request (Figure 9.1)

The process begins when the NAS (Network Access Server) sends an **Access-Request (Code 1)** to the RADIUS server.

### Key Packet Details:

* **Packet ID (0x2):** This number (2) is crucial. The server *must* reply with the exact same ID so the NAS knows which user the answer is for.
* **Authenticator:** A unique random string generated for this specific session.

### Attribute Value Pairs (AVPs):

* **User-Name:** Sent in **Clear Text** (e.g., "robv"). Anyone capturing the traffic can see the username.
* **User-Password:** Labeled as "Encrypted," but technically, it is an **MD5 Hash**.
* **How it works:** The password is NOT sent in plain text. It is hashed using a combination of:
1. The Password text.
2. The **Shared Secret** (only known to the NAS and Server).
3. The **Request Authenticator**.


* **Security Note:** This prevents an eavesdropper from easily reading the password, but since it uses MD5 (an older hashing algorithm), it is considered weak by modern standards unless wrapped in a stronger protocol (like TLS).



---

## 📥 2. The Response: Accept or Reject

The server processes the request and sends a reply. The **Packet Code** tells us the verdict.

### Scenario A: Access-Accept (Figure 9.2)

If the username and password are correct, the server sends **Code 2**.

* **Code:** `Access-Accept (2)`.
* **Packet Identifier:** `0x2`. It matches the request's ID exactly, confirming this is the answer for "robv".
* **Response Authenticator:** This is a calculated MD5 checksum. The NAS uses this to verify that the reply actually came from the real RADIUS server and not an imposter. It is calculated using the Code, ID, Length, Request Authenticator, and the **Shared Secret**.

### Scenario B: Access-Reject (Figure 9.3)

If the credentials are wrong (or the user is not allowed), the server sends **Code 3**.

* **Code:** `Access-Reject (3)`.
* **Packet Identifier:** Matches the request ID (In this specific screenshot, it is `0x3`, indicating it belongs to a different session than the example above).
* **Outcome:** The user is denied access. This usually happens due to a typo in the password or a disabled account.

---

## 🔑 Summary of the Security Mechanism

The security of this simple RADIUS exchange relies entirely on the **Shared Secret**.

1. **Request:** The client proves it knows the secret by hashing the password with it.
2. **Response:** The server proves it is legitimate by hashing the response authenticator with it.
3. **Result:** If the Shared Secret is compromised, an attacker can decrypt passwords and spoof server responses.


---