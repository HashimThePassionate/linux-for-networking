# 🌐 The Domain Name System (DNS)

## 📘 Overview

The **Domain Name System (DNS)** is described as a major underpinning of today's information-based society. It is the fundamental service that connects corporate networks and the public internet, acting as the directory that translates human-readable names into machine-readable IP addresses.

The text highlights a famous proverb within the technical community, presented in the form of a **Haiku**, which perfectly captures the relationship between network engineers and DNS troubleshooting:

> *It's not DNS*
> *There is no way it's DNS*
> *It was DNS*

### 🔍 The Meaning Behind the Haiku

This poem describes a specific technical reality:

1. **Denial:** When a problem arises (even widespread internet or cloud outages), the initial reaction is often to assume the complex infrastructure is at fault, not the basic directory service ("It's not DNS").
2. **Resistance:** As troubleshooting continues, technicians often refuse to believe such a foundational service could be broken ("There is no way it's DNS").
3. **Acceptance/Resolution:** Finally, after exhausting other options, the solution reveals that the root cause was, in fact, the naming system ("It was DNS").

This illustrates that **"The root problem is always DNS."** It emphasizes how critical this service is to every aspect of modern networking.

---

## 📚 Chapter Roadmap: What We Will Cover

This chapter explores the lifecycle of DNS, from basic concepts to advanced troubleshooting and modern security protocols.

### 🏗️ DNS Fundamentals & Implementation

We will begin by establishing the groundwork of the system:

* **What is DNS?**: Defining the core function and structure.
* **Server Implementations**: We will look at the **two main DNS server implementations** used in the industry.
* **Common Deployments**: How DNS is typically set up in real-world environments.
* **Troubleshooting & Reconnaissance**: Techniques for diagnosing DNS issues and gathering information about DNS infrastructure.

### 🔒 Modern Secure DNS Implementations

Once the basics are established, we will discuss **two entirely new implementations** that are seeing rapid adoption to improve privacy and security:

1. **DoH (DNS over HTTPS):**
* *Full Name:* DNS over HyperText Transfer Protocol Secure.
* *Function:* Encrypts DNS queries via the HTTPS protocol, blending DNS traffic with regular web traffic to prevent spying and spoofing.


2. **DoT (DNS over TLS):**
* *Full Name:* DNS over Transport Layer Security.
* *Function:* Encrypts DNS queries using the TLS protocol, providing a dedicated secure channel for DNS traffic.



### 🛡️ DNS Security Extensions (DNSSEC)

Finally, the chapter will cover **DNSSEC**.

* **Function:** This implementation **cryptographically signs DNS responses**.
* **Purpose:** It proves that the data received is **verified** and has **not been tampered with** during transit (preventing Man-in-the-Middle attacks where an attacker redirects users to a fake website).

---

# 🌐 What is DNS?

The **Domain Name System (DNS)** acts as the essential translator for the internet. It bridges the gap between how humans communicate and how computers communicate.

* **The Human Side:** People understand and remember text-based names like `google.com` or `paypal.com`. This occurs at **Layer 7 (Application Layer)** of the OSI model.
* **The Computer Side:** Network equipment doesn't understand names. Routers and switches need numeric **IP (Internet Protocol)** addresses to route traffic at **Layer 3 (Network)** and **Layer 4 (Transport)**.

DNS takes the **Fully Qualified Domain Name (FQDN)** you type into a browser and translates it into the IP address the network needs to deliver your request.

### 🔄 Reverse Lookup (PTR)

While the most common use of DNS is Name-to-IP, it can also work in reverse.

* **Pointer (PTR) Record:** This maps a known IP address back to a specific domain name.
* **Usage:** This is called a "reverse lookup." It is primarily used by technical administrators for troubleshooting and verification, rather than by average users.

---

## 🏢 Two Main DNS Server Implementations

The global DNS infrastructure is massive, consisting of **13 root name server clusters**, major public resolvers (like Google or Cloudflare), and registrars who sell domain names. However, for a network administrator, the focus is usually on two specific use cases:

1. **Internal DNS Servers:** These face **inwards**, serving the employees and devices within the organization.
2. **External DNS Servers:** These face the **internet**, answering queries from the outside world about the organization's public services (like their website).

### 🏠 The Organization's Internal DNS

This is the most common service deployed by organizations. It resolves names for internal users.

* **Zone Files:** These files contain the actual records (mappings) for internal hosts.
* **Population:** Records are added manually by admins or automatically via **DHCP (Dynamic Host Configuration Protocol)** leases when devices join the network.

---

## 📉 The Journey of a DNS Request

When a user tries to access a website, a complex chain of events occurs. If the request is for a local, internal resource, the internal DNS server answers immediately. However, if the user requests an **external** website (like `www.example.com`), the process is much more involved.

### 🖼️ Visualizing the Process (Figure 6.1)

The following image illustrates the "worst-case scenario"—a full lookup where no information is cached. Even though it looks complicated, it happens in milliseconds.

### 🦶 Step-by-Step Breakdown: Resolving `www.example.com`

Below is the detailed workflow corresponding to the diagram above.

**1. The Client Request**

* **Action:** The user (Person) requests `www.example.com`.
* **Details:** The client checks its local cache. If empty, it sends the request to the organization's **Internal DNS Server**.

