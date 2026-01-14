# 🛡️ Linux Security Standards

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