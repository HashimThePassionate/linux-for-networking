# 🌐 Linux Network Configuration: Interfaces & Routes

## 📘 Chapter Overview

Welcome to the guide on configuring and displaying local network interfaces and routes on a Linux host. In this documentation, we will cover both **modern** and **legacy (old)** commands used for these tasks.

You will learn how to:

* 👀 **View** network settings.
* ✏️ **Modify** IP addresses and route parameters.
* 🧮 **Understand** how IP addresses and subnet masks are built using binary numbers.

This knowledge provides a strong foundation for future tasks like troubleshooting network issues, securing your computer (hardening), and setting up secure services.

---

## 📑 Topics Covered

This guide focuses on the following key areas:

1. **Network Settings Tools:** Comparing two different sets of commands (Old vs. New).
2. **Interface Information:** How to display IP details.
3. **IPv4 & Subnets:** Understanding addresses and masks.
4. **IP Assignment:** How to manually assign an IP address to an interface.

---

## 🛠️ Technical Requirements

To follow along with this guide, you should practice the commands on your own computer.

* **Operating System:** The examples are based on **Ubuntu Linux, version 24** (Long-Term Support).
* **Compatibility:** These commands work exactly the same or very similarly on almost any other Linux distribution (like Fedora, CentOS, or Debian).

---

## 1. Working with Network Settings: Two Sets of Commands

In Linux, there is a shift from old tools to new tools. We will explore both so you can work on any system.

### 🏛️ The Legacy (Old) Commands

Historically, Linux used the `net-tools` package. You might still see these in older tutorials.

* **Command:** `ifconfig`
* **Status:** Deprecated (no longer recommended for new setups, but good to know).

### 🚀 The Modern (New) Commands

Modern Linux systems use the `iproute2` package. This is the standard now.

* **Command:** `ip addr`
* **Status:** Recommended and powerful.

---

## 2. Displaying Interface IP Information

Let's look at how to view your current network setup. We will focus on the modern command `ip addr`.

### 💻 Practical Example: The `ip addr` Command

Open your terminal and type the following command:

```bash
ip addr show
```

### 🔍 Detailed Explanation of Output

When you run this command, you will see output that looks like this:

```text
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:56:92:4a brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.15/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86184sec preferred_lft 86184sec

```

Here is exactly what this means, line by line:

1. **`2: eth0`**: This is the ID number (2) and the name of the interface (`eth0`). This is your network card.
2. **`<BROADCAST,MULTICAST,UP...>`**: These are "flags."
* `UP` means the interface is turned on and working.


3. **`link/ether 08:00:27...`**: This is your **MAC Address** (Hardware address). It is unique to your physical network card.
4. **`inet 192.168.1.15/24`**: This is your **IPv4 Address**.
* `192.168.1.15`: The actual IP address of your machine.
* `/24`: The subnet mask (in shorthand format).



---

## 3. IPv4 Addresses and Subnet Masks (Binary Approach)

To truly understand networking, we must look at how computers see IP addresses: as **Binary Numbers** (0s and 1s).

### 🧮 How It Works

An IPv4 address is made of **32 bits**. We usually split these into 4 groups of 8 bits (called octets).

#### Practical Example: Converting `192.168.1.1`

Let's break down the IP address `192.168.1.1` from scratch.

| Decimal Number | Calculation | Binary Result |
| --- | --- | --- |
| **192** | 128 + 64 | `11000000` |
| **168** | 128 + 32 + 8 | `10101000` |
| **1** | 1 | `00000001` |
| **1** | 1 | `00000001` |

**Final Binary View:**
`11000000.10101000.00000001.00000001`

### 🎭 The Subnet Mask

The subnet mask tells the computer which part of the IP is the **Network** and which part is the **Host** (your specific computer).

* **Example Mask:** `255.255.255.0`
* **In Binary:** `11111111.11111111.11111111.00000000`

The `1`s represent the network. The `0`s represent the host. This binary approach helps us calculate network ranges precisely.

---

## 4. Assigning an IP Address to an Interface

Sometimes you need to manually set an IP address instead of getting one automatically. We use the `ip addr add` command for this.

### 💻 Practical Example: Adding an IP

Imagine you want to add the IP `10.0.0.5` to your interface named `eth0`.

**Command:**

```bash
sudo ip addr add 10.0.0.5/24 dev eth0
```

### 🔍 Detailed Explanation of the Command

Let's break down every part of this command:

1. **`sudo`**: This gives you "Superuser" (Administrator) privileges. Changing network settings requires admin rights.
2. **`ip`**: This is the main network tool we are using.
3. **`addr`**: This specifies we are working with **Addresses**.
4. **`add`**: This tells the system we want to **add** a new address.
5. **`10.0.0.5/24`**:
* `10.0.0.5`: The new IP address we want.
* `/24`: This represents the subnet mask `255.255.255.0`.


6. **`dev eth0`**: This stands for **Device**. It tells the system *which* network card (`eth0`) gets this IP.

### 📤 Verification Output

After running the command, verify it by typing `ip addr show dev eth0`. You will now see the new IP listed:

```text
inet 10.0.0.5/24 scope global eth0
```

This confirms the IP address has been successfully added to your system!