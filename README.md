# Ultimate_Wordlist_Generator
Advanced wordlist generator with Smart, Brute-force, Hybrid, and Random modes. Built in Python by VivekXploit for ethical hacking, penetration testing, and CTF research

# 🔐 VivekXploit Ultimate Wordlist Generator

A powerful and customizable **wordlist generator tool** built in Python by **VivekXploit**.  
It can create personalized password lists, brute-force combinations, hybrid lists, or fully random strong passwords.  
Perfect for ethical hacking, penetration testing, CTFs, or security research.

---

## 📂 Project Structure
```bash
vivekxploit-wordgen/
│── wordGen.py # Main script (Wordlist Generator)
│── README.md # Documentation
│── requirements.txt # Python dependencies
│── LICENSE # Open-source license (MIT)
```

---

## ✨ Features
- 🎨 **Colorful ASCII Banner** (Zphisher-style experience)
- 🧠 **Smart Mode** → personalized wordlists from info (name, DOB, pet, etc.) with mutations & leetspeak
- 💣 **Brute-force Mode** → all possible combinations from selected charset
- ⚡ **Hybrid Mode** → Smart + controlled brute-force
- 🎲 **Random Mode** → strong random passwords
- 📊 **Progress bars** with live status
- 💾 **Unique output** (no duplicates)
- 📐 **Size estimator** (predicts file size before generation)
- ⌨️ **Interactive menu system**

---

## 📦 Installation

Clone this repository and install requirements:

```bash
git clone https://github.com/yourusername/Ultimate_Wordlist_Generator.git
cd Ultimate_Wordlist_Generator
pip install -r requirements.txt
```
## 📦 Run

Run the Script

```bash
python3 wordGen.py
```
You will see the menu:

## 🔍 Modes

    [1] Smart Wordlist (personal info → mutations)
    [2] Brute-force Wordlist (charset + length)
    [3] Hybrid (Smart + Controlled Brute)
    [4] Random Strong Passwords
    [0] Exit
---

## 📊 Example Run
```bash
>>> Smart Wordlist (personalized)
 Target Name: John
 Nickname: JD
 DOB (ddmmyyyy): 1998
 Pet: Shadow
 Symbols: @,#
 Numbers: 123,786
...
✅ Done. Wrote 12,540 lines to smart.txt (~1.2 MB)
```
---

## ⚠️ Disclaimer
This tool is created for educational and ethical hacking purposes only.
The author (VivekXploit) is not responsible for any misuse.
Use it only in legal environments such as your own systems, labs, or with explicit permission.
---

**⭐ If this project was helpful, please consider to leaving a **star** to support it!**
