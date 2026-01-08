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

---

# 🛠️ Network Configuration & Package Management in Linux

## 📘 Overview

In the Linux ecosystem, change is the only constant. This document explores the evolution of network commands, the critical role of security privileges (`sudo`), and the power of package management systems (`apt`). We will examine why legacy tools are being replaced and how to manage software across different Linux distributions.

---

## 1. 🔄 Network Commands: Old vs. New

For a long time, the `ifconfig` command was the standard for network configuration. While it is now technically "deprecated" (outdated), many experienced administrators still use it out of habit. However, new administrators are encouraged to learn the modern replacements.

### 🏛️ The Legacy Suite: `net-tools`

* **Main Command:** `ifconfig` (Interface Configuration)
* **Package Name:** `net-tools`
* **Status:** Deprecated in most modern distributions.

### 🚀 The Modern Suite: `iproute2`

* **Main Command:** `ip`
* **Package Name:** `iproute2`
* **Status:** The current standard, installed by default.

### ❓ Why was `ifconfig` replaced?

The transition from `net-tools` to `iproute2` wasn't just for fun. There were technical reasons:

1. **Hardware Support:** New hardware, specifically high-speed **InfiniBand network adapters**, is not well supported by the old commands.
2. **Kernel Consistency:** As the Linux kernel evolved, the old commands became inconsistent in how they reported data. Fixing this was difficult due to the need for backward compatibility.

> **Note:** Even though `net-tools` is old, it is still useful to learn because you may encounter older Linux servers that have never been updated.

---

## 2. 📥 Installing Legacy Tools

If you need the old commands, you can install them manually. Here is the command to install the `net-tools` package on Ubuntu.

### 💻 Command

```bash
hashim@Hashim:~$ sudo apt install net-tools

```

### 📤 Output Explanation

When you run this, you might see output like this:

```text
net-tools is already the newest version (2.10-1.1ubuntu1.25.04.4).
Summary:                   
   Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 70

```

This output confirms that the package is installed and up to date.

---

## 3. 🔐 Understanding `sudo` (Super User Do)

You noticed the command started with `sudo`. This is one of the most important commands in Linux.

### 🛡️ What is `sudo`?

* **Meaning:** "SuperUser DO".
* **Function:** It executes a command with **root** (Administrator) privileges.
* **Requirement:** You must enter your user password to verify identity.

### ⚙️ How it Works

Not everyone can use `sudo`. A user must be listed in a special configuration file located at `/etc/sudoers`.

* **Default Behavior:** During Linux installation, the first user created is automatically added to this file.
* **Adding Users:** Administrators can add more users or groups to this list using the `visudo` command.

### ⚠️ Security Warning: Why not use Root for everything?

If `sudo` gives you full power, why not just log in as the **root** user all the time?

1. **Disaster Prevention:** A simple typo as root can delete critical system files. When running as a normal user, the system blocks these mistakes.
2. **Malware Protection:** If you accidentally run a virus or malware while logged in as root, that malware gets root access too. If you run it as a normal user, the malware is contained.
* *Fact Check:* Yes, Linux malware exists and has been around for a long time.



---

## 4. 📦 Understanding `apt` (Advanced Package Tool)

The command also used `apt`. This is the package manager for Ubuntu and Debian systems.

### 🧠 What does `apt` do?

* **Dependency Management:** In the past, installing software was hard because you had to manually find and install every library the software needed. `apt` does this automatically. It calculates dependencies and installs everything required.
* **Repositories:** It fetches these files from "repos" (online storage servers) to ensure you get safe, verified software.

### 📊 Package Management Across Distributions

Different versions of Linux (Distributions) use different file formats and tools to manage software.

| Operating System | File Format | Installation Tool(s) |
| --- | --- | --- |
| **Debian** | `.deb` | `apt`, `apt-cache`, `apt-get`, `dpkg` |
| **Ubuntu** | `.deb` | `apt`, `apt-cache`, `apt-get`, `dpkg` |
| **Red Hat / CentOS** | `.rpm` | `yum`, `rpm` |
| **SUSE** | `.rpm` | `zypper`, `rpm` |

---

## 5. 📖 Getting Help: The `man` Command

With so many new commands, you do not need to memorize everything. Linux includes a built-in manual system called `man`.

### 💻 Practical Example: The `man` Command

To read the manual for `apt`, type:

```bash
man apt
```

### 🔍 Output Explanation

The system will display a document like this:

```text
APT(8)                             APT                             APT(8)

NAME
       apt - command-line interface

SYNOPSIS
       apt [-h] [-o=config_string] [-c=config_file] [-t=target_release]
           [-a=architecture] {list | search | show | update |
           install pkg [{=pkg_version_number | /target_release}]...  |
           remove pkg...  | upgrade | full-upgrade | edit-sources |
           {-v | --version} | {-h | --help}}

DESCRIPTION
       apt provides a high-level commandline interface for the package
       management system. It is intended as an end user interface...

```

* **NAME:** Tells you what the command is.
* **SYNOPSIS:** Shows the syntax (grammar) of how to use the command options.
* **DESCRIPTION:** Explains the purpose of the tool.

> **Pro Tip:** Whenever you learn a new command, try running `man [command_name]` to see its official documentation.

---

# 🖥️ Displaying Network Interface Information in Linux

## 📘 Introduction

Checking network interface information is one of the most common tasks for a Linux user. This is especially important when your network card (host adapter) is set to configure itself automatically using protocols like **DHCP** (Dynamic Host Configuration Protocol) or **IPv6 autoconfiguration**.

In Linux, there are two ways to do this:

1. **New Systems:** Use the `ip` command.
2. **Old Systems:** Use the `ifconfig` command.

This guide focuses on the modern **`ip` command**, which allows you to view and update IP addresses, routing tables, and other network details.

---

## 🚀 The `ip` Command: Displaying Information

The `ip` command is the standard tool for managing network configurations. It is versatile and powerful.

### 1. Viewing All IP Addresses

To see the current configuration of all network interfaces on your system, use the command `ip address`.

### 💻 Command

```bash
hashim@Hashim:~$ ip address
```

### 📤 Output Analysis

When you run this command, you get detailed output about every interface. Here is the output from the example system:

```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:55:08:5a brd ff:ff:ff:ff:ff:ff
    altname enx08002755085a
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
       valid_lft 86173sec preferred_lft 86173sec

```

### 🔍 Detailed Explanation

This output describes two interfaces:

1. **Interface 1 (`lo`):**
* **Name:** `lo` stands for **Loopback**. This is a virtual interface used by the computer to talk to itself.
* **IP Address (`inet`):** `127.0.0.1`. This is the standard "home" address for the computer.
* **Status:** `<LOOPBACK,UP...>` means it is active and functioning correctly.


2. **Interface 2 (`enp0s3`):**
* **Name:** `enp0s3`. This represents the physical (or virtualized) Ethernet network card.
* **Hardware Address (`link/ether`):** `08:00:27:55:08:5a`. This is the MAC address.
* **IPv4 Address (`inet`):** `10.0.2.15/24`. This is the actual IP address assigned to the machine on the network.
* **Broadcast (`brd`):** `10.0.2.255`.
* **Scope:** `global dynamic`. This implies the IP was likely assigned automatically via DHCP.



