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