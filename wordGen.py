#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import string
import os
import sys
import math
import time
from typing import List
from colorama import Fore, Style, init
from tqdm import tqdm

# Init colorama
init(autoreset=True)

# ============== Utils ==============

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(
        Fore.RED + Style.BRIGHT +
r"""__     ___           _    __  __      _       _ _    
 \ \   / (_)_   _____| | __\ \/ /_ __ | | ___ (_) |_  
  \ \ / /| \ \ / / _ \ |/ / \  /| '_ \| |/ _ \| | __|
   \ V / | |\ V /  __/   <  /  \| |_) | | (_) | | |_  
    \_/  |_| \_/ \___|_|\_\/_/\_\ .__/|_|\___/|_|\__|
                                |_|                  
             V i v e k X p l o i t - ULTIMATE
""" + Fore.CYAN + "        ULTIMATE WORDLIST GENERATOR V1.0\n"
    )

def ask_int(prompt: str, minv: int = None, maxv: int = None, default: int = None) -> int:
    while True:
        raw = input(Fore.YELLOW + prompt + (f" [{default}]" if default is not None else "") + ": " + Fore.WHITE).strip()
        if not raw and default is not None:
            return default
        if raw.isdigit():
            val = int(raw)
            if (minv is None or val >= minv) and (maxv is None or val <= maxv):
                return val
        print(Fore.RED + "Invalid input. Try again.")

def ask_yn(prompt: str, default: str = "y") -> bool:
    d = default.lower()
    while True:
        resp = input(Fore.YELLOW + f"{prompt} (y/n) [{d}]: " + Fore.WHITE).strip().lower()
        if not resp:
            resp = d
        if resp in ("y", "yes"): return True
        if resp in ("n", "no"): return False
        print(Fore.RED + "Please answer y/n.")

def estimate_space(lines: int, avg_len: int = 10) -> str:
    # rough: average length + newline
    bytes_total = lines * (avg_len + 1)
    units = ["B","KB","MB","GB","TB"]
    i = 0
    size = float(bytes_total)
    while size >= 1024 and i < len(units)-1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"

def uniq_write(iterable, fh, limit=0, pbar: tqdm = None):
    count = 0
    seen = set()
    for item in iterable:
        if item in seen:
            continue
        seen.add(item)
        fh.write(item + "\n")
        count += 1
        if pbar: pbar.update(1)
        if limit > 0 and count >= limit:
            break
    return count

# ============== Generators ==============

def smart_variations(keywords: List[str], symbols: List[str], numbers: List[str], min_len: int, max_len: int):
    """Generate realistic mutations from personal keywords."""
    base = set()
    kws = [k for k in keywords if k]
    # simple transforms
    for k in kws:
        variants = {
            k, k.lower(), k.upper(), k.capitalize(),
            k[::-1],                        # reversed
            k.replace("a","@").replace("s","$").replace("i","1").replace("o","0") # common leet
        }
        base.update(variants)

    # append / prepend numbers & symbols
    for b in list(base):
        for n in numbers:
            base.add(b + n)
            base.add(n + b)
        for s in symbols:
            base.add(b + s)
            base.add(s + b)
        for n in numbers:
            for s in symbols:
                base.add(b + s + n)
                base.add(n + s + b)
                base.add(b + n + s)

    # combine multiple keywords
    for i in range(2, min(3, len(kws)) + 1):  # up to triples to keep sane
        for combo in itertools.permutations(kws, i):
            joined = "".join(combo)
            base.add(joined)
            # combine with numbers/symbols once
            for n in numbers:
                base.add(joined + n)
                base.add(n + joined)
            for s in symbols:
                base.add(joined + s)
                base.add(s + joined)

    # filter by length
    for pw in base:
        if min_len <= len(pw) <= max_len:
            yield pw

def brute_force_chars(chars: str, min_len: int, max_len: int):
    for L in range(min_len, max_len + 1):
        for tup in itertools.product(chars, repeat=L):
            yield "".join(tup)

# ============== Modes ==============

