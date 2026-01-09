
import os

file_path = r"c:\Users\Hashim\Desktop\resources\linux-network\03-linux-tools-for-network-diagnostics\readme.md"

replacements = {
    "## 🎯 What We Will Cover": '## <a id="what-we-will-cover"></a>🎯 What We Will Cover',
    "## ⚙️ Technical Requirements": '## <a id="technical-requirements"></a>⚙️ Technical Requirements',
    "## 🧰 Your Network Diagnostic Toolkit": '## <a id="your-network-diagnostic-toolkit"></a>🧰 Your Network Diagnostic Toolkit',
    "### 🖥️ Native & Standard Linux Tools": '### <a id="native-standard-linux-tools"></a>🖥️ Native & Standard Linux Tools',
    "### 🔎 Advanced Scanning & Wireless Tools": '### <a id="advanced-scanning-wireless-tools"></a>🔎 Advanced Scanning & Wireless Tools',
    "## 🌐 Network Basics: The OSI Model": '## <a id="network-basics-the-osi-model"></a>🌐 Network Basics: The OSI Model',
    "### 📊 The 7 Layers of the OSI Model": '### <a id="the-7-layers-of-the-osi-model"></a>📊 The 7 Layers of the OSI Model',
    "### 🔄 Data Travel: Encapsulation & Decapsulation": '### <a id="data-travel-encapsulation--decapsulation"></a>🔄 Data Travel: Encapsulation & Decapsulation',
    "### 📦 Media Layers vs. Host Layers": '### <a id="media-layers-vs-host-layers"></a>📦 Media Layers vs. Host Layers',
    "## 🛡️ Layer 2: Relating IP and MAC Addresses Using ARP": '## <a id="layer-2-relating-ip-and-mac-addresses-using-arp"></a>🛡️ Layer 2: Relating IP and MAC Addresses Using ARP',
    "### 🆔 Understanding MAC Addresses": '### <a id="understanding-mac-addresses"></a>🆔 Understanding MAC Addresses',
    "### 📋 The ARP Cache: Viewing Your Local Table": '### <a id="the-arp-cache-viewing-your-local-table"></a>📋 The ARP Cache: Viewing Your Local Table',
    "### 📊 Viewing Network Statistics": '### <a id="viewing-network-statistics"></a>📊 Viewing Network Statistics',
    "### 🛠️ Managing ARP Entries Manually": '### <a id="managing-arp-entries-manually"></a>🛠️ Managing ARP Entries Manually',
    "### 🎭 Changing the MAC Address (Spoofing)": '### <a id="changing-the-mac-address-spoofing"></a>🎭 Changing the MAC Address (Spoofing)',
    "### 🛠️ Changing MAC Address via Udev Rules": '### <a id="changing-mac-address-via-udev-rules"></a>🛠️ Changing MAC Address via Udev Rules',
    "## 🏷️ MAC Address OUI Values": '## <a id="mac-address-oui-values"></a>🏷️ MAC Address OUI Values',
    "### 🧩 The Structure of a MAC Address": '### <a id="the-structure-of-a-mac-address"></a>🧩 The Structure of a MAC Address',
    "### 📚 The Registries: Who Tracks This?": '### <a id="the-registries-who-tracks-this"></a>📚 The Registries: Who Tracks This?',
    "### 🛠️ Tools for OUI Lookup": '### <a id="tools-for-oui-lookup"></a>🛠️ Tools for OUI Lookup',
    "## 🚦 Layer 4: How TCP and UDP Ports Work": '## <a id="layer-4-how-tcp-and-udp-ports-work"></a>🚦 Layer 4: How TCP and UDP Ports Work',
    "### 🔗 The Connection Process": '### <a id="the-connection-process"></a>🔗 The Connection Process',
    "### 🧩 The \"5-Tuple\" Concept": '### <a id="the-5-tuple-concept"></a>🧩 The "5-Tuple" Concept',
    "### 🔢 Port Number Ranges": '### <a id="port-number-ranges"></a>🔢 Port Number Ranges',
    "### 📋 Common Standard Ports": '### <a id="common-standard-ports"></a>📋 Common Standard Ports',
    "### 🏛️ The IANA Registry vs. Reality": '### <a id="the-iana-registry-vs-reality"></a>🏛️ The IANA Registry vs. Reality',
    "## 🤝 Layer 4: TCP and the Three-Way Handshake": '## <a id="layer-4-tcp-and-the-three-way-handshake"></a>🤝 Layer 4: TCP and the Three-Way Handshake',
    "### 🤝 The TCP Three-Way Handshake": '### <a id="the-tcp-three-way-handshake"></a>🤝 The TCP Three-Way Handshake',
    "### 🛑 Ending the Connection": '### <a id="ending-the-connection"></a>🛑 Ending the Connection',
    "## 🔍 Local Port Enumeration: What Am I Connected To?": '## <a id="local-port-enumeration-what-am-i-connected-to"></a>🔍 Local Port Enumeration: What Am I Connected To?',
    "### 💻 The Command: netstat -tuan": '### <a id="the-command-netstat--tuan"></a>💻 The Command: netstat -tuan',
    "### 🚦 Understanding TCP States": '### <a id="understanding-tcp-states"></a>🚦 Understanding TCP States',
    "## 🛠️ Advanced Port Enumeration: Linking Processes to Ports": '## <a id="advanced-port-enumeration-linking-processes-to-ports"></a>🛠️ Advanced Port Enumeration: Linking Processes to Ports',
    "### 🔍 Identifying the Process: netstat -tulpn": '### <a id="identifying-the-process-netstat--tulpn"></a>🔍 Identifying the Process: netstat -tulpn',
    "### 🚀 The Modern Alternative: ss": '### <a id="the-modern-alternative-ss"></a>🚀 The Modern Alternative: ss',
    "### ✂️ Advanced Formatting: Piping & Cutting": '### <a id="advanced-formatting-piping--cutting"></a>✂️ Advanced Formatting: Piping & Cutting',
    "### 🕵️ Troubleshooting with ss Options": '### <a id="troubleshooting-with-ss-options"></a>🕵️ Troubleshooting with ss Options',
    "### 📂 The \"Everything is a File\" Concept: lsof": '### <a id="the-everything-is-a-file-concept-lsof"></a>📂 The "Everything is a File" Concept: lsof',
    "## 🛠️ Remote Port Enumeration Using Native Tools": '## <a id="remote-port-enumeration-using-native-tools"></a>🛠️ Remote Port Enumeration Using Native Tools',
    "### 📞 Tool 1: Telnet (The Quick Check)": '### <a id="tool-1-telnet-the-quick-check"></a>📞 Tool 1: Telnet (The Quick Check)',
    "### 🐱 Tool 2: Netcat (nc) - The Swiss Army Knife": '### <a id="tool-2-netcat-nc---the-swiss-army-knife"></a>🐱 Tool 2: Netcat (nc) - The Swiss Army Knife',
    "### 🏗️ Netcat as a Server: Creating a Fake Website": '### <a id="netcat-as-a-server-creating-a-fake-website"></a>🏗️ Netcat as a Server: Creating a Fake Website',
    "### 📂 Transferring Files with Netcat": '### <a id="transferring-files-with-netcat"></a>📂 Transferring Files with Netcat',
    "## 📜 Nmap Scripting Engine (NSE) & Advanced Scanning": '## <a id="nmap-scripting-engine-nse--advanced-scanning"></a>📜 Nmap Scripting Engine (NSE) & Advanced Scanning',
    "### 🛡️ Case Study: Scanning for SMB Vulnerabilities": '### <a id="case-study-scanning-for-smb-vulnerabilities"></a>🛡️ Case Study: Scanning for SMB Vulnerabilities',
    "### 🧰 Essential Nmap Scripts for Administrators": '### <a id="essential-nmap-scripts-for-administrators"></a>🧰 Essential Nmap Scripts for Administrators',
    "### ⏳ The Limits of Nmap": '### <a id="the-limits-of-nmap"></a>⏳ The Limits of Nmap'
}

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

count = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        print(f"Warning: Could not find header: {old}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {count} headers.")
