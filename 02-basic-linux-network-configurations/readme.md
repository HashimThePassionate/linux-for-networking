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