def mode_smart():
    banner()
    print(Fore.MAGENTA + ">>> Smart Wordlist (personalized)")
    name       = input(Fore.WHITE + " Target Name: ").strip()
    nickname   = input(" Nickname: ").strip()
    dob        = input(" DOB (ddmmyyyy or yyyy): ").strip()
    pet        = input(" Pet Name: ").strip()
    partner    = input(" Partner Name: ").strip()
    fav        = input(" Favorite Word/Thing: ").strip()
    phone      = input(" Phone digits (e.g., last 4–6): ").strip()
    extra      = input(" Extra keywords (comma separated): ").strip()
    symbols_in = input(" Symbols to include (e.g. @,!,$,#): ").strip()
    nums_in    = input(" Important numbers/years (comma separated): ").strip()

    keywords = [name, nickname, dob, pet, partner, fav, phone]
    if extra:
        keywords.extend([x.strip() for x in extra.split(",") if x.strip()])

    symbols = [x.strip() for x in symbols_in.split(",") if x.strip()] if symbols_in else []
    numbers = [x.strip() for x in nums_in.split(",") if x.strip()] if nums_in else []
    if dob and dob.isdigit():
        numbers.append(dob)
        if len(dob) >= 2: numbers.append(dob[-2:])
        if len(dob) >= 4: numbers.append(dob[-4:])

    min_len = ask_int(" Minimum length", 1, 128, 6)
    max_len = ask_int(" Maximum length", min_len, 128, max(8, min_len))
    limit   = ask_int(" Max lines to generate (0=unlimited)", 0, 10**9, 0)
    out     = input(Fore.WHITE + " Output filename (e.g., smart.txt): ").strip() or "smart.txt"

    # Estimate (rough guess): we don't know exact count upfront; skip heavy estimate
    if not ask_yn(" Proceed to generate?"):
        print(Fore.RED + " Aborted.")
        return

    with open(out, "w", encoding="utf-8") as fh:
        # We don't know total, so no pbar
        written = uniq_write(
            smart_variations(keywords, symbols, numbers, min_len, max_len),
            fh, limit=limit
        )
    print(Fore.GREEN + f"\n✅ Done. Wrote {written} lines to {out} (~{estimate_space(written)})")
    input(Fore.CYAN + "\n[Enter] to return to menu...")

def mode_bruteforce():
    banner()
    print(Fore.MAGENTA + ">>> Brute-force Wordlist (charset-based)")
    chars = ""
    if ask_yn(" Include lowercase a-z?"): chars += string.ascii_lowercase
    if ask_yn(" Include uppercase A-Z?"): chars += string.ascii_uppercase
    if ask_yn(" Include digits 0-9?"):    chars += string.digits
    if ask_yn(" Include symbols?"):       chars += string.punctuation

    if not chars:
        print(Fore.RED + "No charset selected. Returning.")
        time.sleep(1.2)
        return

    min_len = ask_int(" Minimum length", 1, 64, 4)
    max_len = ask_int(" Maximum length", min_len, 64, 6)
    limit   = ask_int(" Max lines to generate (0=unlimited)", 0, 10**12, 0)
    out     = input(Fore.WHITE + " Output filename (e.g., brute.txt): ").strip() or "brute.txt"

    # Estimate combinations
    total_all = sum(len(chars) ** L for L in range(min_len, max_len + 1))
    total = min(total_all, limit) if limit > 0 else total_all
    print(Fore.YELLOW + f"\n~ Estimate: {total_all:,} combos; will write {total:,} lines.")
    print(Fore.YELLOW + f"~ Approx size: {estimate_space(total)}")
    if not ask_yn(" Proceed?"):
        print(Fore.RED + " Aborted.")
        return

    with open(out, "w", encoding="utf-8") as fh:
        written = 0
        with tqdm(total=total, unit="pwd", desc="Generating") as pbar:
            for L in range(min_len, max_len + 1):
                # number of combos for this length
                nL = len(chars) ** L
                for tup in itertools.product(chars, repeat=L):
                    fh.write("".join(tup) + "\n")
                    written += 1
                    pbar.update(1)
                    if limit > 0 and written >= limit:
                        break
                if limit > 0 and written >= limit:
                    break

    print(Fore.GREEN + f"\n✅ Done. Wrote {written:,} lines to {out} (~{estimate_space(written)})")
    input(Fore.CYAN + "\n[Enter] to return to menu...")