---

## ⚡ Using Command Shortcuts (Command Completion)

The `ip` command is smart. It supports **command completion**. This means you do not have to type the full word `address`. You can type a shorter version, as long as it is unique enough for the system to understand.

Both `ip addr` and `ip ad` produce the exact same result as `ip address`.

### 💻 Command

```bash
hashim@Hashim:~$ ip addr
```

### 📤 Output

```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:55:08:5a brd ff:ff:ff:ff:ff:ff
    altname enx08002755085a
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
       valid_lft 86173sec preferred_lft 86173sec

```

This confirms that the shortened command works identically.

---

## 🧹 Filtering Output: IPv4 vs. IPv6

The standard output often shows too much information, mixing **IPv4** (standard IP addresses) and **IPv6** (newer, longer addresses). You can filter this to see exactly what you want using flags.

### 🔹 Option 1: Display Only IPv4

Add the `-4` flag to the command.

### 💻 Command

```bash
hashim@Hashim:~$ ip -4 ad
```

### 📤 Output

```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enx08002755085a
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
       valid_lft 85614sec preferred_lft 85614sec

```

**Explanation:** All `inet6` (IPv6) lines are removed. You only see the `inet` lines (127.0.0.1 and 10.0.2.15).

### 🔹 Option 2: Display Only IPv6

Add the `-6` flag to the command.

### 💻 Command

```bash
hashim@Hashim:~$ ip -6 ad
```

### 📤 Output

```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1000
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever

```

**Explanation:** The Ethernet interface (`enp0s3`) disappears completely because it does not have an IPv6 address configured in this example. Only the Loopback IPv6 address (`::1/128`) is shown.

---

## 📖 Understanding the Manual: `man ip`

To fully master the `ip` command, you should check its manual page. You can access this by typing `man ip`.

### 📜 Manual Page Preview

```text
IP(8)                               Linux                               IP(8)

NAME
       ip - show / manipulate routing, network devices, interfaces and tunnels

SYNOPSIS
       ip [ OPTIONS ] OBJECT { COMMAND | help }

       ip [ -force ] -batch filename

       OBJECT := { address | addrlabel | fou | help | ila | ioam | l2tp | link | macsec | maddress | monitor | mptcp | mroute
               | mrule | neighbor | neighbour | netconf | netns | nexthop | ntable | ntbl | route | rule | sr | tap | tcpmet‐
               rics | token | tunnel | tuntap | vrf | xfrm }

       OPTIONS := { -V[ersion] | -h[uman-readable] | -s[tatistics] | -d[etails] | -r[esolve] | -iec | -f[amily] { inet | inet6
               | link } | -4 | -6 | -B | -0 | -l[oops] { maximum-addr-flush-attempts } | -o[neline] | -rc[vbuf] [size] |
               -t[imestamp] | -ts[hort] | -n[etns] name | -N[umeric] | -a[ll] | -c[olor] | -br[ief] | -j[son] | -p[retty] }

OPTIONS
       -V, -Version
              Print the version of the ip utility and exit.

       -h, -human, -human-readable
              output statistics with human readable values followed by suffix.

```

### 🧠 How to Read This Syntax

The synopsis line `ip [ OPTIONS ] OBJECT { COMMAND | help }` tells you how to construct a command:

1. **`ip`**: The base command.
2. **`[ OPTIONS ]`**: Optional settings that change *how* the command runs.
* *Example:* `-4` (show only IPv4), `-h` (human-readable stats), `-c` (color).


3. **`OBJECT`**: The specific network component you want to manage.
* *Example:* `address` (IP addresses), `link` (network cards/cables), `route` (routing tables).


4. **`{ COMMAND }`**: What you want to do with the object.
* *Example:* `show`, `add`, `del` (delete).



**Example construction:**

* `ip` (Command)
* `-4` (Option)
* `address` (Object)
* `show` (Command - often implied if omitted)

This structure makes the `ip` command a complete toolkit for network management.


---

# 🕰️ Legacy Network Configuration: The `ifconfig` Command

## 📘 Introduction

While the modern `ip` command is the new standard, the legacy **`ifconfig`** (Interface Configuration) command is still widely recognized. It performs similar functions but operates differently under the hood.

* **The Problem with Legacy:** Old commands like `ifconfig` grew "organically." Features were added one by one over many years. This resulted in a lack of consistency; complex tasks became difficult to script or predict.
* **The Modern Solution:** The new `ip` commands were designed from the ground up to be consistent, logical, and structured.

However, because many older systems still run `ifconfig`, understanding it is a critical skill for any Linux administrator.

---

## 💻 The Command: `ifconfig`

Let's look at how to display network information using the old method.

### ⌨️ Input

Type the following in your terminal:

```bash
hashim@Hashim:~$ ifconfig
```

### 📤 Output Analysis

The output is divided into blocks, one for each network interface. Below is the detailed breakdown of the output provided in your example.

### 1️⃣ Interface: `enp0s3` (Ethernet Adapter)

This is your main network connection (likely a wired connection or a virtual machine adapter).

```text
enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
        ether 08:00:27:55:08:5a  txqueuelen 1000  (Ethernet)
        RX packets 786818  bytes 1146614516 (1.1 GB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 113030  bytes 7214154 (7.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

#### 🔍 Detailed Line-by-Line Explanation

* **Line 1: Status & Flags**
* `flags=4163`: A numeric code representing the state of the card.
* `<UP>`: The interface is active.
* `<BROADCAST>`: It can send data to all devices on the network at once.
* `<RUNNING>`: The driver is loaded and the card is ready.
* `<MULTICAST>`: It supports sending data to a specific group of devices.
* `mtu 1500`: **Maximum Transmission Unit**. The largest single packet of data (in bytes) that can be sent at once. 1500 is the standard for the internet.


* **Line 2: IPv4 Configuration**
* `inet 10.0.2.15`: This is your **IPv4 Address**.
* `netmask 255.255.255.0`: This defines the size of your network.
* `broadcast 10.0.2.255`: The address used to shout "Hello!" to every other computer on this specific network.


* **Line 3: Hardware Details**
* `ether 08:00:27:55:08:5a`: This is the **MAC Address** (Physical address). It is burnt into the hardware.
* `txqueuelen 1000`: The length of the transmission queue (buffer).


* **Lines 4-5: Receive (RX) Statistics**
* `RX packets 786818`: Total number of data packets **Received** (downloaded).
* `bytes 1146614516 (1.1 GB)`: Total amount of data downloaded.
* `RX errors 0`: Number of corrupted packets received (should be 0).
* `dropped 0`: Packets the computer received but threw away (usually because buffers were full).
* `overruns 0`: The network card received data faster than the computer could process it.


* **Lines 6-7: Transmit (TX) Statistics**
* `TX packets 113030`: Total number of packets **Transmitted** (uploaded).
* `TX errors 0`: Errors encountered while trying to send data.
* `collisions 0`: Occurs when two devices try to talk at the exact same time. On modern networks, this should be 0.



---

### 2️⃣ Interface: `lo` (Loopback)

This is the internal virtual interface used for diagnostics and internal communication.

```text
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 339  bytes 36404 (36.4 KB)
        ...