**2. Forwarding**

* **Action:** The Internal DNS server checks its own cache.
* **Details:** If the answer is missing or the **TTL (Time To Live)** has expired, the server passes the request to its upstream **Forwarder** (a Public DNS Server like Google `8.8.8.8` or ISP DNS).

**3. Querying the Root**

* **Action:** The Forwarder checks its cache. If empty, it must find out who controls `.com`.
* **Details:** The Forwarder queries one of the **Root Name Servers**. These are the top-level authorities for the internet.

**4. The Root Response (TLD Referral)**

* **Action:** The Root Server replies.
* **Details:** It does *not* know the IP of `www.example.com`. Instead, it tells the Forwarder: *"I don't know, but here is the address of the **.com** Authoritative Server (TLD Server)."*

**5. Querying the TLD**

* **Action:** The Forwarder saves this info and now queries the **.com Authoritative Server**.

**6. The TLD Response (Domain Referral)**

* **Action:** The `.com` server replies.
* **Details:** It also does not know the IP. It tells the Forwarder: *"I don't know, but here is the address of the Authoritative Server for **example.com**."*

**7. Querying the Domain Authority**

* **Action:** The Forwarder now queries the final **Authoritative Name Server** specifically for `example.com`.

**8. The Final Answer**

* **Action:** This server *does* know the answer. It sends the IP address of `www.example.com` back to the Forwarder.

**9. Caching & Replying**

* **Action:** The Forwarder **caches** this IP (to save time next time) and sends the answer back to the Internal DNS Server.

**10. Delivery to Client**

* **Action:** The Internal DNS Server caches the IP and sends it to the user's computer. The browser can now connect to the website.

---

## ⚡ The Power of Caching

The process described above is the **worst-case scenario**. In reality, DNS is much faster because of **Caching**.

* **Steady State:** Once a server has been running for a while, it remembers answers.
* **Skipping Steps:** Usually, the process skips from **Step 1** directly to **Step 10** because the Internal DNS server already knows the answer.
* **Forwarder Efficiency:** Even if the Internal Server doesn't know, the Forwarder likely already knows where the `.com` servers are, so it never has to bother the Root Servers (Steps 3 & 4 are skipped).

---

# ⚙️ Configuring DNS Servers: Internal vs. Internet-Facing

## 📘 Overview

Configuring a DNS server requires a clear understanding of its role. Is it serving your internal employees (Internal DNS), or is it telling the world how to find your website (Internet-Facing DNS)?

These two roles have completely different requirements regarding performance, security, and functionality.

---

## 🏢 1. The Internal DNS Server

The primary goal of an **Internal DNS Server** is to resolve names for local devices and employees. To make this work effectively, specific features must be enabled.

### ✅ Key Features to Enable

* **DNS Recursion:**
* **Definition:** The ability of the server to ask other servers on behalf of the client.
* **Why it's needed:** If a user asks for `google.com`, the internal server doesn't know the answer. It needs permission to go "up the line" and ask the internet for the answer.


* **Forwarder Entries:**
* **Definition:** Specific IP addresses where the server sends requests it cannot answer itself.
* **Why it's needed:** Instead of querying the Root Servers directly (which is slow), the internal server forwards requests to massive, high-performance upstream providers. These providers have massive caches, speeding up browsing for everyone.



### 📋 Common Public DNS Forwarders

Below is the list of industry-standard forwarders (from the provided image). These are preferred over ISP DNS servers due to better reliability and features.

**Google**

* **IPv4:** `8.8.8.8`, `8.8.4.4`
* **IPv6:** `2001:4860:4860::8888`, `2001:4860:4860::8844`

**Cloudflare**

* **IPv4:** `1.1.1.1`, `1.0.0.1`
* **IPv6:** `2606:4700:4700::1111`, `2606:4700:4700::1001`

**Quad9** (Focus on Security/Blocking Malicious Domains)

* **IPv4:** `9.9.9.9`, `149.112.112.112`
* **IPv6:** `2620:fe::fe`, `2620:fe::9`

**OpenDNS** (Now Cisco Umbrella)

* **IPv4:** `208.67.222.222`, `208.67.220.220`, `208.67.222.220`, `208.67.220.222`
* **IPv6:** `2620:119:35::35`, `2620:119:53::53`

### 🧠 Performance & Maintenance Features

* **Caching:**
* Adding RAM to a DNS server allows it to store more answers. If 50 people visit the same website, the server only asks the internet once and serves the cached answer 49 times.


* **Dynamic Registration:**
* Workstations often get new IPs via DHCP. They need to update their DNS records automatically so other computers can find them. This is standard in Active Directory environments but is also available in Linux (BIND) via **RFC 2136**.


* **Host Redundancy (Zone Transfers):**
* You should always have a primary and a secondary server.
* **Zone Transfer:** The process where the secondary server copies the entire database from the primary server to stay in sync. This ensures that if one server goes down for maintenance, users can still browse the web.



---

## 🌍 2. The Internet-Facing DNS Server

An **Internet-Facing DNS Server** has a totally different job. It is an **Authoritative Server**. It is "the end of the line" for a specific domain (e.g., `example.com`). It doesn't ask questions; it answers them.

