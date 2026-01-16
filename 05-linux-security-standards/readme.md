# 🛡️ Linux Security Standards

<details>
<summary><strong>Table of Contents</strong></summary>

- [Section Objectives](#section-objectives)
- [Technical Requirements](#technical-requirements)
- [Securing Linux Hosts](#securing-linux-hosts)
	- [Why Do I Need to Secure My Linux Hosts?](#why-do-i-need-to-secure-my-linux-hosts)
	- [The Auto-Update Process](#the-auto-update-process)
	- [Enterprise Management: Manual vs. Automatic](#enterprise-management-manual-vs-automatic)
	- [The Manual Update Commands](#the-manual-update-commands)
- [Cloud-Specific Security Considerations](#cloud-specific-security-considerations)
	- [The Update Problem (Stale Images)](#the-update-problem-stale-images)
	- [Host Firewalls & The "Ping" Problem](#host-firewalls--the-ping-problem)
	- [Remote Access (SSH) Exposure](#remote-access-ssh-exposure)
- [Commonly Encountered Industry-Specific Security Standards](#commonly-encountered-industry-specific-security-standards)
- [The Center for Internet Security (CIS) Critical Controls](#the-center-for-internet-security-cis-critical-controls)
	- [The Three Implementation Groups (IGs)](#the-three-implementation-groups-igs)
	- [The 18 CIS Critical Controls (Version 8)](#the-18-cis-critical-controls-version-8)
- [Getting a Start on CIS Critical Security Controls 1 and 2](#getting-a-start-on-cis-critical-security-controls-1-and-2)
	- [Critical Control 1: Hardware Inventory](#critical-control-1-hardware-inventory)
	- [Critical Control 2 – Software Inventory](#critical-control-2--software-inventory)
- [OSQuery (Advanced Inventory & Security)](#osquery-advanced-inventory--security)
- [Applying a CIS Benchmark: Securing SSH on Linux](#applying-a-cis-benchmark-securing-ssh-on-linux)
	- [Deep Dive 1: Disable Root Login (5.2.9)](#deep-dive-1-disable-root-login-529)
	- [Deep Dive 2: Ensure Strong Ciphers (5.2.12)](#deep-dive-2-ensure-strong-ciphers-5212)

</details>

Welcome to the comprehensive guide on Linux Security Standards. This section establishes the "big picture" of security, exploring why Linux hosts—regardless of their environment—require continuous care and maintenance immediately following installation and throughout their entire lifecycle.

---

## 📖 Section Objectives

We will navigate through the critical reasons and methodologies for securing Linux systems. The following key topics are covered in this section:

* ❓ **The Necessity of Security:** Why do I need to secure my Linux hosts?
* ☁️ **Cloud Considerations:** Specific security considerations for cloud environments.
* 🏭 **Industry Standards:** Commonly encountered industry-specific security standards.
* 🛡️ **CIS Controls:** The Center for Internet Security (CIS) Critical Controls.
* 📊 **CIS Benchmarks:** The Center for Internet Security (CIS) Benchmarks.
* 🔒 **Access Control:** Deep dive into SELinux and AppArmor.

---

## 🛠️ Technical Requirements

While this section covers a broad range of theoretical topics, the practical implementation will focus specifically on **hardening the SSH (Secure Shell) service**.

### 💻 Environment Setup

* **Primary System:** We will use the current Linux host or a Virtual Machine (VM).
* **Optional Testing:** As with previous sections, having a **second host** available to test changes and connectivity is beneficial, though it is not strictly required to follow the examples.

---

# 🔒 Securing Linux Hosts

## 📘 Why Do I Need to Secure My Linux Hosts?

Like almost every other operating system, a standard Linux installation is designed to be **streamlined and easy**. The goal is to get the user up and running with as few errors as possible.

However, this ease of use comes at a cost:

* **No Firewall:** As seen in previous chapters, fresh installations often have no firewall enabled by default.
* **Outdated Software:** The version of the operating system and its packages match the **installation media** (the ISO file), not the latest secure versions available online.
* **Default Settings:** Default configurations are often set for compatibility, not security.

To remedy this, the industry relies on legislation, regulations, and security recommendations to harden these default states.

---

## 🔄 The Auto-Update Process

Luckily, most modern Linux distributions (like Ubuntu) have an **auto-update process** enabled by default to handle initial security patches.

### 📂 Configuration File Location

This behavior is controlled by a specific configuration file:
`/etc/apt/apt.conf.d/20auto-upgrades`

### 📝 The Configuration Lines

Inside this file, you will typically see two lines:

```bash
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

### 🔍 Detailed Explanation

* **`Update-Package-Lists "1"`**: This setting controls whether the system automatically checks for new software lists (like checking a menu for new items).
* **`Unattended-Upgrade "1"`**: This setting turns the actual automatic installation on or off.
* **Value `"1"**`: Enabled (Default).
* **Value `"0"**`: Disabled.

> **Note:** The `Unattended-Upgrade` setting usually only applies to **security updates**, not full feature upgrades. This "cruise control" setting is generally fine for personal desktops or non-critical servers.

---

## 🏢 Enterprise Management: Manual vs. Automatic

In a well-managed corporate environment, relying on "unattended upgrades" is risky. An automatic update could break a critical application while no one is watching.

### 🏗️ The Maintenance Window Strategy

Instead of auto-updates, administrators use **Scheduled Maintenance Windows**:

1. **Test:** Upgrades are first applied to non-critical (test/dev) servers.
2. **Verify:** The team ensures nothing broke.
3. **Deploy:** Updates are applied to important production hosts.

In this scenario, you would set the auto-update configuration values to **"0"** and use manual commands.

---

## 🛠️ The Manual Update Commands

For Ubuntu (and Debian-based systems), the manual update process involves two distinct steps.

### 1️⃣ Step 1: Update the Lists

This command does **not** install new software. It simply contacts the online repositories to download the latest list of available packages and versions.

**Command:**

```bash
sudo apt-get update
```

### 2️⃣ Step 2: Upgrade the Software

This command compares your installed software against the new list (from Step 1) and installs the newer versions.

**Command:**

```bash
sudo apt-get upgrade
```

### ⚡ Combining Commands

You can run both steps in a single line using the `&&` operator.

**Command:**

```bash
sudo apt-get update && sudo apt-get upgrade
```

### 🔍 Detailed Explanation of `&&`

The `&&` (AND) operator is a logical tool in Linux:

1. It executes the **first** command (`update`).
2. It checks if the first command finished successfully (Return Code 0).
3. **Only then** does it execute the **second** command (`upgrade`).

If the update fails (e.g., no internet), the upgrade will never attempt to run.

> **User Interaction:** During the upgrade step, you may be prompted to approve the download size (Yes/No) or make decisions if a package's configuration file has changed significantly.

---

## ☁️ Cloud vs. Data Center

You might ask, "My servers are in the cloud (AWS, Azure, Google Cloud). Are they safe?"

**The Reality:** Linux is Linux, no matter where it is installed.

* **Cloud Instances:** Sometimes, cloud templates are *less* secure than a custom-built data center template because they are optimized for generic use.
* **Responsibility:** Security updates remain a critical part of your security program, regardless of the deployment location.

---

# ☁️ Cloud-Specific Security Considerations

## 📘 Overview

When you create (spin up) **Virtual Machines (VMs)** in major cloud environments (like AWS, Azure, or Google Cloud) using their **default images**, there are specific security risks you must address immediately.

Do not assume a cloud server is secure just because it is new. You must verify updates, firewalls, and access rules yourself.

---

## 🔄 1. The Update Problem (Stale Images)

### ⚠️ The Reality of Cloud Images

* **Auto-Updates vary:** Some cloud providers enable automatic updates by default, but others do not.
* **Outdated by Definition:** Every operating system image (snapshot) is **always** somewhat out of date. The moment an image is created, it stops receiving updates until you launch it.

### 🛠️ The Necessary Action

As soon as you spin up a new VM, your first task must be to update it, exactly as you would for a physical computer in your office.

### 💻 Practical Example: Updating a Fresh Cloud VM

If you launch an Ubuntu instance, run this command immediately to fix security holes:

**Command:**

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### 🔍 Detailed Explanation

1. **`sudo`**: Run as administrator.
2. **`apt-get update`**: Download the latest list of package versions.
3. **`&&`**: Run the second command only if the first one succeeds.
4. **`apt-get upgrade`**: Install the new versions.
5. **`-y`**: Automatically answer "Yes" to prompts (crucial for automation scripts).

---

## 🛡️ 2. Host Firewalls & The "Ping" Problem

### 🚧 Default Restrictions

Most cloud service images come with a **Host Firewall** enabled. Usually, this firewall is set to a **Restrictive Mode** (blocking most traffic).

### 🔍 The "Ping" Test Failure

A common point of confusion for new administrators is trying to `ping` their new server to see if it is online.

* **Expectation:** You ping the server IP, and it replies.
* **Reality:** The ping fails (Request Timed Out).
* **Reason:** The host firewall (inside the VM) or the Cloud Security Group (outside the VM) is blocking **ICMP** (Internet Control Message Protocol).

### 🛠️ Verification Steps

Before troubleshooting network connectivity, you must check the internal firewall configuration. Remember to check **both** types of firewall tools, as discussed in previous chapters:

1. **Check `iptables`:**
```bash
sudo iptables -L -n -v
```


2. **Check `nftables`:**
```bash
sudo nft list ruleset
```



---

## 🔓 3. Remote Access (SSH) Exposure

### ⚠️ The "Open Door" Default

Many default cloud images (or the setup wizards used to create them) automatically create a rule to allow **Remote Administrative Access**.

* **Protocol:** SSH (Secure Shell).
* **Port:** TCP/22.
* **Source:** **The Public Internet (`0.0.0.0/0`)**.

### 🚨 Why is this bad?

While this makes it easy for you to connect immediately, it also allows **every hacker on the internet** to try and connect to your server. Even if you have a strong password, your server will be bombarded with login attempts.

### 🛡️ Best Practice

Always check your security groups or firewall rules. **Restrict SSH access** so that only **your specific IP address** (or your office VPN IP) can connect.

---

## 🏭 4. Cloud "Services" vs. Server Instances

### ☁️ Understanding Managed Services

Often, you will use a **Cloud Service** instead of a raw Server Instance.

* **Example:** A **Serverless Database** (like Amazon RDS or Azure SQL).

### ⚖️ The Trade-off

1. **Your Control:** You have full control over the database (creating tables, users, and data).
2. **Hidden Infrastructure:** The actual server hosting the database is **not visible** to you. You cannot SSH into it or check its OS version.

### 🏢 Shared Infrastructure

In these serverless or managed scenarios:

* The underlying server might be **dedicated** to you (Single Tenant).
* More likely, it is **shared** across multiple organizations (Multi-Tenant).

This means you rely entirely on the Cloud Provider to handle the OS security, updates, and hardware isolation for that specific service.


---

# 🛡️ Commonly Encountered Industry-Specific Security Standards

## 📘 Overview

There is a wide variety of guidance and regulatory requirements designed for specific industries. Even if you do not work in these specific fields, you may still recognize many of them. Because they are tailored to specific sectors, we will describe them at a high level. However, keep in mind that each of these standards is complex enough to fill entire books on its own.

---

## 🌍 Privacy Legislation

This section outlines the key regulations that govern how personal data is protected in different regions of the world.

### 🇪🇺 GDPR (General Data Protection Regulation)

* **Region:** European Union
* **Unique Feature:** This legislation includes **"the right to be forgotten."** This means vendors who must follow GDPR are required to provide a method to securely delete a person's private information upon request.
* **Complexity:** This regulation is notable for being both complete and very complex. It was passed in 2016, but even as of 2021, the specific details and implications are not fully interpreted for every situation.

### 🇨🇦 PIPEDA (Personal Information Protection and Electronic Documents Act)

* **Region:** Canada
* **Function:** Like many other jurisdictions, this legislation governs how personal information is used, stored, protected, deleted, and sometimes sold.
* **Note on the US:** While many regions have privacy laws (like the two listed here), the **United States** is notable because it currently does not have any single federal (national) privacy regulation.

---

## 🔐 Security Standards

This section details the various standards created by industries and governments to ensure information security.

### 💳 PCI-DSS (Payment Card Industry Data Security Standard)

* **Target Audience:** This applies to you if you handle credit cards or work in the financial sector.
* **Focus:** Its primary goal is the security of cardholder data.
* **Reputation:** It is often referred to as a "lowest common denominator" standard, meaning it sets the basic baseline for security.

### 🏥 HIPAA (Health Information Portability and Accountability Act)

* **Target Audience:** This standard applies strictly to the healthcare sector.
* **Focus:** It focuses on protecting **PII** (Personally Identifiable Information) and data specific to healthcare operations.

### 🏛️ NIST-800 Series (National Institute for Standards and Technology)

* **Origin:** NIST is a US Government agency that publishes standards for government departments.
* **The 800 Series:** This specific series of documents defines information security and physical security requirements.
* **Adoption:** These standards are so comprehensive that many **private sector** organizations choose to use them voluntarily. Additionally, private companies doing federal contract work may be legally mandated to comply with them.

### ☁️ FedRAMP (Federal Risk and Authorization Management Program)

* **Focus:** This set of standards specifically governs the security of **cloud-based** products and services intended for use by US Government agencies.

### 🛡️ DISA STIGs (Defense Information Systems Agency Security Technical Implementation Guides)

* **Target Audience:** These are created exclusively for products and systems used in the **military**, covering several Linux distributions.
* **Key Difference:** While other standards focus on the *end goal* (being secure), DISA STIGs are different. They are **prescriptive guides** that tell you exactly which specific settings and configurations to use.

---

## 🤝 The Common Ground: CIS Controls

While every standard listed above has a specific industry focus, the underlying security recommendations are often very similar.

When there is no specific regulation providing good security guidance, organizations often turn to the **Center for Internet Security (CIS)** "critical controls." These controls are frequently used alongside regulatory requirements to create a stronger overall security posture.

---

# 🛡️ The Center for Internet Security (CIS) Critical Controls

## 📘 Overview

While the CIS critical controls aren't standards for compliance, they are certainly an excellent foundation and a good working model for any organization. The critical controls are very practical in nature – rather than being compliance-driven, they are focused on real-world attacks and defending against them.

The understanding is that if you focus on the controls, in particular, if you focus on them in order, then your organization will be well defended against the more common attacks seen "in the wild."

**The Logical Order:**

* You can't secure your hosts (**#3**) unless you know what hosts are on your network (**#1**).
* Logging (**#8**) isn't effective without an inventory of hosts and applications (**#2** and **#3**).

As an organization works its way down the list, it quickly reaches the objective of not being the "slowest gazelle in the herd."

**Volunteer Maintenance:**
As with the CIS benchmarks, the critical controls are authored and maintained by volunteers. They are also revised over time (currently Version 8, released in 2021) to address new threats, tools, and malware methods.

---

## 🏗️ The Three Implementation Groups (IGs)

The critical controls are broken into three groups to help organizations prioritize based on size and resources.

### 🔹 Implementation Group 1 (IG1) – Basic Controls

* **Target:** Smaller IT groups and organizations using commercial/off-the-shelf hardware and software.
* **Goal:** These controls are where organizations normally start. If these are all in place, then you can have some assurance that your organization is no longer the "slowest gazelle in the herd."

### 🔹 Implementation Group 2 (IG2) – Medium-Sized Enterprises

* **Target:** Larger organizations where there is a single person or a small group responsible for information security, or organizations with regulatory compliance requirements.
* **Goal:** Expands on IG1 by adding technical guidance for more specific configurations and technical processes.

### 🔹 Implementation Group 3 (IG3) – Larger Enterprises

* **Target:** Large environments with established security teams and processes.
* **Goal:** Includes advanced governance, such as policies for incident response, incident management, penetration tests, and red team exercises.
* **Note:** Each group is a super-set of the previous, so IG3 includes everything in IG1 and IG2.

---

## 📋 The 18 CIS Critical Controls (Version 8)

### Control 01: Inventory and Control of Hardware Assets

* **Action:** Actively inventory and manage all hardware devices on the network. This includes scanning the network to update the inventory.
* **Access Rights:** Assets should be given different access rights depending on whether they are managed, unmanaged, inventoried, or not.

### Control 02: Inventory and Control of Software Assets

* **Action:** In addition to hardware, it is critical to inventory software.
* **Policy:** Only software that is authorized should be installed or permitted to execute.

### Control 03: Data Protection

* **Challenge:** Often one of the hardest tasks for organizations.
* **Process:** Covers technical controls to classify data, handle it securely (knowing who has rights to it), retain it, and dispose of it based on a defined life cycle.
* **Privilege Management:** It is common (and risky) for most employees to have full read/write/delete rights to critical data; this control aims to limit that.

### Control 04: Secure Configuration of Assets, Network Infrastructure, and Applications

* **Action:** Establish a secure configuration standard for all assets and apply them (often based on industry recommendations).
* **Goal:** Configure systems as securely as possible to prevent attackers or malware from exploiting vulnerable settings or services.

### Control 05: Account Management

* **Standards:** Establish standards for user account creation and robust processes to retire/delete unused accounts.
* **Monitoring:** Monitor unused accounts and maintain strict processes for assigning group memberships, especially regarding administrative rights.

### Control 06: Access Control Management

* **Process:** Defines tool processes to manage authorizations/privileges for users, devices, and applications.
* **Recommendation:** **Multi-factor authentication (MFA)** is specifically recommended for external services, remote access, and administrative access.

### Control 07: Continuous Vulnerability Management

* **Operational Perspective:** Beyond just scanning for vulnerabilities, this requires automation to apply timely updates and patches to all OSs and applications.
* **Intelligence:** Includes monitoring industry news to understand new attacks/vulnerabilities relevant to the organization.

### Control 08: Audit Log Management

* **Action:** Centrally and locally collect and manage logs to help detect, understand, and recover from attacks.
* **Automation:** Essential because logs grow large quickly. Manual review is impossible; tools must filter normal events and alert on potential compromises.

### Control 09: Email and Web Browser Protections

* **Context:** Email (malicious docs/links) and browsers are the primary points of compromise.
* **Defense:** Tools must be in place to ensure these links never arrive or are "de-fanged" before reaching the user.

### Control 10: Malware Defenses

* **Scope:** More than just 1990s "antivirus." Includes policies preventing script execution by non-admins and restricting USB storage.
* **Detection Strategy:** Must detect exploitation behavior, not just "known bad" signatures, as there is too much malware to rely on lists alone.

### Control 11: Data Recovery

* **Modern Approach:** More than just "backups." It involves restricting local data on workstations so they can be re-imaged immediately if infected.
* **Server Strategy:** Servers are backed up as "images" to allow recovery in minutes rather than days.
* **Requirement:** Must have tested, rapid recovery procedures and know when the last "known good" version existed (tying into detection in Control #10).

### Control 12: Network Infrastructure Management (802.1x)

* **Focus:** Secure configuration of physical, virtual, and cloud network infrastructure (routers, switches, firewalls).
* **Tools:** Includes appropriate use of **ACLs (Access Control Lists)** and network authentication like **802.1x** or EAP-TLS.
* **Note:** Default configurations usually prioritize ease of use over security; this control reverses that.

### Control 13: Network Monitoring and Defense

* **Tools:** Processes for monitoring beyond just up/down status. Includes throughput and detailed traffic logging (e.g., Netflow).
* **SIEM:** Use **Security Information and Event Management** tools to collect events from multiple sources and give analysts a clear picture of potential incidents.

### Control 14: Security Awareness and Skills Training

* **Importance:** The person at the keyboard is often the first or last line of defense.
* **Implementation:** Training should be specific to the department or job function and must include all departments in the organization.

### Control 15: Service Provider Management

* **Context:** Key infrastructure is often outsourced to MSPs, MSSPs, or CSPs (Cloud Service Providers).
* **Goal:** Manage the risks associated with moving these tasks outside of the direct organization.

### Control 16: Application Software Security

* **Scope:** Manage both in-house developed and purchased applications (including SaaS).
* **Action:** Prevent, detect, and remediate or mitigate security issues within these applications.

### Control 17: Incident Response Management

* **Requirement:** Develop a plan including policies, procedures, runbooks, and table-top exercises.
* **Personnel:** Defined roles with named individuals must be established, with regular training to ensure everyone understands their role.

### Control 18: Penetration Testing

* **Action:** Periodically (or continuously) assess infrastructure for weaknesses.
* **Method:** Testing that simulates the objectives and tactics of a real attacker, covering internal, external, and cloud-based hosts and applications.

---

# 🛡️ Getting a Start on CIS Critical Security Controls 1 and 2

## 📘 Overview

The foundation of any robust security framework is knowing exactly what you are protecting. This concept is embodied in **CIS Critical Security Controls 1 and 2**:

* **Control 1:** Inventory and Control of Hardware Assets.
* **Control 2:** Inventory and Control of Software Assets.

**The Philosophy:** You cannot secure a device or application if you don't know it exists.

In this section, we will explore a "zero-budget" approach to gathering this critical inventory data using only the **native commands** already built into your Linux host.

---

## 🖥️ Critical Control 1: Hardware Inventory

Gathering hardware information on Linux is straightforward because Linux treats almost everything as a file. We can extract detailed system parameters by reading specific files in the `/proc` directory.

### 1. The `/proc` Filesystem

The `/proc` directory is a **virtual filesystem**. It doesn't contain real files on your hard drive; instead, it contains dynamic files that reflect the current state of the kernel and hardware in real-time.

#### 🧠 CPU Information

To see details about your processor (CPU model, speed, cache size, core count, etc.), you can read the `/proc/cpuinfo` file.

**Command:**

```bash
cat /proc/cpuinfo

```

**Output Analysis:**

```text
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 158
model name      : Intel(R) Xeon(R) CPU E3-1505M v6 @ 3.00GHz
stepping        : 9
microcode       : 0xde
cpu MHz         : 3000.003
cache size      : 8192 KB
physical id     : 0
siblings        : 1
core id         : 0
cpu cores       : 1
...
flags           : fpu vme de pse ... (lists supported CPU features like 'vmx' for virtualization)
bugs            : cpu_meltdown spectre_v1 ... (lists known hardware bugs)
bogomips        : 6000.00

```

* **`model name`**: Tells you exactly what chip is inside.
* **`flags`**: Shows capabilities (e.g., `aes` for encryption acceleration).
* **`bugs`**: Shows hardware vulnerabilities the CPU is susceptible to (like Spectre/Meltdown).

#### 💾 Memory Information

To see details about your RAM (Total, Free, Swap, Buffers), read `/proc/meminfo`.

**Command:**

```bash
cat /proc/meminfo

```

**Output Analysis:**

```text
MemTotal:        8025108 kB   (Total RAM ~8GB)
MemFree:         4252804 kB   (Unused RAM)
MemAvailable:    6008020 kB   (RAM available for new apps)
Buffers:          235416 kB
Cached:          1486592 kB
SwapCached:            0 kB
...

```

#### 🌐 Network Parameters

You can dig even deeper to find specific TCP/IP settings. These are located in:
`/proc/sys/net/ipv4`

---

### 🐧 Operating System Version

Knowing "what hardware I have" often includes "what OS runs on it." There are multiple ways to find this.

**Method 1: `/proc/version` (Kernel & Compiler info)**

```bash
$ cat /proc/version
Linux version 5.8.0-38-generic ... (Ubuntu 9.3.0-17ubuntu1~20.04) ...

```

**Method 2: `/etc/issue` (Distribution Release)**

```bash
$ cat /etc/issue
Ubuntu 20.04.1 LTS \n \l

```

**Method 3: `uname` (Kernel Version)**

```bash
$ uname -v
#43~20.04.1-Ubuntu SMP Tue Jan 12 16:39:47 UTC 2021

```

> **Note:** While OS version is technically software, it is often tracked in the Hardware Inventory because it is the base layer of the system.

---

### 🧰 The "Give Me Everything" Command: `lshw`

If you want a complete dump of all hardware information in one go, use `lshw`.

* **Pros:** Extremely detailed.
* **Cons:** Can be *too* detailed (pages of output). You usually want to be selective.

---

## 📜 Automating Inventory: A Custom Bash Script

Instead of running ten different commands manually, organizations often write a simple script to collect exactly what they need.

Below is a custom script (`hwinven.sh`) that combines `fdisk`, `dmesg`, `dmidecode`, and standard text processing (`grep`, `awk`, `cut`) to generate a clean report.

### 📝 The Script (`hwinven.sh`)

```bash
echo -n "Basic Inventory for Hostname: "
uname -n
#
echo =====================================
# Extract System Info (Manufacturer, Product Name)
dmidecode | sed -n '/System Information/,+2p' | sed 's/\x09//'
# Check for Hypervisors (Virtualization)
dmesg | grep Hypervisor
# Get Serial Numbers (ignoring empty ones)
dmidecode | grep "Serial Number" | grep -v "Not Specified" | grep -v None
#
echo =====================================
echo "OS Information:"
uname -o -r
# Check RedHat specific release file
if [ -f /etc/redhat-release ]; then
 echo -n " "
 cat /etc/redhat-release
fi
# Check Standard Issue file
if [ -f /etc/issue ]; then
 cat /etc/issue
fi
#
echo =====================================
echo "IP information: "
# Get IP address (excluding localhost and IPv6 loopback)
ip ad | grep inet | grep -v "127.0.0.1" | grep -v "::1/128" | tr -s " " | cut -d " " -f 3
#
echo =====================================
echo "CPU Information: "
# Get CPU Model and Vendor, sort and remove duplicates
cat /proc/cpuinfo | grep "model name\|MH\|vendor_id" | sort -r | uniq
echo -n "Socket Count: "
cat /proc/cpuinfo | grep processor | wc -l
echo -n "Core Count (Total): "
# Sum up core counts
cat /proc/cpuinfo | grep cores | cut -d ":" -f 2 | awk '{ sum+=$1} END {print sum}'
#
echo =====================================
echo "Memory Information: "
grep MemTotal /proc/meminfo | awk '{print $2,$3}'
#
echo =====================================
echo "Disk Information: "
# List physical disks
fdisk -l | grep Disk | grep dev

```

### 📤 The Script Output

When you run this script (using `sudo` because `fdisk` and `dmidecode` require root), you get a beautifully formatted inventory report.

**Command:**

```bash
sudo ./hwinven.sh

```

**Result:**

```text
Basic Inventory for Hostname: ubuntu
=====================================
System Information
Manufacturer: VMware, Inc.
Product Name: VMware Virtual Platform
[    0.000000] Hypervisor detected: VMware
 Serial Number: VMware-56 4d 5c ce 85 8f b5 52-65 40 f0 92 02 33 2d 05
=====================================
OS Information:
5.8.0-45-generic GNU/Linux
Ubuntu 20.04.2 LTS \n \l
=====================================
IP information:
192.168.122.113/24
fe80::1ed6:5b7f:5106:1509/64
=====================================
CPU Information:
vendor_id       : GenuineIntel
model name      : Intel(R) Xeon(R) CPU E3-1505M v6 @ 3.00GHz
cpu MHz         : 3000.003
Socket Count: 2
Core Count (Total): 2
=====================================
Memory Information:
8025036 kB
=====================================
Disk Information:
Disk /dev/loop0: 65.1 MiB, 68259840 bytes, 133320 sectors
Disk /dev/loop1: 55.48 MiB, 58159104 bytes, 113592 sectors
Disk /dev/loop2: 218.102 MiB, 229629952 bytes, 448496 sectors
...
Disk /dev/sda: 40 GiB, 42949672960 bytes, 83886080 sectors
...

```

### 🔍 Key Takeaways from the Output

1. **System Information:** It correctly identified this as a **VMware Virtual Platform**, not physical hardware.
2. **IP Information:** It listed both IPv4 (`192.168...`) and IPv6 (`fe80...`) addresses.
3. **Disk Information:** It listed the main hard drive (`/dev/sda`, 40 GiB) and several `loop` devices (often used by Snap packages in Ubuntu).

---

# 📦 Critical Control 2 – Software Inventory

## 📘 Overview

**CIS Critical Control 2** focuses on "Inventory and Control of Software Assets."
Just like with hardware, you cannot secure your environment if you don't know what software is installed. Unpatched or unauthorized software is a primary vector for attacks.

We will explore two ways to achieve this:

1. **Native Linux Commands:** Using package managers (`apt`, `dpkg`, `rpm`).
2. **Advanced Tooling:** Using **OSQuery** for a database-driven approach.

---

## 🐧 Part 1: Native Linux Inventory Commands

### 1. Using `apt` (Debian/Ubuntu)

The easiest way to get a count of installed packages is using `apt`.

**Command:**

```bash
sudo apt list --installed | wc -l
```

**Output:**

```text
WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
1735

```

**Insight:**

* The system has **1735** packages installed.
* **Warning:** The `apt` command warns that its output format might change in future versions, so it's not ideal for automated scripts.

### 2. Using `dpkg` (Debian/Ubuntu)

For detailed information that is script-friendly, `dpkg` is the better tool.

**Command: List All Packages**

```bash
dpkg -l
```

**Output:**

```text
Name                       Version               Description
====================================================================================
acpi-support               0.136.1               scripts for handling many ACPI events
acpid                      1.0.10-5ubuntu2.1     Advanced Configuration and Power Interface
adduser                    3.112ubuntu1          add and remove users and groups
adium-theme-ubuntu         0.1-0ubuntu1          Adium message style for Ubuntu
adobe-flash-properties-gtk 10.3.183.10-0lucid1   GTK+ control panel for Adobe Flash Player
.... and so on ....
```

**Command: List Files Inside a Package**
If you want to know exactly where `openssh-client` installed its files, use `-L`.

```bash
hashim@Hashim:~$ dpkg -L openssh-client
```

**Output:**

```text
/.
/etc
/etc/ssh
/etc/ssh/ssh_config
/etc/ssh/ssh_config.d
/usr
/usr/bin
/usr/bin/scp
/usr/bin/sftp
/usr/bin/ssh
...
```

### 3. Using `rpm` (Red Hat/CentOS/Fedora)

For Red Hat-based systems, we use the **RPM (Red Hat Package Manager)**.

**Command: List All Installed Packages**

```bash
rpm -qa
```

**Output:**

```text
libsepol-devel-2.0.41-3.fc13.i686
wpa_supplicant-0.6.8-9.fc13.i686
system-config-keyboard-1.3.1-1.fc12.i686
... (and so on)
```

**Command: Get Info on a Specific Package**
To get details (Version, Vendor, Build Date, License) about a package like `python`, use `-qi`.

```bash
rpm -qi python
```

**Output:**

```text
Name        : python                       Relocations: (not relocatable)
Version     : 2.6.4                        Vendor: Fedora Project
Release     : 27.fc13                      Build Date: Fri 04 Jun 2010 02:22:55 PM EDT
Install Date: Sat 19 Mar 2011 08:21:36 PM  Build Host: x86-02.phx2.fedoraproject.org
Group       : Development/Languages        Source RPM: python2.6.4-27.fc13.src.rpm
Size        : 21238314                     License: Python
Signature   : RSA/SHA256, Fri 04 Jun 2010 02:36:33 PM EDT, Key ID 7edc6ad6e8e40fde
Packager    : Fedora Project
URL         : http://www.python.org/
Summary     : An interpreted, interactive, object-oriented programming language
Description : Python is an interpreted, interactive, object-oriented programming ...

```

---

## 🔍 Part 2: OSQuery (Advanced Inventory & Security)

**Why use OSQuery?**
Native commands (`dpkg`, `rpm`) produce text files that are hard to manage across 1,000 servers.
**OSQuery** turns your operating system into a **SQL Database**. You can query it like a database to instantly find answers across Linux, Windows, and macOS.

### 🛠️ Installing OSQuery on Ubuntu

We need to add the repository and install the package.

**Commands:**

```bash
wget https://github.com/osquery/osquery/releases/download/5.11.0/osquery_5.11.0-1.linux_amd64.deb

cd ~/Downloads

sudo dpkg -i osquery_5.11.0-1.linux_amd64.deb

osqueryi --version
```

### 🧩 Components of OSQuery

* **`osqueryd`**: The background daemon (service) that runs scheduled queries.
* **`osqueryi`**: The **interactive shell**. This is where you type SQL commands to explore the system manually.
* **`osqueryctl`**: A helper script to test configurations.

---

### 💻 Using the OSQuery Interactive Shell (`osqueryi`)

Let's start the shell and see what tables are available.

**Command:**

```bash
hashim@Hashim:~$ osqueryi
```

**Output:**

```text
Using a virtual database. Need help, type '.help'
osquery> .help
Welcome to the osquery shell. Please explore your OS!
You are connected to a transient 'in-memory' virtual database.
...

```

**Listing Tables:**
To see what you can query (e.g., users, packages, wifi), type `.tables`.

```bash
osquery> .tables
```

**Output:**

```text
 => acpi_tables
 => apparmor_events
 => apt_sources
 => arp_cache
 => block_devices
 ...
```

---

### ⚡ Practical Queries for Security (Critical Controls 1 & 2)

#### 1. Software Inventory (Control 2)

Get the OS version details.

**Query:**

```sql
select * from os_version;
```

**Output:**

```text
+--------+-----------------------+-------+-------+-------+-------+----------+---------------+----------+--------+
| name   | version               | major | minor | patch | build | platform | platform_like | codename | arch   |
+--------+-----------------------+-------+-------+-------+-------+----------+---------------+----------+--------+
| Ubuntu | 25.04 (Plucky Puffin) | 25    | 4     | 0     |       | ubuntu   | debian        | plucky   | x86_64 |
+--------+-----------------------+-------+-------+-------+-------+----------+---------------+----------+--------+
```

#### 2. Network Inventory (Control 1)

Find IP addresses (excluding the Loopback `lo` interface).

**Query:**

```sql
select interface,address,mask from interface_addresses where interface NOT LIKE '%lo%';
```

**Output:**

```text
+-----------+-----------+---------------+
| interface | address   | mask          |
+-----------+-----------+---------------+
| enp0s3    | 10.0.2.15 | 255.255.255.0 |
+-----------+-----------+---------------+
```

#### 3. View ARP Cache (Who are we talking to?)

**Query:**

```sql
select * from arp_cache;
```

**Output:**

```text
+-----------+-------------------+-----------+-----------+
| address   | mac               | interface | permanent |
+-----------+-------------------+-----------+-----------+
| 10.0.2.2  | 52:55:0a:00:02:02 | enp0s3    | 0         |
| 10.0.2.20 | 00:00:00:00:00:00 | enp0s3    | 0         |
+-----------+-------------------+-----------+-----------+
```

#### 4. List Installed Packages (Control 2)

**Query:**

```sql
select * from deb_packages limit 2;
```

**Output:**

```text
+-----------------+------------------+--------+------+-------+----------+----------------------+-----------------------------------------------------------+---------+----------+---------------+
| name            | version          | source | size | arch  | revision | status               | maintainer                                                | section | priority | admindir      |
+-----------------+------------------+--------+------+-------+----------+----------------------+-----------------------------------------------------------+---------+----------+---------------+
| accountsservice | 23.13.9-7ubuntu1 |        | 552  | amd64 | 7ubuntu1 | install ok installed | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | admin   | optional | /var/lib/dpkg |
| acl             | 2.3.2-2          |        | 192  | amd64 | 2        | install ok installed | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | utils   | optional | /var/lib/dpkg |
+-----------------+------------------+--------+------+-------+----------+----------------------+-----------------------------------------------------------+---------+----------+---------------+
```

---

### 🛡️ Advanced Security: Malware Detection (Control 10)

We can go beyond simple inventory. We can list running processes and **calculate their SHA256 Hash**.

* **Why?** Malware often hides by using a fake name (e.g., `bash` or `update-notifier`).
* **The Fix:** If you check the **Hash** (Digital Fingerprint), you can see if the `bash` process is the *real* `bash` or a virus pretending to be `bash`.

**Query:**

```sql
SELECT DISTINCT h.sha256, p.name, u.username
FROM processes AS p
INNER JOIN hash AS h ON h.path = p.path
INNER JOIN users AS u ON u.uid = p.uid
ORDER BY start_time DESC
LIMIT 5;
```

**Output:**

```text
W0116 10:38:58.135358  5862 filesystem.cpp:139] Cannot read /opt/osquery/bin/osqueryd size exceeds limit: 86508160 > 52428800
+------------------------------------------------------------------+---------------+----------+
| sha256                                                           | name          | username |
+------------------------------------------------------------------+---------------+----------+
|                                                                  | osqueryi      | hashim   |
| b8d3da2bedb52234e236bb3702310d77c3bdc429321552e60d05717896f6b049 | gvfsd-recent  | hashim   |
| 5ff1ea84ba9ecb43e4da3f51145e052593afd9cab4f5a48c46c6b4a165b3dda8 | gvfsd-network | hashim   |
| 4dd760d3fef6dfdb489ad1465279926c1b2d784954445046573ecd77f5f5ce9e | gvfsd-dnssd   | hashim   |
| 5ef5374cb79a1b84b06bcac6a4d1ecb3671cfb46f80930824b0d3cdf77c48065 | gvfsd-wsdd    | hashim   |
+------------------------------------------------------------------+---------------+----------+
```

### 🚀 Conclusion

With just a few queries, **OSQuery** allows us to:

1. Verify OS versions (Find vulnerable hosts).
2. Inventory software packages (Find unpatched apps).
3. Hash running processes (Detect Malware).

This makes it an incredibly powerful tool for meeting **CIS Critical Controls 1, 2, 10, and 17**.

---

# 🛡️ Applying a CIS Benchmark: Securing SSH on Linux

## 📘 Overview

When securing a server, relying on guesswork isn't enough. You need a standard checklist. This is what the **CIS (Center for Internet Security) Benchmarks** provide. They are industry-standard "best practice" guides for securing operating systems and software.

**The Reality of Benchmarks:**

* You typically **never** implement 100% of a benchmark.
* Security settings can break functionality.
* The goal is to evaluate each recommendation and create an organization-specific "Build Document."

In this guide, we will use the **CIS Benchmark for Ubuntu 20.04** to secure **SSH (Secure Shell)**, the primary door for remote administration on Linux.

---

## 🏗️ Step 1: Preparation (Update & Install)

Before securing the system, we must ensure the OS is up to date and the SSH service is actually installed.

**1. Update the System**
We run two commands in sequence using `&&` (the second only runs if the first succeeds).

* `update`: Refreshes the list of available software.
* `upgrade`: Installs the newest versions.

**Command:**

```bash
sudo apt update && sudo apt upgrade
```

**2. Install SSH Server**
SSH is not always installed by default on desktop versions of Ubuntu.

**Command:**

```bash
sudo apt-get install openssh-server
```

---

## 📋 The CIS SSH Recommendations

The benchmark lists **22 separate recommendations** (Section 5.2) for SSH. Here are a few key examples:

* **5.2.9:** Disable root login (Prevent the "God" account from logging in remotely).
* **5.2.12:** Use strong Ciphers (Ensure encryption is modern and unbreakable).
* **5.2.15:** Set Idle Timeout (Kick off users who walk away from their desks).

Let's implement two of the most critical checks in detail.

---

## 🔒 Deep Dive 1: Disable Root Login (5.2.9)

**The Problem:**
The "root" user exists on every Linux system. If you allow root login, attackers already know the **username** (50% of the puzzle); they just need to guess the password.
**The Goal (Non-Repudiation):**
Every administrator should log in with their own **named account** (e.g., `robv` or `hashim`). If an incident occurs, the logs will show exactly *who* did it. You cannot claim "it wasn't me" if the log shows your specific username.

**1. Audit (Check current status)**
We check the running configuration (`-T`) for the `permitrootlogin` setting.

**Command:**

```bash
sudo sshd -T | grep permitrootlogin
```

**Output:**

```text
permitrootlogin without-password
```

* **Verdict:** **Non-Compliant.** This setting allows root login using keys (certificates). We want to block it entirely.

**2. Remediation (Fix it)**
We edit the configuration file `/etc/ssh/sshd_config`. We need to change the setting to `no`.

**3. Verification**
After saving the file and reloading SSH, we check again.

**Command:**

```bash
sudo sshd -T | grep permitrootlogin
```

**Output:**

```text
permitrootlogin no
```

* **Verdict:** **Compliant.**

---

## 🔐 Deep Dive 2: Ensure Strong Ciphers (5.2.12)

**The Problem:**
SSH supports many encryption algorithms (Ciphers). Some older ones (like DES, 3DES, or CBC modes) are weak and can be cracked.
**The Goal:**
Force SSH to use only strong, modern encryption strings.

**1. Audit (Check current status)**

**Command:**

```bash
sudo sshd -T | grep Ciphers
```

**Output:**

```text
ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com
```

* **Verdict:** **Mixed.** While strong ciphers are present, some non-compliant ones are also enabled. An attacker could force a "downgrade" to a weaker cipher.

**2. Remediation (Fix it)**
We edit `/etc/ssh/sshd_config`. Often, the `Ciphers` line doesn't exist, so we must add it manually at the bottom.

**Text to Add:**

```text
# Ciphers and keying
Ciphers aes256-ctr,aes192-ctr,aes128-ctr
```

**3. Reload and Verify**
Reload the service so changes take effect.

**Command:**

```bash
sudo systemctl reload sshd
```

**Check again:**

```bash
cat sshd_config | grep Cipher
```

**Output:**

```text
# Ciphers and keying
Ciphers aes256-ctr,aes192-ctr,aes128-ctr
```

---

## 🕵️ Verification with Nmap

Trusting your own configuration file is good, but verifying from the "outside" is better. We can use `nmap` with a specific script (`ssh2-enum-algos`) to ask the server exactly what encryption it supports.

**Command:**

```bash
sudo nmap -p22 -Pn --open 127.0.0.1 --script ssh2-enum-algos.nse
```

**Output:**

```text
Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-08 15:22 Eastern Standard Time
Nmap scan report for ubuntu.defaultroute.ca (127.0.0.1)
Host is up (0.00013s latency).
PORT STATE SERVICE
22/tcp open ssh
| ssh2-enum-algos:
|   encryption_algorithms: (3)
|       aes256-ctr
|       aes192-ctr
|       aes128-ctr
...
Nmap done: 1 IP address (1 host up) scanned in 4.09 seconds
```

* **Result:** The server now **only** offers the three strong ciphers we configured. The weak ones are gone.

---

# 🛡️ SSH Hardening: Quick Security Wins

These three settings are essential for any Linux server. They prevent resource exhaustion and improve auditing.

### 🛠️ Step 1: Edit the Configuration File

Open the file with `nano`.

**Command:**

```bash
sudo nano /etc/ssh/sshd_config
```

### 🛠️ Step 2: Locate and Modify Settings

#### 1. Logging Level (5.2.4)

Change logging from `INFO` to `VERBOSE`. This ensures the logs record the **fingerprint of the key** used to log in, which is crucial for forensic analysis.

**Configuration:**

```text
LogLevel VERBOSE
```

#### 2. Idle Timeout (5.2.15)

This kicks off users who leave their session open.

* `ClientAliveInterval 300`: Server sends a "Are you there?" check every 300 seconds (5 minutes).
* `ClientAliveCountMax 0`: If the client doesn't respond instantly (meaning they are idle), disconnect them.

**Configuration:**

```text
ClientAliveInterval 300
ClientAliveCountMax 0
```

#### 3. MaxSessions (5.2.22)

This limits the number of shell sessions per connection. Attackers use "Multiplexing" to open hundreds of shells over a single connection to crash the server (DoS). Limiting this to 2 or 10 stops that attack.

**Configuration:**

```text
MaxSessions 2
```

### 🚀 Step 3: Save, Test, and Restart

**1. Save and Exit:**

* Press `Ctrl + O` then `Enter`.
* Press `Ctrl + X`.

**2. Test Syntax:**
Always test before restarting. If you made a typo, this command will tell you *before* you break the server.

**Command:**

```bash
sudo sshd -t
```

*(If there is no output, the syntax is correct).*

**3. Restart SSH:**
Apply the changes.

**Command:**

```bash
sudo systemctl restart ssh
```

Your SSH server is now significantly harder to attack! ✅


---