```

* **`inet 127.0.0.1`**: The universal "Home" address (localhost).
* **`inet6 ::1`**: The IPv6 version of localhost.
* **`mtu 65536`**: Loopback has a massive MTU because data never leaves the CPU, so packets can be huge without causing issues.

---

## ⚖️ Comparison: `ifconfig` vs `ip`

Why stick to the new command? Here is the breakdown:

| Feature | `ifconfig` (Legacy) | `ip` (Modern) |
| --- | --- | --- |
| **Output Format** | Slightly messy, different for every OS. | Structured, consistent, easier to parse. |
| **IPv6 Support** | Limited. Cannot filter easily (no `-6` flag). | Excellent. Can isolate `-4` or `-6` easily. |
| **Functionality** | Only handles interfaces. | Handles interfaces, routing, tunnels, and rules. |
| **Status** | Deprecated (No longer developed). | Active (Standard for all Linux systems). |

### 🛠️ Key Takeaway on Consistency

If you look at the `man` page (manual) for `ifconfig` versus `ip`, you will see that `ip` options follow a strict logic. `ifconfig` options were added randomly over 20 years, making them harder to memorize systematically.

---

# 🛣️ Displaying Routing Information in Linux

## 📘 Chapter Overview

Routing is the process of selecting a path for network traffic. In this section, we will learn how to view the **Routing Table** on a Linux system. The routing table is like a map that tells your computer where to send data packets.

We will cover:

* The **Modern** command (`ip route`).
* How the **Default Gateway** works.
* Understanding **Link-Local Addresses** (APIPA).
* The **Legacy** commands (`netstat` and `route`).

---

## 🚀 The Modern Command: `ip route`

In modern Linux systems, we use the `ip` command for almost everything. To see routing information, we use `ip route`.

### ⚡ Shortcut

You can shorten this command to just `ip r`. Both commands do exactly the same thing.

### 💻 Command Execution

```bash
hashim@Hashim:~$ ip route
default via 10.0.2.2 dev enp0s3 proto dhcp src 10.0.2.15 metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100 

```

### 🔍 Detailed Explanation of the Output

Let's break down the output line by line to understand exactly what the computer is doing.

#### 1. The Default Route

```text
default via 10.0.2.2 dev enp0s3 ...

```

* **What it is:** This is the "Default Gateway."
* **How it works:** If your computer tries to send a packet to an IP address that is **not** listed anywhere else in the routing table, it sends it here.
* **The Logic:** The routing table always looks for the "Most Specific Route" first (a route that matches the destination IP exactly). If it finds no match, it falls back to this default route (which technically represents `0.0.0.0/0`, meaning "everything else").
* **The Assumption:** Your computer assumes `10.0.2.2` is a router that knows how to forward the packet to the internet or other networks.

#### 2. The Connected Route (Local Subnet)

```text
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 ...

```

* **What it is:** This is a "Connected Route."
* **Meaning:** It tells the computer, "You are directly connected to the `10.0.2.0` network."
* **Action:** If you want to talk to another computer on this same network (e.g., `10.0.2.50`), you do not need a router. You can talk to them directly through the interface `enp0s3`.

---

## 🧩 Special Address Types Explained

The text mentions two other types of addresses you might see in a routing table, even if they aren't in the snippet above.

### 1. Link-Local Addresses (169.254.0.0/16)

You might see a route pointing to `169.254.0.0/16`.

* **Definition:** This is a **Link-Local Address (LLA)** defined by **RFC 3927**.
* **What is an RFC?** RFC stands for "Request for Comment." It is a document used by the **IETF** (Internet Engineering Task Force) to define internet standards.
* **When is it used?**
1. Your computer does not have a static IP.
2. Your computer **cannot** find a DHCP server to give it an IP.
3. As a last resort, it assigns itself an address starting with `169.254`.


* **How it works:**
* The computer picks the first two numbers (`169.254`).
* It generates the last two numbers randomly.
* It performs a check (using Ping/ARP) to make sure no one else is using that specific random address.


* **Purpose:** It allows computers on the same wire to talk to each other without a router.
* **Microsoft Name:** On Windows, this is called **APIPA** (Automatic Private Internet Protocol Addressing).

### 2. Connected Subnet Example

In some examples, you might see `192.168.122.0/24`. This is simply another example of a "Connected Route," telling the host that no routing is required for that specific range of IPs.

---

## 🏛️ The Legacy Commands: `netstat` and `route`

On older systems (or for administrators who prefer old habits), there are different ways to see this same information. The most common legacy command is `netstat`.

### 💻 Command: `netstat -rn`

* `-r`: Show **Routing** table.
* `-n`: Show **Numerical** addresses (do not try to resolve hostnames).

```bash
hashim@Hashim:~$ netstat -rn
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG        0 0          0 enp0s3
10.0.2.0        0.0.0.0         255.255.255.0   U         0 0          0 enp0s3

