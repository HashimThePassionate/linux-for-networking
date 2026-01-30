# 🏗️ Building a Private Certificate Authority

## 📘 Overview

Building a private Certificate Authority (CA) begins with a fundamental decision: **Which software package should we use?**

Just like with DNS or DHCP, there isn't a single tool for the job. There is a spectrum of options ranging from manual, command-line tools to fully automated systems that manage the entire lifecycle of a certificate.

---

## 🛠️ The Options: Choosing Your CA Software

The text outlines six specific options available for Linux administrators, categorized by their level of automation and integration.

### 1. OpenSSL (The Universal Standard)

* **Description:** This provides all the raw tools needed to build a PKI (Public Key Infrastructure). You manually maintain the directory structure and write your own scripts.
* **Capabilities:** It allows you to create **Root CAs**, **Subordinate CAs**, generate **CSRs (Certificate Signing Requests)**, and sign them to create valid certificates .
* **Pros:** It is universally supported and gives you total control.
* **Cons:** It is heavily manual. You must manage the "bits and pieces" yourself, which can be tedious for most users.

### 2. Certificate Manager

* **Description:** A CA tool bundled specifically with **Red Hat Linux** and its related distributions.

### 3. YaST (Yet another Setup Tool)

* **Description:** The native configuration tool for **openSUSE** and related distributions. It includes a built-in module to manage a CA.

### 4. Easy-RSA

* **Description:** A set of scripts that essentially acts as a **wrapper** around OpenSSL.
* **Goal:** To make the complex OpenSSL commands easier to use without changing the underlying technology.

### 5. Smallstep (The Modern Automation Tool)

* **Description:** A modern tool designed for automation.
* **Key Feature:** It can be configured as a private **ACME** server.
* **Benefit:** It allows clients to "help themselves" by requesting and fulfilling their own certificates automatically, rather than an admin manually signing each one.

### 6. Boulder

* **Description:** An **ACME-based CA** written in the **Go** programming language.
* **Origin:** This is the software distributed on the **Let's Encrypt** GitHub page, meaning it powers one of the largest public CAs in the world.

---

## 📉 The Evolution: From Manual to ACME

The text highlights a clear trend in how these tools are designed:

1. **The "Old" Way (OpenSSL & Wrappers):** Most older tools are simply wrappers around OpenSSL commands. They require the administrator to handle the process: receive a request, verify it, sign it, and return it .
2. **The "New" Way (ACME Protocol):** Newer tools (like Smallstep and Boulder) focus on the **ACME protocol**, pioneered by Let's Encrypt. This protocol allows servers to automatically prove they own a domain and fetch a certificate without human intervention.

---

## 🎯 The Decision: Why We Will Use OpenSSL

Despite the rise of automation tools, the guide selects **OpenSSL** for the upcoming example.

* **Reason:** It is the **most widely deployed** Linux CA solution.
* **Learning Value:** Because it is manual, using OpenSSL forces you to understand the underlying mechanics of PKI (keys, signing, requests) rather than having a script hide them from you.

# 🏗️ Building a Private CA with OpenSSL: Initial Setup

## 📘 Overview

Because OpenSSL is a foundational tool included in almost every Linux distribution, there is usually nothing to install. We can begin building our Certificate Authority (CA) immediately using the tools already present on the system.

The setup process involves creating a secure directory structure to house the CA and initializing the simple flat-file database it uses to track issued certificates.

---

## 📂 Step 1: Creating the CA Directory Structure

The standard location for SSL/TLS configuration on most Linux systems is `/etc/ssl`. We need to create dedicated subdirectories within this protected area to store our Certificate Authority's private data and the certificates it issues.

**Commands:**

```bash
$ sudo mkdir /etc/ssl/CA
$ sudo mkdir /etc/ssl/newcerts
```

**Detailed Explanation:**

1. **`sudo mkdir /etc/ssl/CA`**:
* **`sudo`**: Grants root privileges (required because regular users cannot write to `/etc`).
* **`mkdir`**: The "make directory" command.
* **`/etc/ssl/CA`**: This new directory will serve as the "home base" for your CA, storing its private keys and configuration files.