Because it faces the public internet, the focus shifts from **performance** to **maximum security**.

### 🔒 Key Restrictions & Security Configurations

* **Restrict Recursion (CRITICAL):**
* This server should **NEVER** answer a query for a domain it doesn't host.
* If someone asks your server for `google.com`, it should refuse. It is only there to answer for `your-company.com`.


* **Cache is Less Important:**
* Since it only hosts specific zones, it doesn't need a massive cache for the whole internet. It only needs enough RAM to load its own zone files.


* **Restrict Zone Transfers:**
* **The Risk:** A "Zone Transfer" asks for a list of *every single host* in your domain.
* **The Fix:** You should block this for the general public. Only your own Backup/Secondary DNS servers should be allowed to request a zone transfer. There is no reason for a stranger on the internet to need a list of all your servers.


* **Restrict Dynamic Registration:**
* Never allow public devices to register their own names. This is a massive security risk. (Exceptions exist for specialized Dynamic DNS providers like DynDNS or No-IP, but they use custom authentication agents).



### 🛡️ Rate Limiting (RRL)

**Response Rate Limiting (RRL)** is a feature that limits how often a single IP address can query your server.

**Why is this necessary?**

1. **Preventing Amplification Attacks:**
* DNS uses **UDP**, which is "connectionless" (no handshake).
* Attackers can spoof a target's IP address and send small requests to your DNS server.
* Your server replies with a large answer (like a TXT record) to the *victim*.
* RRL stops your server from being used as a weapon in these "reflection" attacks.


2. **Stopping Reconnaissance:**
* Hackers often use automated scripts to guess subdomains (`admin.example.com`, `test.example.com`) to map your network. Rate limiting slows this process down significantly.

---

# 🛠️ Common DNS Implementations & Building an Internal BIND Server

## 📘 Overview

In the Linux world, there are two primary ways to implement DNS. Depending on the size of your organization and your specific needs (like blocking ads or integrating with DHCP), you will likely choose one of the following:

### 1. BIND (named)

* **Full Name:** Berkeley Internet Name Domain.
* **Process Name:** `named` (Name Daemon).
* **Reputation:** The "Gold Standard." It is the most flexible, complete, and widely used DNS server on the internet.
* **Pros:** Extremely powerful, standard in enterprise environments.
* **Cons:** Can be difficult to configure and troubleshoot due to its complexity.
* **Usage:** Used for both internal corporate DNS and public internet-facing DNS.

### 2. Dnsmasq (DNS Masquerade)

* **Reputation:** The "Lightweight Champion."
* **Usage:** Commonly found on home routers, firewalls, and IoT devices (like the Raspberry Pi).
* **Key Features:**
* **DHCP Integration:** It can handle both DNS and IP address assignment (DHCP). It automatically updates DNS records when a device gets a new IP.
* **Blocklists:** It is the engine behind **Pi-hole**, a popular tool for blocking ads and tracking domains network-wide.
* **Small Footprint:** Uses very little RAM and CPU.



---

## 🏗️ Step-by-Step: Installing & Configuring BIND

In this guide, we will focus on **BIND** to build a standard **Internal DNS Server**.

### 1️⃣ Installation

Installing BIND on Ubuntu is a single command.

**Command:**

```bash
hashim@Hashim:~$ sudo apt install bind9 -y
```

### 2️⃣ Understanding the Configuration Structure

Unlike older versions that used one giant file, modern BIND splits configuration into logical pieces. The main file `/etc/bind/named.conf` simply "includes" other files.

**Command:**

```bash
hashim@Hashim:~$ sudo cat /etc/bind/named.conf
```

**Output:**

```c
// This is the primary configuration file for the BIND DNS server named.
// ...
// If you are just adding zones, please do that in /etc/bind/named.conf.local

include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
include "/etc/bind/named.conf.default-zones";
```

* **`named.conf.options`**: Global server settings (who can query, who to forward to).
* **`named.conf.local`**: Definitions for your specific domains (zones).
* **`named.conf.default-zones`**: Standard zones like `localhost`.

---

### 3️⃣ Step 3: Configuring Global Options

We edit `/etc/bind/named.conf.options` to define how the server behaves.

**Key Changes:**

1. **ACL "trusted":** Define who is allowed to talk to us (e.g., our internal subnets).
2. **Forwarders:** If we don't know the answer (like `google.com`), ask Google (`8.8.8.8`) or Cloudflare (`1.1.1.1`).
3. **Allow-query:** Restrict questions to `localhost` and our internal subnet (`10.0.2.0/24`).
4. **Listen-on:** Listen on port 53 (standard DNS).
5. **Recursion:** Set to `yes` (required for internal servers so they can look up external websites).

**Command:**

```bash
hashim@Hashim:~$ cat /etc/bind/named.conf.options
```

**File Content:**

```c
options {
	directory "/var/cache/bind";

	// If there is a firewall between you and nameservers you want
	// to talk to, you may need to fix the firewall to allow multiple
	// ports to talk.  See http://www.kb.cert.org/vuls/id/800113

	// If your ISP provided one or more IP addresses for stable 
	// nameservers, you probably want to use them as forwarders.  
	// Uncomment the following block, and insert the addresses replacing 
	// the all-0's placeholder.

	forwarders { 8.8.8.8; 8.8.4.4; 1.1.1.1; };
	
	allow-query { localhost; 10.0.2.0/24; };

	//========================================================================
	// If BIND logs error messages about the root key being expired,
	// you will need to update your keys.  See https://www.isc.org/bind-keys
	//========================================================================
	dnssec-validation no;
	
	listen-on port 53 { 127.0.0.1; 10.0.2.15; };
        
        recursion yes;
 
	// listen-on-v6 { any; };
};
```