```

### 🔍 Output Comparison

The information is the same as `ip route`, but the format is different:

| Legacy Column | Modern Equivalent | Explanation |
| --- | --- | --- |
| **Destination 0.0.0.0** | `default` | The catch-all route. |
| **Gateway 10.0.2.2** | `via 10.0.2.2` | Where to send the traffic. |
| **Flags UG** | N/A | **U** = Up (Active), **G** = Gateway (Uses a router). |
| **Iface enp0s3** | `dev enp0s3` | The physical network card used. |

### ⚠️ The Challenge of Legacy Tools

In the old "legacy" world, you have to learn multiple different commands for similar tasks:

* `ifconfig` for interfaces.
* `netstat` for routing tables.
* `route` (another separate command) also shows routing tables.

This overlap and the need to remember different syntax for every tool is why the modern **`ip`** command is superior. It unifies everything into one consistent logic.

---

# 🌐 IPv4 Addresses and Subnet Masks: Deep Dive

## 📘 Introduction to IPv4 Addressing

In this section, we will explore IPv4 addressing in detail. An IPv4 address allows us to uniquely identify every device on a subnet. To do this, we use two components:

1. **The IP Address:** The unique ID of the device (e.g., `192.168.122.182` or your specific IP `10.0.2.15`).
2. **The Subnet Mask:** A filter that tells the computer which part of that address is the "Network" and which part is the "Host".

---

## 🧮 Practical Example: Our System's Binary Analysis
Let's analyze the output you provided:

**Our IP Information:**

* **IP Address:** `10.0.2.15`
* **Subnet Mask:** `/24` (which translates to `255.255.255.0`)

To understand how the computer sees this, we must convert your Decimal (human) numbers into Binary (machine) numbers.

### 1. Converting Your IP to Binary

An IPv4 address is split into 4 "octets" (groups of 8 bits). Each bit represents a power of 2 </br>(128, 64, 32, 16, 8, 4, 2, 1).

| Decimal Value | Calculation (Powers of 2) | Binary Result |
| --- | --- | --- |
| **10** | 8 + 2 | `00001010` |
| **0** | 0 | `00000000` |
| **2** | 2 | `00000010` |
| **15** | 8 + 4 + 2 + 1 | `00001111` |

**Your IP in Binary:**
`00001010.00000000.00000010.00001111`

### 2. Applying the Subnet Mask

Your mask is `/24`. This means the first **24 bits** are turned "ON" (set to 1). This defines your network. The remaining 8 bits are for hosts.

| Component | Decimal Format | Binary Format |
| --- | --- | --- |
| **IP Address** | `10.0.2.15` | `00001010.00000000.00000010.00001111` |
| **Subnet Mask** | `255.255.255.0` | `11111111.11111111.11111111.00000000` |

**The Result:**

* **Network Portion:** `10.0.2` (Matches the `1`s in the mask).
* **Host Portion:** `.15` (Matches the `0`s in the mask).
* **Range:** Your host address can range from `1` to `254`.

---

## ✂️ Subnetting: "Sliding the Mask"

What happens if we need a larger network? We simply "slide" the mask to the left.

In the provided text, there is an example of changing a `/24` mask to a `/20` mask.

### Comparing /24 vs /20

When we change the mask to `/20`, we use only 20 bits for the network instead of 24.

* **Mask in Binary (/20):** `11111111.11111111.11110000.00000000`
* **Mask in Decimal:** `255.255.240.0`

This small change massively increases the number of available hosts. Instead of just 254 hosts, a `/20` network can support **3,824 hosts** because it borrows extra bits from the third octet.

> **Pro Tip:** Networking professionals should always keep a calculator handy that can convert Decimal to Binary and Hexadecimal.

---

## 📢 Special-Purpose Addresses

There are specific addresses reserved for special tasks on a network.

### 1. Broadcast Addresses

The **Broadcast Address** is used to speak to *everyone* on the subnet at once. To find it, you set all the "Host" bits to `1`.

**For Your IP (`10.0.2.15/24`):**

* **Network:** `10.0.2`
* **Host Bits (All 1s):** `11111111` (which is 255)
* **Your Broadcast Address:** `10.0.2.255`

### 2. Multicast Addresses

Multicast is used to send data to a specific *group* of devices, like video screens or conference calls. These addresses usually look like `224.x.x.x`.

#### 📋 Common Multicast Addresses (Extracted from Image)

| Address | Description |
| --- | --- |
| `224.0.0.1` | All hosts on the subnet |
| `224.0.0.2` | All routers in the subnet |
| `224.0.0.12` | DHCP Servers and DHCP relay agents |
| `224.0.0.18` | Devices participating in the VRRP protocol |
| `224.0.0.102` | Devices participating in the **Hot Standby Router Protocol (HSRP)** |
| `224.0.1.1` | All **Network Time Protocol (NTP)** servers |
| `224.0.0.113` | AllJoyn hosts (used by Windows for device discovery) |

---

## 🏫 IPv4 Address Classes

Historically, IP addresses were divided into "Classes" based on their leading bits. This is often the default setting in many operating systems.

#### 📊 Address Class Table (Extracted from Image)

| Class | Leading Bits | Default Subnet Mask | First Address | Last Address | Purpose |
| --- | --- | --- | --- | --- | --- |
| **Class A** | `0` | `/8` (255.0.0.0) | `0.0.0.0` | `127.255.255.255` | Huge Networks |
| **Class B** | `10` | `/16` (255.255.0.0) | `128.0.0.0` | `191.255.255.255` | Medium Networks |
| **Class C** | `110` | `/24` (255.255.255.0) | `192.0.0.0` | `223.255.255.255` | Small Networks |
| **Class D** | `1110` | N/A | `224.0.0.0` | `239.255.255.255` | **Multicast** |
| **Class E** | `1111` | N/A | `240.0.0.0` | `255.255.255.255` | Reserved (Not in use) |

---

## 🏠 Private Addresses (RFC 1918)

These are special addresses reserved for internal use within an organization. They are safe to use because they do not exist on the public internet.

* **Class A Range:** `10.0.0.0/8` (This matches **your** current IP!)
* **Class B Range:** `172.16.0.0` to `172.31.0.0` (`/12`)
* **Class C Range:** `192.168.0.0/16`

To connect these private addresses to the internet, we use a technology called **NAT** (Network Address Translation).

---

# 🏠 Private IP Address Classes & Ranges (RFC 1918)

Hello Hashim! 👋

Private IP addresses are specific addresses that are **not routed on the public Internet**. They are exclusively used within a **Local Area Network (LAN)**, such as your home, office, or an internal organizational network.

Under the **RFC 1918** standard, these addresses are divided into three (3) specific classes.

Let's understand these in detail with a table and a comprehensive explanation.

---

## 📊 Private IP Ranges Table

| Class | CIDR (Prefix) | Range Start | Range End | Total IPs (Approx) | Where is it Used? |
| --- | --- | --- | --- | --- | --- |
| **Class A** | `/8` | `10.0.0.0` | `10.255.255.255` | 16 Million | Large Companies / Cloud (AWS/Azure) |
| **Class B** | `/12` | `172.16.0.0` | `172.31.255.255` | 1 Million | Medium Companies / Universities |
| **Class C** | `/16` | `192.168.0.0` | `192.168.255.255` | 65,536 | Home Routers / Small Offices |

---

### 1. Class A: "The Largest Range" 🏢

* **Range:** `10.0.0.0` to `10.255.255.255`
* **Mask:** `/8` (Default Subnet Mask: `255.0.0.0`)

**Detail:**
This range provides the highest number of IP addresses. This is why massive organizations and Cloud Service Providers (like AWS, Google Cloud, and Azure) utilize this range to ensure they never run out of available internal IP addresses.

> **Note for you:** Hashim, the IP address you encountered previously, `10.0.2.15`, belongs to this **Class A Private range**.

### 2. Class B: "The Confusion Point" 🏫

* **Range:** `172.16.0.0` to `172.31.255.255`
* **Mask:** The summary mask is `/12` (`255.240.0.0`).

**Pay Attention:**
Many people mistakenly believe that *any* IP starting with `172.` is a private IP. **This is incorrect.**

* `172.15.x.x` = **Public IP** (Internet routable).
* `172.16.x.x` to `172.31.x.x` = **Private IP** (Local Network use only).
* `172.32.x.x` = **Public IP**.

### 3. Class C: "Standard for Homes" 🏠

* **Range:** `192.168.0.0` to `192.168.255.255`
* **Mask:** `/16` (Default Subnet Mask: `255.255.0.0`, though it is frequently subnetted to `/24`).

**Detail:**
This is the range we encounter most frequently in our daily lives. Most home networking equipment, such as TP-Link, D-Link, and Huawei routers, use a default Gateway IP of `192.168.0.1` or `192.168.1.1`.

---

## 🛡️ What is the Benefit? (NAT)

Since these addresses cannot function directly on the public Internet, we require a technology called **NAT (Network Address Translation)**.

**How it works:**

1. You use a private IP like `192.168.1.5` on your device at home.
2. When you send a request (e.g., to open Google), your **Router** "hides" your private IP.
3. The Router communicates with Google using its **Public IP**.
4. When Google sends a reply, it sends it to the Router's Public IP.
5. The Router then hands that data back to your specific private IP (`192.168.1.5`).

This mechanism allows millions of people around the world to use the exact same Private IPs (like `192.168...`) simultaneously without causing any network conflicts! 🚀

---

# 🛠️ Assigning an IP Address to a Network Interface

## 📘 Overview

One of the most essential tasks when setting up a Linux server is assigning a **Permanent IPv4 Address**. While servers often get addresses automatically (via DHCP), a static (permanent) IP ensures the server is always reachable at the same location.

We will cover two methods:

1. **Modern Method:** Using `nmcli` (Network Manager Command Line).
2. **Legacy Method:** Editing configuration files manually.

---

## 🚀 The Modern Method: `nmcli`

On modern Linux systems, we use the **Network Manager Command Line** tool (`nmcli`). It is powerful, scriptable, and cleaner than editing files by hand.

### 1️⃣ Step 1: Identify Your Connection

First, we need to find the specific name of the network connection we want to configure.

**Command:**

```bash
hashim@Hashim:~$ sudo nmcli connection show
```

**Output:**

```text
NAME             UUID                                   TYPE      DEVICE 
netplan-enp0s3   1eef7e45-3b9d-3043-bee3-fc5925c90273   ethernet  enp0s3 
lo               1b3afd68-80a1-446d-9dfe-ad09777436dd   loopback  lo
```

* **Connection Name:** `netplan-enp0s3`
* **Device Name:** `enp0s3` (This is the physical interface).

> **Pro Tip:** You do not need to type the full name every time. You can use **Tab Completion**. Type the first few letters (e.g., `netp`) and press **Tab** to autocomplete the name. `nmcli` also accepts short commands like `con` for `connection` and `mod` for `modify`.

### 2️⃣ Step 2: Configure the Network Parameters

Now we will run a sequence of commands to set the IP, Gateway, DNS, and Addressing Mode.

#### A. Set the IP Address

We set the specific IP address and the subnet mask (using `/24` notation).

```bash
$ sudo nmcli connection modify "netplan-enp0s3" ipv4.addresses 10.0.2.22/24
```

#### B. Set the Default Gateway

This tells the server where to send traffic meant for the internet.

```bash
$ sudo nmcli connection modify "netplan-enp0s3" ipv4.gateway 10.0.2.2
```

#### C. Set the DNS Server

We configure the server to use Google's DNS (`8.8.8.8`) for resolving domain names.

```bash
$ sudo nmcli connection modify "netplan-enp0s3" ipv4.dns "8.8.8.8"
```

#### D. Set the Method to Manual

This is crucial. We must tell the system to stop looking for automatic (DHCP) addresses and use the manual static settings we just provided. Note the use of shortened commands (`con mod`).

```bash
$ sudo nmcli con mod "netplan-enp0s3" ipv4.method manual
```

### 3️⃣ Step 3: Apply the Changes

The changes are saved but not yet active. To make them "live," we must bring the connection up.

**Command:**

```bash
$ sudo nmcli connection up "netplan-enp0s3"
```

**Output:**

```text
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/5)
```

Your server now has a permanent static IP address! 🎉

---

## 🏛️ The Legacy Method: Editing Files

In older Linux distributions, network configuration was done by manually editing text files. This method is tricky because file locations and names change depending on the OS (Ubuntu vs. CentOS vs. Debian).

**⚠️ Warning:** On modern systems, this approach often fails because NetworkManager or Netplan overrides these manual file edits. This is **not backward compatible**.

### 1️⃣ Changing DNS Servers

To change where the computer looks for domain names, you edit the `resolv.conf` file.

**File Location:** `/etc/resolv.conf`

**Edit the content:**

```text
nameserver 8.8.8.8
```

### 2️⃣ Changing IP Address & Gateway

To change the interface settings, you edit the interface configuration script.

**File Location (Red Hat/CentOS style):** `/etc/sysconfig/network-scripts/ifcfg-eth0`

**Edit the content to look like this:**

```bash
DEVICE=eth0
BOOTPROTO=none         # "none" or "static" means no DHCP
ONBOOT=yes             # Start this network when computer boots
NETMASK=255.255.255.0
IPADDR=10.0.1.27
GATEWAY=10.0.2.2  # Add this if the gateway is on this interface
```

### 🔍 Comparison Summary

| Feature | Modern (`nmcli`) | Legacy (File Edit) |
| --- | --- | --- |
| **Consistency** | Same command across most modern distros. | Varies wildly (file paths differ). |
| **Safety** | Validates syntax before applying. | Typos can break networking instantly. |
| **Activation** | Immediate with `connection up`. | Requires network service restart. |
| **Compatibility** | Works on Ubuntu 20+, RHEL 8+, etc. | Mostly broken on modern systems. |

---



# 🛣️ Adding and Managing Network Routes in Linux

## 📘 Overview

This guide provides a detailed walkthrough on how to configure network routes on your Linux host. We will cover adding **temporary routes** using the `ip` command, **permanent routes** using `nmcli`, and legacy methods for older systems. Additionally, we will explore how to safely disable and enable network interfaces.

---

## 📍 Adding a Temporary Route

To add a static route that works immediately but disappears after a reboot, we use the `ip` command.

In this example, we configure the host to route traffic destined for the **10.20.20.0/24** network through the gateway **10.0.2.100**.

### 💻 Command

```bash
hashim@Hashim:~$ sudo ip route add 10.20.20.0/24 via 10.0.2.100 dev enp0s3
```

### 🔍 Detailed Command Explanation

* **`sudo`**: Executes the command with administrator (root) privileges.
* **`ip route add`**: The core command to insert a new entry into the routing table.
* **`10.20.20.0/24`**: The **Target Network**. This is the destination we want to reach.
* **`via 10.0.2.100`**: The **Gateway**. This specifies the IP address of the router that knows how to get to the destination.
* **`dev enp0s3`**: The **Device**. This explicitly forces the traffic to go out through the `enp0s3` network interface.

### 📤 Verification Output

After running the command, we verify the routing table.

```bash
hashim@Hashim:~$ ip route
default via 10.0.2.2 dev enp0s3 proto static metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.22 metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100 
10.20.20.0/24 via 10.0.2.100 dev enp0s3 
```

**Observation:** You can see the new line `10.20.20.0/24 via 10.0.2.100` is now active.

> **⚠️ Important Note:** This is a **temporary** route. If you restart the computer or the network service, this route will be deleted.

---

## 🔒 Adding a Permanent Route (Using `nmcli`)

To ensure a route survives a reboot, we use the **Network Manager Command Line** (`nmcli`) tool.

### 1️⃣ Step 1: Identify the Connection Name

First, we list the active connections to find the correct name.

```bash
hashim@Hashim:~$ sudo nmcli connection show
NAME            UUID                                  TYPE      DEVICE 
netplan-enp0s3  1eef7e45-3b9d-3043-bee3-fc5925c90273  ethernet  enp0s3 
lo              53f1ef76-bb34-4ec0-877a-735fea6ad7cd  loopback  lo     
```

* **Connection Name:** `netplan-enp0s3`

### 2️⃣ Step 2: Add the Persistent Route

We will add a route to the **10.30.30.0/24** network via the gateway **10.0.2.101**.

```bash
hashim@Hashim:~$ sudo nmcli connection modify "netplan-enp0s3" +ipv4.routes "10.30.30.0/24 10.0.2.101"
```

### 🔍 Detailed Command Explanation

* **`connection modify`**: Tells the system we are updating an existing connection.
* **`"netplan-enp0s3"`**: The target connection name we found in Step 1.
* **`+ipv4.routes`**: The `+` symbol is critical. It means "add this route to the existing list." Without the `+`, you might overwrite all existing routes.
* **`"10.30.30.0/24 10.0.2.101"`**: The format is strictly `"DESTINATION GATEWAY"`.

### 3️⃣ Step 3: Apply Changes

We must reactivate the connection for the changes to take effect.

```bash
hashim@Hashim:~$ sudo nmcli connection up "netplan-enp0s3"
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/3)
```

### 📤 Verification Output

Let's check the routing table again.

```bash
hashim@Hashim:~$ ip route
default via 10.0.2.2 dev enp0s3 proto static metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.22 metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100 
10.20.20.0/24 via 10.0.2.100 dev enp0s3 
10.30.30.0/24 via 10.0.2.101 dev enp0s3 proto static metric 100 
```

**Observation:** Both routes (the temporary `10.20...` and the permanent `10.30...`) are currently visible.

### 🔄 Testing Persistence

If we restart the network interface (or reboot), the temporary route will vanish, but the `nmcli` route will stay.

```bash
hashim@Hashim:~$ ip route
default via 10.0.2.2 dev enp0s3 proto static metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.22 metric 100 
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100 
10.30.30.0/24 via 10.0.2.101 dev enp0s3 proto static metric 100 
```

**Result:** The temporary route (`10.20.20.0`) is gone. The permanent route (`10.30.30.0`) remains.

---

## 📜 Adding a Route Using Legacy Approaches

On older Linux systems (or when `nmcli` is not available), we use different methods.

### 1️⃣ The Old Command (`route`)

To add a temporary route to **10.40.40.0/24** via **10.0.2.102**:

```bash
hashim@Hashim:~$ sudo route add -net 10.40.40.0 netmask 255.255.255.0 gw 10.0.2.102
```

### 2️⃣ Making it Permanent (Legacy Files)

Making routes permanent on old systems is complicated because the file location changes depending on the Linux distribution.

| Distribution | File Location | Configuration Line to Add |
| --- | --- | --- |
| **Debian / Ubuntu (Old)** | `/etc/network/interfaces` | `up route add -net 10.40.40.0 netmask 255.255.255.0 gw 10.0.2.102` |
| **RedHat / CentOS (Old)** | `/etc/sysconfig/network-scripts/route-enp0s3` | `10.40.40.0/24 via 10.0.2.102` |
| **Universal (Least Elegant)** | `/etc/rc.local` | `/sbin/route add -net 10.40.40.0 netmask 255.255.255.0 gw 10.0.2.102` |

> **Note on `rc.local`:** This file simply runs commands when the computer turns on. It works on almost any system, but it is considered "messy" because it is not a proper network configuration file.

---

## 🔌 Disabling and Enabling an Interface

Sometimes, for troubleshooting or initial setup, you need to turn a network interface "off" and then "on" again. This is often called "bouncing" the interface.

### 🚀 Modern Method (`ip` command)

We use the `ip link set` command.

```bash
hashim@Hashim:~$ sudo ip link set enp0s3 down
hashim@Hashim:~$ sudo ip link set enp0s3 up
```

### 🏛️ Legacy Method (`ifconfig`)

On older systems, use `ifconfig`.

```bash
hashim@Hashim:~$ sudo ifconfig enp0s3 down
hashim@Hashim:~$ sudo ifconfig enp0s3 up
```

### 🚨 Critical Warning

**Do not saw off the branch you are sitting on!**
If you are connected to the Linux machine remotely (for example, using **SSH**), disabling the network interface (`down`) will immediately disconnect you. You will lose control of the server and will not be able to send the `up` command to reconnect. Always be careful when modifying active interfaces remotely.

---

# 📦 Setting the MTU on a Network Interface

## 📘 Overview: What is MTU?

In modern networking, a common configuration task is setting the **MTU** (Message Transfer Unit).

* **Definition:** MTU is the size of the largest **Protocol Datagram Unit** (PDU)—often called a **frame**—that a network interface can send or receive.
* **Standard Size:** On standard Ethernet networks, the default MTU is **1,500 bytes**. This means the maximum size of a single packet is 1,500 bytes.
* **MSS:** The maximum packet size for a specific type of media is often referred to as the **Maximum Segment Size** (MSS).

---

## 📊 Understanding Frame Sizes

Different network scenarios require different packet sizes. The table below illustrates the relationship between frame size, MTU, and usage.

| Parameter | Standard Value | Description |
| --- | --- | --- |
| **MTU** | 1,500 Bytes | The default payload size for standard Ethernet. |
| **Jumbo Frame** | ~9,000 Bytes | Used for high-performance data center traffic to reduce overhead. |
| **Small Frame** | < 1,500 Bytes | Used for Tunnels, VPNs, or Satellite links where extra headers take up space. |

### ❓ Why Would We Need to Change This?

The standard **1,500-byte** size is a widely accepted compromise. It is small enough that transmission errors are detected quickly, and re-sending lost data doesn't take much time. However, specific use cases require adjustments:

#### 1. 🚀 Increasing MTU (Jumbo Frames)

In data centers, larger packets allow servers to send more data with less CPU processing (overhead).

* **Target MTU:** ~9,000 bytes (Jumbo Packet).
* **Network Speed:** Used on 1 Gbps, 10 Gbps, or faster connections.
* **Use Cases:**
* Storage traffic (e.g., iSCSI).
* System Backups.
* Virtual Machine migration (VMware vMotion, Hyper-V Live Migration).



#### 2. 📉 Decreasing MTU (Small Frames)

Sometimes, packets must be smaller than 1,500 bytes.

* **The Problem:** Many applications set a **DF (Don't Fragment)** flag on their packets. If they send a 1,500-byte packet across a link that only supports 1,380 bytes (due to overhead), the packet is dropped, and the application crashes or fails silently.
* **Use Cases:**
* **VPNs & Tunnels:** Wrapping a packet inside another packet (encapsulation) adds extra headers, leaving less room for the actual data.
* **Satellite Links:** These often use very small frames (e.g., 512 bytes).



---

## 🛠️ Configuration Example: Setting MTU to 9000

We will now configure your specific connection (`netplan-enp0s3`) to use **Jumbo Frames** (MTU 9000). We will use the **Network Manager Command Line** (`nmcli`) tool.

### 1️⃣ Step 1: Modify the Connection

We verify the connection name and modify the `802-3-ethernet.mtu` setting.

**Command:**

```bash
hashim@Hashim:~$ sudo nmcli connection modify "netplan-enp0s3" 802-3-ethernet.mtu 9000
```

**Explanation:**

* `connection modify`: Tells Network Manager to update an existing profile.
* `"netplan-enp0s3"`: The specific connection profile we are editing.
* `802-3-ethernet.mtu 9000`: Sets the MTU property for Ethernet to 9000 bytes.

### 2️⃣ Step 2: Apply the Changes

Changes in `nmcli` are saved to the configuration file but are not active until the connection is reloaded.

**Command:**

```bash
hashim@Hashim:~$ sudo nmcli connection up "netplan-enp0s3"
```

**Output:**

```text
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/7)

