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