---

### 4️⃣ Step 4: Defining the Local Zone

We need to tell BIND that we are the "Master" (Authoritative) server for the domain `hashim.net`. We verify this in `/etc/bind/named.conf.local`.

**Command:**

```bash
hashim@Hashim:~$ cat /etc/bind/named.conf.local
```

**File Content:**

```c
//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";

// Hashim.net Zone Declaration
zone "hashim.net" IN {
    type master;             // Hum iske Maalik (Master) hain
    file "/var/cache/bind/hashim.net.zone";  // Asal file kahan hogi?
    allow-update { none; };
};
```

* **`type master;`**: We hold the original copy of the data.
* **`file ...`**: This points to where the actual list of IP addresses is stored.

---

### 5️⃣ Step 5: Creating the Zone File

This is the "Address Book." It maps names (like `gateway` or `pc1`) to IP addresses. The file is located at `/var/cache/bind/hashim.net.zone`.

**Key Components:**

* **SOA (Start of Authority):** Describes the domain administrator and settings.
* **Serial:** A number you increase every time you edit the file (so secondary servers know to update).
* **NS (Name Server):** Who is the DNS server? (`ns1.hashim.net`).
* **A (Address) Records:** The actual mappings (e.g., `gateway` -> `10.0.2.1`).

**Command:**

```bash
hashim@Hashim:~$ cat /var/cache/bind/hashim.net.zone
```

**File Content:**

```text
;
; BIND data file for local loopback interface
;$TTL	604800
@	IN	SOA	localhost. root.localhost. (
			      2		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	ns1.hashim.net.
ns1       IN      A       10.0.2.15
gateway   IN      A       10.0.2.1
pc1       IN      A       10.0.2.5
```

---

### 6️⃣ Step 6: Restart and Verify

Finally, we restart the service and test it using `dig` (Domain Information Groper).

**1. Restart Service:**

```bash
hashim@Hashim:~$ sudo systemctl restart bind9
```

**2. Check Status:**

```bash
hashim@Hashim:~$ sudo systemctl status bind9
```

**Output Analysis:**

```text
● named.service - BIND Domain Name Server
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; preset: enabled)
     Active: active (running) since Sat 2026-01-17 09:42:42 PKT; 65ms ago
 ...
Jan 17 09:42:42 Hashim named[3964]: zone hashim.net/IN: loaded serial 2
Jan 17 09:42:42 Hashim named[3964]: all zones loaded
```

* **Active (running):** The server started successfully.
* **loaded serial 2:** It successfully read our `hashim.net` zone file.

**3. Test Query (`dig`):**
We ask our new server (`@10.0.2.15`) for the IP of `gateway.hashim.net`.

```bash
hashim@Hashim:~$ dig @10.0.2.15 gateway.hashim.net
```

**Output:**

```text
; <<>> DiG 9.20.11-0ubuntu0.2-Ubuntu <<>> @10.0.2.15 gateway.hashim.net
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 51396
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; ANSWER SECTION:
gateway.hashim.net.	604800	IN	A	10.0.2.1

;; Query time: 3 msec
;; SERVER: 10.0.2.15#53(10.0.2.15) (UDP)
```

* **status: NOERROR**: Success!
* **ANSWER SECTION**: It correctly returned `10.0.2.1`.

---

# 🌐 BIND: Internet-Facing Implementation Specifics

## 📘 Overview

Hosting your own internet-facing DNS server was the standard method in the 1990s. Today, it is much less common.

### ☁️ Modern Approach: Cloud DNS (Registrars)

Most organizations now use their DNS Registrar (like GoDaddy, Cloudflare, or AWS Route53) to host their DNS zones.

* **Pros:** Simplified maintenance and better security (handled by the provider).
* **Security Requirement:** If you use a cloud provider, you **must** enable **Multi-Factor Authentication (MFA)** to prevent credential stuffing attacks. Also, verify their account recovery process so an attacker cannot simply "call helpdesk" to steal your domain.

### 🏢 Legacy/Specialized Approach: Self-Hosted DNS

Despite the cloud trend, many organizations still have valid use cases for hosting their own DNS (e.g., specific compliance needs, complex hybrid environments, or learning purposes).

We will now modify our **Internal** BIND configuration to act as a **Public Internet-Facing** server.

---

## ⚙️ Configuration Changes

We need to edit the main options file: `/etc/bind/named.conf.options`.

### 1️⃣ Rate Limiting (RRL)

**Response Rate Limiting (RRL)** protects your server from being used in DDoS attacks (amplification/reflection attacks).

* **Logic:** A normal user won't ask for the same domain 10 times in one second. If an IP does this, they are likely attacking.
* **Configuration Strategy:**
* Set `responses-per-second` (e.g., 10).
* Start with `log-only yes;`. This logs potential blocks to `/var/log/syslog` without actually blocking traffic.
* Monitor logs. If legitimate traffic is getting flagged, increase the limit. If only attacks are flagged, remove `log-only` to enforce the block.