```

### 3️⃣ Step 3: Verify the Change

We use the `ip` command to confirm the interface is actually using the new size.

**Command:**

```bash
hashim@Hashim:~$ ip ad | grep mtu
```

**Output:**

```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9000 qdisc fq_codel state UP group default qlen 1000

```

**Analysis:**
Notice that `enp0s3` now shows **`mtu 9000`**. The configuration was successful.

---

## ⚡ Advanced: Using `nmcli` Interactive Mode

The `nmcli` tool includes a powerful "interactive mode" (a shell) that lets you view and edit settings without typing long commands repeatedly.

### 1️⃣ Entering the Shell & Viewing Properties

To start editing, use the `connection edit` command. Once inside, you can type `print` to see **every single detail** of the connection.

**Command:**

```bash
hashim@Hashim:~$ sudo nmcli connection edit "netplan-enp0s3"
```

**Output & Interaction:**

```text
===| nmcli interactive connection editor |===

Editing existing '802-3-ethernet' connection: 'netplan-enp0s3'

Type 'help' or '?' for available commands.
Type 'print' to show all the connection properties.
Type 'describe [<setting>.<prop>]' for detailed property description.

You may edit the following settings: connection, 802-3-ethernet (ethernet), 802-1x, dcb, sriov, ethtool, match, ipv4, ipv6, hostname, link, tc, proxy
nmcli> print

