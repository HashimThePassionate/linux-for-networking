# 🏴‍☠️ Lab: ARP Cache Poisoning:

**Topic:** ARP Spoofing / Cache Poisoning

**Source Context:** Based on Figure 11.3 - ARP cache poisoning and Chapter 11 text.

**Environment:** Ubuntu 22.04/24.04 (VirtualBox Bridged Mode)

**Attacker IP:** `192.168.1.19` (Your Machine)

---

## 🌍 1. Real-World Scenario: "The Classroom Prankster"

To fully grasp this concept, visualize a classroom environment:

* **Teacher (Router/Gateway):** Needs to send messages (Internet traffic) to the entire class.
* **Student A (Victim):** Wants to receive their specific message from the Teacher.
* **Student B (Attacker - You):** The malicious student sitting in between.

### The Normal Process

1. **Teacher asks:** "Who is Student A?"
2. **Student A raises their hand:** "I am!"
3. **Teacher:** Hands the message directly to Student A.

### The ARP Poisoning Attack

1. **Teacher asks:** "Who is Student A?"
2. **Interruption:** Before Student A can speak, **Student B (Attacker)** shouts loudly: **"I am Student A!"**
3. **Deception:** simultaneously, Student B whispers to Student A: **"I am the Teacher!"**

**The Result:**

* The **Teacher** hands messages to **Student B**, believing they are Student A.
* **Student A** hands their replies to **Student B**, believing they are the Teacher.
* **Student B** reads all the messages in the middle and then passes them along so no one suspects the theft.

In the world of networking, this "Lying" is accomplished using **ARP Packets**.

---

## 🛠️ 2. Hands-on Ubuntu Lab

In this laboratory exercise, we will use the `arpspoof` tool (part of the `dsniff` suite mentioned in the textbook). We will configure your machine (`192.168.1.19`) to act as the Attacker, intercepting traffic between the Gateway and another device (e.g., your mobile phone).

### Step 1: Tool Installation

First, we must install the `dsniff` package, which contains the `arpspoof` utility.

**Command:**

```bash
sudo apt update && sudo apt install dsniff -y

```

**Detailed Explanation:**

* `sudo apt update`: Refreshes your package lists to ensure you download the latest version.
* `&&`: Logical operator that runs the second command only if the first succeeds.
* `sudo apt install dsniff -y`: Installs the suite. Although the text notes `dsniff` is an older tool, it remains excellent for understanding the core concepts of spoofing.

### Step 2: Enable IP Forwarding (Crucial Step!)

If we intercept traffic but do not pass it on, the victim's internet connection will drop, and they will become suspicious. We must configure our machine to forward traffic.

**Command:**

```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

```

**Expected Output:**

```text
1

```

**Detailed Explanation:**

* **Default Behavior:** By default, Linux drops network traffic that is not destined for itself.
* **The Command:** This instructs the kernel to set the `ip_forward` value to `1`.
* **Result:** This tells the kernel: *"If traffic arrives that isn't for me, send it to its actual destination."* Effectively, this turns your machine into a **Router**.

### Step 3: Identify Targets

We need to identify two key players: the Network Gateway and the Target (Victim).

**1. Find the Gateway:**

```bash
ip route show | grep default

```

* **Output Example:** `default via 192.168.1.1 dev enp0s3 ...`
* **Note:** For this lab, we assume the Gateway is `192.168.1.1`.

**2. Find the Target (Victim):**
Identify the IP address of another device on your network (e.g., your smartphone).

* **Assumption:** Let's assume the Victim's IP is `192.168.1.25`.

### Step 4: Launch the Attack (ARP Spoofing)

We need to open **two separate terminals** to perform "Two-way Spoofing" (as illustrated in Figure 11.3).

#### Terminal 1: Deceiving the Victim

*Message:* "I am the Router."

**Command:**

```bash
# Syntax: arpspoof -i [Interface] -t [Victim IP] [Gateway IP]
sudo arpspoof -i enp0s3 -t 192.168.1.25 192.168.1.1

```

**Detailed Explanation:**

* `-i enp0s3`: Specifies your network interface.
* `-t 192.168.1.25`: Targets the Victim.
* `192.168.1.1`: The IP we are pretending to be (The Gateway).
* **Result:** This sends continuous ARP packets to the Victim saying, *"I am the Router (192.168.1.1)."* The Victim will now send all internet requests to **You** (`192.168.1.19`).

#### Terminal 2: Deceiving the Router

*Message:* "I am the Victim."

**Command:**

```bash
# Syntax: arpspoof -i [Interface] -t [Gateway IP] [Victim IP]
sudo arpspoof -i enp0s3 -t 192.168.1.1 192.168.1.25

```

**Detailed Explanation:**

* `-t 192.168.1.1`: Targets the Router.
* `192.168.1.25`: The IP we are pretending to be (The Victim).
* **Result:** This tells the Router, *"I am the Victim (192.168.1.25)."* When the Router receives data from the internet for the victim, it sends it to **You** instead.

### Step 5: Monitor the Traffic

Since all traffic is now flowing through your machine, you can inspect it.

**Command:**

```bash
# Example: Watch traffic to/from the victim
sudo tcpdump -i enp0s3 host 192.168.1.25

```

**Detailed Explanation:**

* This command displays live traffic originating from or destined for the Victim's phone. You will see their requests passing through your terminal.

---

## 🔍 3. Behind the Scenes (Technical Context)

When you execute these commands, the background activity mirrors **Figure 11.3**:

1. **Cache Poisoning:** You are forcibly injecting your MAC address (e.g., `33:33...`) into the Victim's ARP table.
2. **Man-in-the-Middle (MitM):** The traffic flow changes physically:
* **Old Flow:** Victim ↔️ Router
* **New Flow:** Victim ↔️ **Attacker** ↔️ Router


3. **Gratuitous ARP:** The `arpspoof` tool utilizes "Gratuitous ARP" packets. These are unsolicited ARP replies—answers to questions that no one asked—sent forcibly to update the target's cache immediately.

> **⚠️ Important Note:**
> When you finish the lab, press **Ctrl+C** in the terminal to stop `arpspoof`. Upon exiting, the tool usually performs "re-arping." It sends correct ARP packets to restore the Victim's legitimate connection to the Router, ensuring they do not realize an attack occurred.