**Code:**

```nginx
rate-limit {
    responses-per-second 10;
    log-only yes;
}
```

### 2️⃣ Disable Recursion & Forwarding (Critical)

A public authoritative server must **never** resolve random internet domains for strangers. If it does, it becomes an "Open Resolver," which is a major security vulnerability.

* **Recursion:** Set to `no`.
* **Forwarders:** Remove the section entirely. We don't ask Google/Cloudflare for help anymore.

**Code:**

```nginx
recursion no;
```

### 3️⃣ Allow Query from Anywhere

Since this server is for the public internet, we must allow anyone (`0.0.0.0/0` or `any`) to ask us questions about *our* domain.

**Code:**

```nginx
allow-query { localhost; 0.0.0.0/0; };
```

---

## 🛠️ Step-by-Step Implementation & Analysis

### 1. Editing & Restarting the Service

We edit the file, restart the service to apply changes, and check if it is running.

**Commands:**

```bash
hashim@Hashim:~$ sudo nano /etc/bind/named.conf.options
hashim@Hashim:~$ sudo systemctl restart bind9
hashim@Hashim:~$ sudo systemctl status bind9
```

**Output Analysis:**

```text
● named.service - BIND Domain Name Server
     Loaded: loaded ... enabled; preset: enabled)
     Active: active (running) since Mon 2026-01-19 16:21:52 PKT; 7s ago
...
Jan 19 16:21:52 Hashim named[3516]: zone hashim.net/IN: loaded serial 2
```

* **Active (running):** The server restarted successfully with the new config.
* **loaded serial 2:** It successfully loaded our authoritative zone `hashim.net`.

---

### 2. Reviewing the Configuration File

Let's look at the final configuration file to understand exactly what we changed.

**Command:**

```bash
hashim@Hashim:~$ sudo cat /etc/bind/named.conf.options
```

**Output Breakdown:**

```nginx
acl "trusted" {
    10.0.2.15;
    10.0.2.20;
};

options {
    directory "/var/cache/bind";

    // 1. Rate Limiting (Security)
    // Limits responses to 10 per second to prevent DDoS usage.
    // Currently in 'Audit Mode' (log-only) so we don't accidentally block real users.
    rate-limit {
        responses-per-second 10;
        log-only yes;
    };

    // 2. Allow Query (Open to World)
    // Changed from specific subnets to 'any' because the whole world needs to see this.
    allow-query { any; };

    // 3. Listening Port
    listen-on port 53 { any; };
    listen-on-v6 { any; };

    // 4. Recursion & Forwarding (CRITICAL CHANGE)
    // Disabled recursion. This prevents the server from looking up google.com for others.
    // Forwarders block is removed.
    recursion no;
     
    // Security setting
    dnssec-validation no;
};
```

---

### 3. Verification Test 1: Querying an Authoritative Domain

We ask the server for a record it **owns** (`gateway.hashim.net`). This should work.

**Command:**

```bash
hashim@Hashim:~$ dig @10.0.2.15 gateway.hashim.net
```

**Output Analysis:**

```text
; <<>> DiG 9.20.11-0ubuntu0.2-Ubuntu <<>> @10.0.2.15 gateway.hashim.net
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41755
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available
```

* **status: NOERROR:** The request was successful.
* **flags: aa:** "Authoritative Answer." The server is saying, "I know this because I own this domain."
* **WARNING: recursion requested but not available:** `dig` asked for recursion by default, but our server correctly said "No" (because we set `recursion no;`).
* **ANSWER SECTION:** It returned `10.0.2.1`. **Success.**

---

### 4. Verification Test 2: Querying an External Domain (The "Recursion" Test)

Now we ask the server for a domain it **does not** own (`google.com`). Since we disabled recursion, this **must fail**.

**Command:**

```bash
hashim@Hashim:~$ dig @10.0.2.15 google.com
```

**Output Analysis:**

```text
; <<>> DiG 9.20.11-0ubuntu0.2-Ubuntu <<>> @10.0.2.15 google.com
;; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 24902
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

; EDE: 20 (Not Authoritative): (recursion disabled)

```

* **status: REFUSED:** The server rejected the request. This is exactly what we want!
* **ANSWER: 0:** No IP address was provided.
* **Reason:** The server does not own `google.com`, and it is not allowed to go ask other servers for it.

**Conclusion:** The server is now correctly configured as a secure, internet-facing Authoritative DNS server.

---

# 🔍 DNS Troubleshooting and Reconnaissance

## 📘 Overview

The primary tool in Linux for troubleshooting DNS services is **`dig`** (Domain Information Groper).

* **Availability:** It comes pre-installed on almost all Linux distributions.
* **Installation:** If it is missing, you can install it using the `dnsutils` package.

**Command:**

```bash
sudo apt install dnsutils
```

The usage is straightforward: `dig @<server_ip> <domain_name> <record_type>`.

---

## 🛠️ Deep Dive: The Full DNS Query (`NS` Record)

Let's find the **Name Server (NS)** records for our local domain `hashim.net`. We will query our local server (`10.0.2.15`).