def mode_hybrid():
    banner()
    print(Fore.MAGENTA + ">>> Hybrid Mode (Smart + Controlled Brute)")
    # Smart inputs
    name       = input(Fore.WHITE + " Target Name: ").strip()
    nickname   = input(" Nickname: ").strip()
    dob        = input(" DOB (ddmmyyyy or yyyy): ").strip()
    pet        = input(" Pet Name: ").strip()
    partner    = input(" Partner Name: ").strip()
    fav        = input(" Favorite Word/Thing: ").strip()
    phone      = input(" Phone digits: ").strip()
    extra      = input(" Extra keywords (comma separated): ").strip()
    symbols_in = input(" Symbols to include (e.g. @,!,$,#): ").strip()
    nums_in    = input(" Important numbers/years (comma separated): ").strip()

    keywords = [name, nickname, dob, pet, partner, fav, phone]
    if extra:
        keywords.extend([x.strip() for x in extra.split(",") if x.strip()])

    symbols = [x.strip() for x in symbols_in.split(",") if x.strip()] if symbols_in else []
    numbers = [x.strip() for x in nums_in.split(",") if x.strip()] if nums_in else []
    if dob and dob.isdigit():
        numbers.append(dob)
        if len(dob) >= 2: numbers.append(dob[-2:])
        if len(dob) >= 4: numbers.append(dob[-4:])

    # Brute subset
    chars = ""
    if ask_yn(" Include lowercase a-z?"): chars += string.ascii_lowercase
    if ask_yn(" Include uppercase A-Z?"): chars += string.ascii_uppercase
    if ask_yn(" Include digits 0-9?"):    chars += string.digits
    if ask_yn(" Include symbols?"):       chars += string.punctuation

    min_len = ask_int(" Minimum length", 1, 64, 6)
    max_len = ask_int(" Maximum length", min_len, 64, 10)
    limit   = ask_int(" Max lines to generate (0=unlimited)", 0, 10**12, 0)
    out     = input(Fore.WHITE + " Output filename (e.g., hybrid.txt): ").strip() or "hybrid.txt"

    # Estimate brute part
    total_brute_all = sum(len(chars) ** L for L in range(min_len, max_len + 1)) if chars else 0

    print(Fore.YELLOW + "\n~ Estimating smart portion (unique count unknown, usually thousands).")
    print(Fore.YELLOW + f"~ Brute-force potential: {total_brute_all:,} combos.")
    if not ask_yn(" Proceed?"):
        print(Fore.RED + " Aborted.")
        return

    written = 0
    with open(out, "w", encoding="utf-8") as fh:
        # Smart first (no progress bar—unknown total)
        written += uniq_write(
            smart_variations(keywords, symbols, numbers, min_len, max_len),
            fh, limit=(0 if limit == 0 else max(0, limit - written))
        )

        # Then controlled brute with progress bar
        if chars and (limit == 0 or written < limit):
            remain = (limit - written) if limit > 0 else total_brute_all
            total = min(total_brute_all, remain) if limit > 0 else total_brute_all
            with tqdm(total=total, unit="pwd", desc="Brute") as pbar:
                produced = 0
                for L in range(min_len, max_len + 1):
                    for tup in itertools.product(chars, repeat=L):
                        fh.write("".join(tup) + "\n")
                        written += 1
                        produced += 1
                        pbar.update(1)
                        if limit > 0 and written >= limit:
                            break
                    if limit > 0 and written >= limit:
                        break

    print(Fore.GREEN + f"\n✅ Done. Wrote {written:,} lines to {out} (~{estimate_space(written)})")
    input(Fore.CYAN + "\n[Enter] to return to menu...")

def mode_random():
    banner()
    print(Fore.MAGENTA + ">>> Random Strong Passwords")
    length = ask_int(" Password length", 4, 128, 12)
    count  = ask_int(" How many", 1, 10**7, 50)
    out    = input(Fore.WHITE + " Output filename (e.g., random.txt): ").strip() or "random.txt"

    chars = string.ascii_letters + string.digits + string.punctuation
    print(Fore.YELLOW + f"\n~ Will generate {count} random passwords.")
    if not ask_yn(" Proceed?"):
        print(Fore.RED + " Aborted.")
        return

    with open(out, "w", encoding="utf-8") as fh, tqdm(total=count, unit="pwd", desc="Random") as pbar:
        for _ in range(count):
            # os.urandom not needed here; simple random is fine for wordlists
            pw = "".join(chars[os.urandom(1)[0] % len(chars)] for _ in range(length))
            fh.write(pw + "\n")
            pbar.update(1)

    print(Fore.GREEN + f"\n✅ Done. Wrote {count:,} lines to {out} (~{estimate_space(count)})")
    input(Fore.CYAN + "\n[Enter] to return to menu...")

# ============== Menu ==============

def menu():
    while True:
        banner()
        print(
            Fore.GREEN + Style.BRIGHT +
            "[1] " + Fore.WHITE + "Smart Wordlist (personal info → mutations)\n" +
            Fore.GREEN + "[2] " + Fore.WHITE + "Brute-force Wordlist (charset + length)\n" +
            Fore.GREEN + "[3] " + Fore.WHITE + "Hybrid (Smart + Controlled Brute)\n" +
            Fore.GREEN + "[4] " + Fore.WHITE + "Random Strong Passwords\n" +
            Fore.RED   + "[0] " + Fore.WHITE + "Exit\n"
        )
        choice = input(Fore.YELLOW + "Choose an option: " + Fore.WHITE).strip()
        if choice == "1":
            mode_smart()
        elif choice == "2":
            mode_bruteforce()
        elif choice == "3":
            mode_hybrid()
        elif choice == "4":
            mode_random()
        elif choice == "0":
            print(Fore.CYAN + "\nGoodbye, VivekXploit 👋")
            break
        else:
            print(Fore.RED + "Invalid choice.")
            time.sleep(1.2)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nInterrupted. Bye!")
        sys.exit(1)