2. **`sudo mkdir /etc/ssl/newcerts`**:
* **`/etc/ssl/newcerts`**: This directory acts as an archive. Every time you issue a certificate, a copy will be stored here so you have a history of everything the CA has signed.



**Output:**

* These commands are silent upon success. If you see no output, the directories were created successfully.

---

## 📝 Step 2: Initializing the CA Database

A Certificate Authority needs to keep a ledger. It must track two things:

1. **Serial Numbers:** Every certificate needs a unique ID. We usually start sequentially.
2. **Index/Status:** A list of every certificate issued, including its details and validity status.

We initialize these by creating two specific files.

### 1. The Serial Number File

We will create a file named `serial` and seed it with the starting number `01`.

**Command:**

```bash
$ sudo sh -c "echo '01' > /etc/ssl/CA/serial"
```

**Detailed Explanation:**

* **The Goal:** To write the text `01` into the file `/etc/ssl/CA/serial`.
* **The Challenge:** You might expect to run `sudo echo '01' > ...`. However, this fails on Linux.
* *Why?* When you use the redirection symbol (`>`), your *current* shell (running as your normal user) tries to open the file for writing *before* the `sudo` command even runs. Since your user doesn't own `/etc/ssl/CA`, permission is denied.


* **The Solution (`sh -c`):**
* **`sudo sh`**: We elevate to root and immediately start a temporary shell.
* **`-c "..."`**: We pass the entire command string (echo and redirect) to this new root shell.
* **Result:** The redirection `>` is now performed by the root shell, which has permission to write the file.



### 2. The Index File

We need an empty database file to start tracking certificates.

**Command:**

```bash
$ sudo touch /etc/ssl/CA/index.txt
```

**Detailed Explanation:**

* **`touch`**: A standard Unix command that updates the timestamp of a file. If the file does not exist, it creates an empty one.
* **`/etc/ssl/CA/index.txt`**: This text file will grow over time, adding a new line for every certificate we sign. Starting it as an empty file prepares OpenSSL to append data to it.

---

## 🛡️ Security Insight: Why not `sudo su`?

The text highlights an important security best practice regarding the `sudo sh -c` command used above.

Alternative methods, like running `sudo su` or `su` to become the root user permanently, would also allow you to create these files. However, using the "single-shot" command (`sudo sh -c`) is far superior.

**The Risk of Root Shells:**
Staying in a root shell context (where your prompt is `#` instead of `$`) keeps you in a "god mode" state.

* **Accidental Deletion:** You might accidentally delete critical system files that only root has access to.
* **Malware Risks:** If you accidentally download or execute a malicious script while in a root shell, the malware immediately gains full system control (potentially installing ransomware), whereas a normal user context limits the damage.

By using `sudo sh -c`, you execute the specific command with high privileges and immediately return to your safer, regular user context.

# 🏗️ Building a Private CA with OpenSSL: Configuration & Root Certificate

## 📘 Overview

Now that the directory structure is in place, we must configure OpenSSL to recognize our new file paths and then generate the most critical component of our PKI: the **Root Certificate**. This certificate will serve as the trusted anchor for all other certificates issued by your organization.

---

## ⚙️ Step 3: Editing the Configuration File

We need to tell OpenSSL where to find our new directories (`/etc/ssl/CA`, etc.). This is done by editing the master configuration file located at `/etc/ssl/openssl.cnf`.

We specifically need to modify the `[ CA_default ]` section.

**The Original Defaults:**
By default, OpenSSL expects files in a local `./demoCA` directory, which is not suitable for a system-wide CA.

```ini
[ CA_default ]
dir = ./demoCA              # Where everything is kept
certs = $dir/certs          # Where the issued certs are kept
crl_dir = $dir/crl          # Where the issued crl are kept
database = $dir/index.txt   # database index file.
#unique_subject = no        # Set to 'no' to allow creation of several certs with same subject.
new_certs_dir = $dir/newcerts # default place for new certs.
certificate = $dir/cacert.pem # The CA certificate
serial = $dir/serial        # The current serial number
crlnumber = $dir/crlnumber  # the current crl number
crl = $dir/crl.pem          # The current CRL
private_key = $dir/private/cakey.pem # The private key
x509_extensions = usr_cert  # The extensions to add to the cert
```