**Command:**

```bash
hashim@hashim-server:~$ dig @10.0.2.15 hashim.net ns
```

**Output:**

```text
; <<>> DiG 9.18.39-0ubuntu0.24.04.2-Ubuntu <<>> @10.0.2.15 hashim.net ns
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 51701
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 2
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: d066135d27c4605301000000696f0bb6cbc3a6f01791e25d (good)
;; QUESTION SECTION:
;hashim.net.			IN	NS

;; ANSWER SECTION:
hashim.net.		604800	IN	NS	ns1.hashim.net.

;; ADDITIONAL SECTION:
ns1.hashim.net.		604800	IN	A	10.0.2.15

;; Query time: 0 msec
;; SERVER: 10.0.2.15#53(10.0.2.15) (UDP)
;; WHEN: Tue Jan 20 04:59:34 UTC 2026
;; MSG SIZE  rcvd: 101
```

### 🧐 Detailed Output Analysis

The `dig` output is verbose but extremely valuable. Here is what every section means:

**1. The Header & Status**

* `status: NOERROR`: The query was successful.
* `id: 51701`: A unique transaction ID to match the request with the response.

**2. The Flags (Crucial for Troubleshooting)**

* `qr` (Query Response): This is a reply, not a question.
* **`aa` (Authoritative Answer):** This is the most important flag here. It means the server (`10.0.2.15`) **owns** this domain. It is not passing along a rumor; it is the source of truth.
* `rd` (Recursion Desired): The client asked for recursion.
* **`WARNING: recursion requested but not available`**: This confirms our configuration from the previous section. We explicitly set `recursion no;`, so the server correctly warned us that it won't perform recursion.

**3. Question Section**

* `;hashim.net. IN NS`: We asked for the **NS** records for `hashim.net`.

**4. Answer Section**

* `hashim.net. 604800 IN NS ns1.hashim.net.`: The server replied: "The name server for this domain is `ns1.hashim.net`."
* `604800`: This is the **TTL (Time to Live)** in seconds.

**5. Additional Section (Glue Records)**

* `ns1.hashim.net. ... IN A 10.0.2.15`: The server was helpful. It realized that telling you "go to ns1" isn't helpful if you don't know where `ns1` is. So, it provided the IP address for `ns1` (`10.0.2.15`) automatically.

---

## ⚡ The Short Output (`+short`)

Sometimes you don't need the metadata; you just want the answer. We use the `+short` parameter for this.

### 1. Local Query (Hashim.net)

**Command:**

```bash
hashim@hashim-server:~$ dig @10.0.2.15 hashim.net ns +short
```

**Output:**

```text
ns1.hashim.net.
```

* **Result:** Simple and clean.

### 2. External Query (Google.com)

Now let's ask a public DNS server (`8.8.8.8`) for Google's name servers.

**Command:**

```bash
hashim@hashim-server:~$ dig @8.8.8.8 google.com ns +short
```

**Output:**

```text
ns3.google.com.
ns4.google.com.
ns1.google.com.
ns2.google.com.
```

* **Result:** Google has multiple redundant name servers (ns1-ns4) for reliability.

---

## 📧 Mail Exchanger (`MX`) Queries

The `dig` command can query any record type. To find out which servers handle email for a domain, we look up the **MX** record.

### 1. Querying Local Server for MX (Hashim.net)

**Command:**

```bash
hashim@hashim-server:~$ dig @10.0.2.15 hashim.net mx +short
```

**Output:**
*(Empty)*

* **Reason:** We never added an MX record to our `hashim.net.zone` file in the previous configuration steps! The server correctly returns nothing because no record exists.

### 2. Querying Local Server for External MX (Google.com)

**Command:**

```bash
hashim@hashim-server:~$ dig @10.0.2.15 google.com mx +short
```

**Output:**
*(Empty)*

* **Reason:** Our server has `recursion no;` enabled. It cannot go out to the internet to find Google's mail servers, so it refuses to answer or returns nothing.

### 3. Querying Public Server for Gmail MX

Let's ask Google (`8.8.8.8`) about Gmail's mail servers.

**Command:**

```bash
hashim@hashim-server:~$ dig @8.8.8.8 gmail.com mx +short
```

**Output:**

```text
20 alt2.gmail-smtp-in.l.google.com.
40 alt4.gmail-smtp-in.l.google.com.
30 alt3.gmail-smtp-in.l.google.com.
10 alt1.gmail-smtp-in.l.google.com.
5 gmail-smtp-in.l.google.com.
```

* **Result:** The numbers (5, 10, 20...) are **Priorities**.
* **Logic:** Mail servers try to connect to the server with the **lowest number** (5) first. If that fails, they try the next lowest (10), and so on. This provides failover redundancy.

---

# 🔒 DNS over HTTPS (DoH)

## 📘 Overview

**DNS over HTTPS (DoH)** is a newer protocol that performs DNS resolution via the HTTPS protocol. Unlike traditional DNS, which uses UDP or TCP on port 53, DoH encapsulates DNS queries within secure HTTP traffic on **port 443**.

**Key Characteristics:**