```

**Full Connection Details:**

```text
===============================================================================
                  Connection profile details (netplan-enp0s3)
===============================================================================
connection.id:                          netplan-enp0s3
connection.uuid:                        1eef7e45-3b9d-3043-bee3-fc5925c90273
connection.stable-id:                   --
connection.type:                        802-3-ethernet
connection.interface-name:              enp0s3
connection.autoconnect:                 yes
connection.autoconnect-priority:        0
connection.autoconnect-retries:         -1 (default)
connection.multi-connect:               0 (default)
connection.auth-retries:                -1
connection.timestamp:                   1767873502
connection.permissions:                 --
connection.zone:                        --
connection.controller:                  --
connection.master:                      --
connection.slave-type:                  --
connection.port-type:                   --
connection.autoconnect-slaves:          -1 (default)
connection.autoconnect-ports:           -1 (default)
connection.down-on-poweroff:            -1 (default)
connection.secondaries:                 --
connection.gateway-ping-timeout:        0
connection.ip-ping-timeout:             0
connection.ip-ping-addresses:           --
connection.ip-ping-addresses-require-all:-1 (default)
connection.metered:                     unknown
connection.lldp:                        default
connection.mdns:                        -1 (default)
connection.llmnr:                       -1 (default)
connection.dns-over-tls:                -1 (default)
connection.mptcp-flags:                 0x0 (default)
connection.wait-device-timeout:         -1
connection.wait-activation-delay:       -1
-------------------------------------------------------------------------------
802-3-ethernet.port:                    --
802-3-ethernet.speed:                   0
802-3-ethernet.duplex:                  --
802-3-ethernet.auto-negotiate:          no
802-3-ethernet.mac-address:             --
802-3-ethernet.cloned-mac-address:      --
802-3-ethernet.generate-mac-address-mask:--
802-3-ethernet.mac-address-denylist:    --
802-3-ethernet.mtu:                     9000
802-3-ethernet.s390-subchannels:        --
802-3-ethernet.s390-nettype:            --
802-3-ethernet.s390-options:            --
802-3-ethernet.wake-on-lan:             --
802-3-ethernet.wake-on-lan-password:    --
802-3-ethernet.accept-all-mac-addresses:-1 (default)
-------------------------------------------------------------------------------
ipv4.method:                            auto
ipv4.dns:                               8.8.8.8
ipv4.dns-search:                        --
ipv4.dns-options:                       --
ipv4.dns-priority:                      0
ipv4.addresses:                         10.0.2.22/24
ipv4.gateway:                           10.0.2.2
ipv4.routes:                            { ip = 10.30.30.0/24, nh = 10.0.2.101 }
ipv4.route-metric:                      -1
ipv4.route-table:                       0 (unspec)
ipv4.routing-rules:                     --
ipv4.replace-local-rule:                -1 (default)
ipv4.dhcp-send-release:                 -1 (default)
ipv4.routed-dns:                        -1 (default)
ipv4.ignore-auto-routes:                no
ipv4.ignore-auto-dns:                   no
ipv4.dhcp-client-id:                    --
ipv4.dhcp-iaid:                         --
ipv4.dhcp-dscp:                         --
ipv4.dhcp-timeout:                      0 (default)
ipv4.dhcp-send-hostname-deprecated:     yes
ipv4.dhcp-send-hostname:                -1 (default)
ipv4.dhcp-hostname:                     --
ipv4.dhcp-fqdn:                         --
ipv4.dhcp-hostname-flags:               0x0 (none)
ipv4.never-default:                     no
ipv4.may-fail:                          yes
ipv4.required-timeout:                  -1 (default)
ipv4.dad-timeout:                       -1 (default)
ipv4.dhcp-vendor-class-identifier:      --
ipv4.dhcp-ipv6-only-preferred:          -1 (default)
ipv4.link-local:                        0 (default)
ipv4.dhcp-reject-servers:               --
ipv4.auto-route-ext-gw:                 -1 (default)
ipv4.shared-dhcp-range:                 --
ipv4.shared-dhcp-lease-time:            0 (default)
-------------------------------------------------------------------------------
ipv6.method:                            disabled
ipv6.dns:                               --
ipv6.dns-search:                        --
ipv6.dns-options:                       --
ipv6.dns-priority:                      0
ipv6.addresses:                         --
ipv6.gateway:                           --
ipv6.routes:                            --
ipv6.route-metric:                      -1
ipv6.route-table:                       0 (unspec)
ipv6.routing-rules:                     --
ipv6.replace-local-rule:                -1 (default)
ipv6.dhcp-send-release:                 -1 (default)
ipv6.routed-dns:                        -1 (default)
ipv6.ignore-auto-routes:                no
ipv6.ignore-auto-dns:                   no
ipv6.never-default:                     no
ipv6.may-fail:                          yes
ipv6.required-timeout:                  -1 (default)
ipv6.ip6-privacy:                       -1 (default)
ipv6.temp-valid-lifetime:               0 (default)
ipv6.temp-preferred-lifetime:           0 (default)
ipv6.addr-gen-mode:                     default-or-eui64
ipv6.ra-timeout:                        0 (default)
ipv6.mtu:                               auto
ipv6.dhcp-pd-hint:                      --
ipv6.dhcp-duid:                         --
ipv6.dhcp-iaid:                         --
ipv6.dhcp-timeout:                      0 (default)
ipv6.dhcp-send-hostname-deprecated:     yes
ipv6.dhcp-send-hostname:                -1 (default)
ipv6.dhcp-hostname:                     --
ipv6.dhcp-hostname-flags:               0x0 (none)
ipv6.auto-route-ext-gw:                 -1 (default)
ipv6.token:                             --
-------------------------------------------------------------------------------
proxy.method:                           none
proxy.browser-only:                     no
proxy.pac-url:                          --
proxy.pac-script:                       --
-------------------------------------------------------------------------------