**The Required Changes:**
We must update the path variables to point to our system's SSL directory `/etc/ssl`.

**Configuration Updates:**

```ini
dir = /etc/ssl                  # CHANGED: Point to the system SSL directory
database = $dir/CA/index.txt    # CHANGED: Point to the index file we created
certificate = $dir/certs/cacert.pem # CHANGED: Where the public Root Cert will live
serial = $dir/CA/serial         # CHANGED: Point to the serial file we created
private_key = $dir/private/cakey.pem # No change needed, but verify it points to /private/
```

> **Note:** Ensure you double-check the `private_key` line. Even though we didn't change the text, it now resolves to `/etc/ssl/private/cakey.pem` because we changed the `dir` variable.

---

## 🔐 Step 4: Creating the Self-Signed Root Certificate

With the configuration set, we generate the Root Certificate.

* **Private CA:** For an internal CA, we create a **Self-Signed** root certificate. We are the root of trust.
* **Public CA:** If this were public, we would generate a request (CSR) and send it to a higher authority (like Verisign) to be signed.

**Validity Period:** Since this is the foundation of your infrastructure, we set a long lifespan (**10 years** / 3,650 days) to avoid having to rebuild the entire PKI frequently.

**The Command:**

```bash
$ openssl req -new -x509 -extensions v3_ca -keyout cakey.pem -out cacert.pem -days 3650
```

**Command Breakdown:**

* `req`: The OpenSSL subcommand for managing certificate requests.
* `-new`: Generate a new certificate request.
* `-x509`: Instead of creating a request (CSR) to send away, output a **Self-Signed Certificate** immediately.
* `-extensions v3_ca`: Apply X.509 v3 extensions required for a Certificate Authority (allows this cert to sign others).
* `-keyout cakey.pem`: Save the new Private Key to this file.
* `-out cacert.pem`: Save the new Public Certificate to this file.
* `-days 3650`: Make the certificate valid for 10 years.

**The Interactive Process:**
When you run the command, OpenSSL will ask for a **Passphrase** (to protect the private key) and **Identity Information** (Distinguished Name).

**Output & Inputs:**

```text
Generating a RSA private key
...............+++++
.................................................+++++
writing new private key to 'cakey.pem'
Enter PEM pass phrase:  <Type a Strong Password>
Verifying - Enter PEM pass phrase: <Repeat Password>
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
...
Country Name (2 letter code) [AU]: CA
State or Province Name (full name) [Some-State]: ON
Locality Name (eg, city) []: MyCity
Organization Name (eg, company) [Internet Widgits Pty Ltd]: Coherent Security
Organizational Unit Name (eg, section) []: IT
Common Name (e.g. server FQDN or YOUR name) []: ca01.coherentsecurity.com
Email Address []:
```

> **Critical Note:** Do **not** lose the PEM pass phrase. Without it, you cannot use your CA to sign certificates.
---

## 📦 Step 5: Securing the Keys

The `openssl` command generated the files in your current directory. We must move them to the secure locations defined in our configuration file.

**Commands:**

```bash
sudo mv cakey.pem /etc/ssl/private/
sudo mv cacert.pem /etc/ssl/certs/
```

**Security Best Practice:**

* **Use `mv` (Move), NOT `cp` (Copy):**
* It is common during security audits to find sensitive keys left in "temporary" or "home" directories because an admin copied them instead of moving them.
* If an attacker finds a copy of `cakey.pem` in your home folder, they can compromise your entire PKI. **Always move the files.**

### 🎉 Status: Open for Business!

Your Private Certificate Authority is now fully operational.

1. **Private Key:** Securely stored in `/etc/ssl/private/cakey.pem`.
2. **Root Certificate:** Stored in `/etc/ssl/certs/cacert.pem`.
3. **Configuration:** Pointed correctly at `/etc/ssl`.

You are now ready to generate Certificate Signing Requests (CSRs) and sign them!

---