* **API-Like Structure:** DoH queries and responses look like standard **Application Programming Interface (API)** calls (specifically JSON) rather than raw network packets.
* **Browser-First Adoption:** This protocol was first supported directly in web browsers (like Chrome and Firefox) before being added to operating systems.
* **Current Status:** It is now available on most mainstream operating systems, though it is often **not enabled by default**.

---

## 🛠️ Verifying DoH with `curl`

Since DoH uses standard web protocols, we can use the `curl` command (a tool for transferring data with URLs) to interact with a DoH server directly.

### 1️⃣ The Raw Query

In this example, we query the **Cloudflare Public DNS** server (`1.1.1.1`) for the domain `www.coherentsecurity.com`.

**Command:**

```bash
curl -s -H 'accept: application/dns-json' 'https://1.1.1.1/dns-query?name=www.coherentsecurity.com&type=A'
```

**Command Breakdown:**

* **`curl`**: The command-line tool.
* **`-s` (Silent)**: Mutes the progress bar/error messages.
* **`-H 'accept: application/dns-json'`**: Sends an HTTP Header telling the server, "Please reply with JSON data.".
* **The URL**:
* **Protocol**: `https://` (Port 443).
* **Endpoint**: `/dns-query`.
* **Parameters**: `?name=...` (The domain to look up) and `&type=A` (Look for an IPv4 address).



**Output:**

```json
{"Status":0,"TC":false,"RD":true,"RA":true,"AD":
false,"CD":false,"Question":[{"name":"www.coherentsecurity.
com","type":1}],"Answer":[{"name":"www.coherentsecurity.
com","type":5,"TTL":1693,"data":"robvandenbrink.github.
io."},{"name":"robvandenbrink.github.io","type":1,
"TTL":3493,"data":"185.199.108.153"},{"name":"robvandenbrink.
github.io","type":1,"TTL":3493,"data":"185.199.109.153"},
{"name":"robvandenbrink.github.io","type":1,"TTL":3493,"data":
"185.199.110.153"},{"name":"robvandenbrink.github.
io","type":1,"TTL":3493,"data":"185.199.111.153"}]}
```

**Analysis:**
The output is a raw JSON string. It confirms the server received the HTTPS request and returned DNS data, but it is difficult for a human to read.

---

### 2️⃣ Making it Readable with `jq`

To understand the flags and data, we pipe the output into `jq`, a command-line JSON processor.

**Command:**

```bash
curl -s -H 'accept: application/dns-json' 'https://1.1.1.1/dns-query?name=www.coherentsecurity.com&type=A' | jq
```

**Output:**

```json
{
 "Status": 0,
 "TC": false,
 "RD": true,
 "RA": true,
 "AD": false,
 "CD": false,
 "Question": [
 {
 "name": "www.coherentsecurity.com",
 "type": 1
 }
 ],
 "Answer": [
 {
 "name": "www.coherentsecurity.com",
 "type": 5,
 "TTL": 1792,
 "data": "robvandenbrink.github.io."
 },
 ….
 {
 "name": "robvandenbrink.github.io",
 "type": 1,
 "TTL": 3592,
 "data": "185.199.111.153"
 }
 ]
}
```

**Detailed Breakdown of Fields:**

* **`Status: 0`**: Success (No Error).
* **`TC: false` (Truncated)**: The message was not cut off.
* **`RD: true` (Recursion Desired)**: The client (curl) asked the server to chase down the answer if it didn't know it.
* **`RA: true` (Recursion Available)**: The server (Cloudflare) confirmed it *is* capable of recursion.
* **`Question`**: Confirms we asked for an A Record (`type: 1`) for `www.coherentsecurity.com`.
* **`Answer`**:
* **Type 5 (CNAME)**: `www.coherentsecurity.com` is an alias for `robvandenbrink.github.io`.
* **Type 1 (A Record)**: `robvandenbrink.github.io` resolves to the IP `185.199.111.153` (and others).



---

## 🔍 Verifying the Certificate with Nmap

Since DoH relies on HTTPS, you can use **Nmap** to verify the SSL/TLS certificate of the DoH server. This ensures you are talking to the real provider (e.g., Cloudflare) and not an imposter.

**Command:**

```bash
nmap -p443 1.1.1.1 --script ssl-cert.nse
```

**Output:**

```text
Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-25 11:28
Eastern Standard Time
Nmap scan report for one.one.one.one (1.1.1.1)
Host is up (0.029s latency).
PORT STATE SERVICE
443/tcp open https
| ssl-cert: Subject: commonName=cloudflaredns.com/organizationName=Cloudflare, Inc./
stateOrProvinceName=California/countryName=US
| Subject Alternative Name: DNS:cloudflare-dns.com, DNS:*.
cloudflare-dns.com, DNS:one.one.one.one, IP Address:1.1.1.1,
IP Address:1.0.0.1, IP Address:162.159.36.1, IP
Address:162.159.46.1, IP Address:2606:4700:4700:0:0:0:0:1111,
IP Address:2606:4700:4700:0:0:0:0:1001, IP Address:2606:4700:47
00:0:0:0:0:64, IP Address:2606:4700:4700:0:0:0:0:6400
| Issuer: commonName=DigiCert TLS Hybrid ECC SHA384 2020 CA1/
organizationName=DigiCert Inc/countryName=US
| Public Key type: unknown
| Public Key bits: 256
| Signature Algorithm: ecdsa-with-SHA384
| Not valid before: 2021-01-11T00:00:00
| Not valid after: 2022-01-18T23:59:59
| MD5: fef6 c18c 02d0 1a14 ab75 1275 dd6a bc29
|_SHA-1: f1b3 8143 b992 6454 97cf 452f 8c1a c842 4979 4282
Nmap done: 1 IP address (1 host up) scanned in 7.41 seconds
```