```

### 2️⃣ Modifying Settings Interactively

In this session, we will:

1. **Revert** the MTU back to `auto`.
2. **Manually set** a new IP, Gateway, and DNS.

**Interactive Session:**

```bash
nmcli> set 802-3-ethernet.mtu auto
nmcli> set ipv4.addresses 10.0.2.23/24
Do you also want to set 'ipv4.method' to 'manual'? [yes]: 
nmcli> set ipv4.gateway 10.0.2.2
nmcli> set ipv4.dns 8.8.8.8
nmcli> save
Connection 'netplan-enp0s3' (1eef7e45-3b9d-3043-bee3-fc5925c90273) successfully updated.
nmcli> quit
```

**Step-by-Step Logic Explanation:**

1. **`set 802-3-ethernet.mtu auto`**: This command removes the hardcoded 9000 value, allowing the system to negotiate the default MTU (usually 1500).
2. **`set ipv4.addresses 10.0.2.23/24`**: We assign a new Static IP (`.23`).
3. **The Prompt (`[yes]`):** The `nmcli` tool is smart. It sees you are adding a static IP, so it asks if you want to switch the method from `auto` (DHCP) to `manual`. Pressing **Enter** accepts the default "Yes".
4. **`set ipv4.gateway` & `dns**`: We define the router and Google DNS so the machine can surf the web.
5. **`save`**: Commits the changes to the disk.
6. **`quit`**: Exits the shell.

This interactive mode is ideal for scripting, allowing administrators to push complex network changes to thousands of stations efficiently.


---


Here is the professional README documentation for the specific task of removing the IP address `10.0.2.23`.

---

# 🗑️ Removing a Specific Static IP Address

This guide documents the precise steps to clean up your network configuration by removing an unwanted Static IP address. In this specific scenario, we are removing the secondary IP address **`10.0.2.23/24`** from the `netplan-enp0s3` connection using the **Network Manager CLI (nmcli)** interactive mode.

## 📋 Prerequisites

* **Operating System:** Ubuntu Linux (or any distribution using Network Manager).
* **Access:** You must have `sudo` (administrative) privileges.
* **Tool:** We will use the `nmcli` interactive editor for safety and precision.

---

## 🛠️ Step-by-Step Implementation

Follow these steps to safely remove the IP address without disrupting other configurations.

### 1. Check Current IP Status

Before making any changes, it is best practice to verify which IP addresses are currently assigned to your interface.

**Command:**

```bash
ip -4 ad

