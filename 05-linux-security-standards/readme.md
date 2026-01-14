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