**Output Analysis:**

* **Port 443:** Open (HTTPS service).
* **Subject:** Confirms the certificate belongs to `cloudflaredns.com` and `Cloudflare, Inc`.
* **Subject Alternative Name (SANs):** Lists other valid names/IPs for this cert, including `1.1.1.1`, `1.0.0.1`, and IPv6 addresses. This confirms the server identity matches the IP we queried.

---

## 🚀 Advanced: Custom Nmap Scripts for DoH

Standard Nmap scripts (`ssl-cert.nse`) only verify the *encryption tunnel* (SSL), not the actual *DoH service*. To verify that the server is actually answering DNS queries over HTTPS, you can use a custom script.

* **Script Name:** `dns-doh.nse`
* **Source:** Available on GitHub (`robvandenbrink/dns-doh.nse`).
* **Function:**
1. Verifies the port is servicing HTTP.
2. Constructs the specific query string.
3. Makes the HTTPS request with the correct headers.



This fills the gap in Nmap's default capabilities for auditing DoH servers.

---

# 🔒 DNS over TLS (DoT)

## 📘 Overview

**DNS over TLS (DoT)** is the standard DNS protocol, but it is encapsulated within a **Transport Layer Security (TLS)** tunnel.

* **Dedicated Port:** Unlike DoH (which hides inside HTTPS traffic on port 443), DoT uses its own dedicated port: **TCP/853**.
* **Co-existence:** Because it uses a unique port (853), it does not conflict with standard DNS (UDP/53) or DoH (TCP/443). A single server can easily run all three services simultaneously.
* **Client Support:** Most modern operating systems support DoT, though it often needs to be manually enabled in settings.

---

## 🛠️ Verification Method 1: Basic Port Scan

The simplest way to check if a server supports DoT is to verify if **Port 853** is open and listening.

**Command:**

```bash
nmap -p 853 8.8.8.8
```

**Output Analysis:**

```text
Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-21 13:33 PST
Nmap scan report for dns.google (8.8.8.8)
Host is up (0.023s latency).
PORT    STATE SERVICE
853/tcp open  domain-s
```

* **`853/tcp open`**: The port is accessible.
* **`domain-s`**: This is the IETF standard name for "DNS over Secure Sockets Layer," confirming the service type.

---

## 🕵️ Verification Method 2: Service Version Detection (`-sV`)

We can try to identify exactly what software or version is running behind that port.

**Command:**

```bash
nmap -p 853 -sV 8.8.8.8
```

**Output Analysis:**

```text
PORT    STATE SERVICE    VERSION
853/tcp open  ssl/domain (generic dns response: NOTIMP)
1 service unrecognized despite returning data...
...
SF:%r(DNSVersionBindReqTCP...
SF:ersion\x04bind...
SF:x04\0\0\0\0\0\0\0\0");
```

* **"Service Unrecognized":** Nmap (at the time of writing) didn't have a perfect signature match for Google's specific implementation, so it flagged it as unrecognized.
* **The Clue (`DNSStatusRequestTCP`):** Even though Nmap complained, the "Fingerprint" data (`SF`) contains the string `DNSStatusRequestTCP`. This technical detail proves that the server is indeed responding to DNS commands over that TCP connection. It is a "nice clue" that confirms DoT is active.

---

## 🔐 Verification Method 3: Certificate Inspection

Since DoT uses TLS (just like HTTPS websites), it must have a digital certificate to prove its identity. We can inspect this certificate to ensure we aren't being tricked by a Man-in-the-Middle attacker.

**Command:**

```bash
nmap -p853 --script ssl-cert 8.8.8.8
```

**Output Analysis:**

```text
| ssl-cert: Subject: commonName=dns.google/
| organizationName=Google LLC/stateOrProvinceName=California/
| countryName=US
| Subject Alternative Name: DNS:dns.google, DNS:*.dns.google.com, 
| IP Address:8.8.8.8, ...
| Issuer: commonName=GTS CA 1O1 ...
| Not valid before: 2021-01-26 ...
| Not valid after: 2021-04-20 ...
```

* **`Subject: commonName=dns.google`**: Proof that this server is actually Google's DNS.
* **`Subject Alternative Name`**: Lists all other IPs (like `8.8.4.4` and IPv6 addresses) that are allowed to use this specific certificate.
* **`Issuer`**: Specifies who signed the certificate (Google Trust Services).
* **Validity Dates**: Confirms the certificate is currently valid (not expired).

---

## 🧰 The Limitation of `dig` & The Solution (`kdig`)

At the time of writing, the standard Linux `dig` tool **cannot** make DoT queries. It only understands plain DNS (UDP/53).

To actually test DoT functionality (sending a query and getting an answer), we need a different tool called **`kdig`**, which is part of the `knot-dnsutils` package. This tool acts as an "advanced dig" capable of speaking TLS.

---