```

**Explanation:**

* **`ip`**: The main command for network monitoring.
* **`-4`**: Filters the output to show only IPv4 addresses (hides complicated IPv6 details).
* **`ad`**: Short for `address`, listing the IP details.
* **Output Analysis:** Look for `10.0.2.23/24` in the list. It might be listed as `secondary`.

---

### 2. Enter the Interactive Editor

Instead of typing complex long commands, we enter the `nmcli` interactive shell. This allows us to see exactly what we are changing.

**Command:**

```bash
sudo nmcli connection edit "netplan-enp0s3"

```

**Explanation:**

* **`sudo`**: Grants permission to modify system network settings.
* **`connection edit`**: Opens the configuration menu for a specific connection.
* **`"netplan-enp0s3"`**: The specific name of the connection profile we are modifying.

---

### 3. Verify Settings Before Deletion

Once inside the editor (you will see the `nmcli>` prompt), check the list of currently assigned IP addresses to ensure you target the correct one.

**Command:**

```bash
nmcli> print ipv4

```

**Explanation:**

* **`print ipv4`**: Displays all IPv4-related settings.
* **Target:** You should see `ipv4.addresses: 10.0.2.22/24, 10.0.2.23/24` (or similar).

---

### 4. Remove the Unwanted IP (`10.0.2.23`)

Now, we execute the removal command. This command surgically removes only the specific IP you type, leaving other IPs (like `.22`) untouched.

**Command:**

```bash
nmcli> remove ipv4.addresses 10.0.2.23/24

```

**Explanation:**

* **`remove`**: The action to delete a value from a list.
* **`ipv4.addresses`**: The specific setting field we are modifying.
* **`10.0.2.23/24`**: The exact value we want to delete.

> **Note:** If the system asks: *"Do you also want to set 'ipv4.method' to 'manual'? [yes]:"*, simply press **Enter**. This confirms that you still want to manage IPs manually.

---

### 5. Save and Exit

The changes are currently only in temporary memory. You must save them to the configuration file.

**Commands:**

```bash
nmcli> save
nmcli> quit

```

**Explanation:**

* **`save`**: writes the changes to the persistent connection file on the disk.
* **`quit`**: Exits the interactive `nmcli>` shell and returns you to the standard terminal.

---

### 6. Apply Changes (Restart Connection)

Linux often caches (remembers) old IP addresses even after you change the settings file. To force the system to drop the old IP (`10.0.2.23`), you must fully restart the connection.

**Commands:**

```bash
sudo nmcli connection down "netplan-enp0s3"
sudo nmcli connection up "netplan-enp0s3"

```

**Explanation:**

* **`down`**: Completely deactivates the interface, flushing out all current IP addresses.
* **`up`**: Reactivates the interface, loading *only* the new configuration (without the deleted IP).

---

### 7. Final Verification

Confirm that the operation was successful and the IP address `10.0.2.23` is gone.

**Command:**

```bash
ip -4 ad

```

**Expected Result:**
You should no longer see `10.0.2.23` in the output. The interface should now only show your remaining Primary IP (e.g., `10.0.2.22`) and the Loopback address.

---

### 🎯 Success!

You have successfully removed the specific static IP address while maintaining your network configuration.

---


