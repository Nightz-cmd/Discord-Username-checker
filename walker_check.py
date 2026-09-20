import os
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import string
from pathlib import Path


string.ascii_letters # A-Z a-z
string.digits # 1-9

def main():
    """"Main entry point"""
    print(f"""
          _________________________________________________________________
                                          ! Walker
                               Advanced Discord Username checker
                                ⣼⣯⠄⣸⣠⣶⣶⣦⣾⠄⡅⡅⠄⠄⠄⠄⡉⠹⠄⡅⠄⠄⠄
                                ⠿⠿⠶⠿⢿⣿⣿⣿⣿⣦⣤⣄⢀⡅⢠⣾⣛⡉⠄⠄⠄⠸⢀
                                ⣴⣶⣶⡀⠄⠄⠙⢿⣿⣿⣿⣿⣿⣴⣿⣿⣿⢃⣤⣄⣀⣥⣿
                                ⣿⣿⣿⣧⣀⢀⣠⡌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⣿⣿
                                ⣤⣤⣤⣬⣙⣛⢿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡍⠄⠄⢀⣤⣄⠉
                                ⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⢇⣿⣿⡷⠶⠶⢿⣿⣿⠇
                                ⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣷⣶⣥⣴
                                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                                ⣻⣿⣿⣧⠙⠛⠛⡭⠅⠒⠦⠭⣭⡻⣿⣿⣿⣿⣿⣿⣿⣿⡿
                                ⣿⣿⣿⣿⡆⠄⠄⠄⠄⠄⠄⠄⠄⠹⠈⢋⣽⣿⣿⣿⣿⣵⣾
                                ⣿⣿⣿⣿⣿⠄⣴⣿⣶⣄⠄⣴⣶⠄⢀⣾⣿⣿⣿⣿⣿⣿⠃
                                ⠛⢿⣿⣿⣿⣦⠁⢿⣿⣿⡄⢿⣿⡇⣸⣿⣿⠿⠛⠁⠄⠄⠄
                                ⠄⠄⠉⠻⣿⣿⣿⣦⡙⠻⣷⣾⣿⠃⠿⠋⠁⠄⠄⠄⠄⠄⢀
                                ⣮⣥⠄⠄⠄⠛⢿⣿⣿⡆⣿⡿⠃⠄⠄⠄⠄⠄⠄⠄⣠⣴⣿.
          __________________________________________________________________
          """)

    
if __name__ == '__main__':
    main()

def ask_for_length_and_count():

    chars = string.ascii_letters + string.digits + '._'

    char_length = int(input('Length (2-20):'))
    count = int(input('Count (1-10,000,000):'))

    names = []

    for i in range(count):
        name = ''.join(random.choice(chars) for _ in range(char_length))
        print(name)
        names.append(name)
    return names

names_that_get_printed_in_txt = ask_for_length_and_count()
names_checked_file = Path(__file__).parent / 'data' / 'names_to_check.txt'
with open(names_checked_file, 'w') as f:
    for x in names_that_get_printed_in_txt:
        f.write(x)
        f.write('\n')


url = 'https://discord.com/api/v9/unique-username/username-attempt-unauthed'

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'Origin': 'https://discord.com',
    'Referer': 'https://discord.com/register',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Discord-Locale': 'en-US',
}

# Try to import SOCKS support
try:
    import socks
    import socket
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False
    print("[!] For better results, install: ")

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.lock = threading.Lock()
        
    def fetch_proxies(self):
        """Fetch proxies from multiple sources"""
        all_proxies = set()
        
        # Sources that return fresh proxies
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=5000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        ]
        
        print("\n[*] Fetching fresh proxies...")
        
        for source in sources:
            try:
                print(f"  From {source.split('/')[2]}...", end=" ")
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    count = 0
                    for line in response.text.splitlines():
                        proxy = line.strip()
                        if proxy and ':' in proxy and not proxy.startswith('#'):
                            if '@' in proxy:
                                proxy = proxy.split('@')[-1]
                            # Only keep proxies with standard ports
                            port = proxy.split(':')[-1]
                            if port in ['8080', '3128', '1080', '80', '443', '8085', '8888']:
                                all_proxies.add(proxy)
                                count += 1
                    print(f"✓ {count} proxies")
                else:
                    print("✗ Failed")
                time.sleep(0.5)
            except:
                print("✗ Error")
                continue
        
        self.proxies = list(all_proxies)
        print(f"\n[✓] Total: {len(self.proxies)} proxies")
        return self.proxies
    
    def test_discord_proxy(self, proxy):
        """Test if proxy works with Discord specifically"""
        try:
            # Test with a random username
            test_name = f"test_{random.randint(10000, 99999)}"
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            
            start = time.time()
            response = requests.post(url, json={'username': test_name}, 
                                   headers=headers, proxies=proxies, timeout=5)
            latency = time.time() - start
            
            # Any response (200, 400, 429) means proxy works
            if response.status_code in [200, 400, 429] and latency < 3:
                return proxy, latency
        except:
            pass
        return None, None
    
    def get_working_proxies(self, target=30):
        """Get proxies that work with Discord"""
        print(f"\n[*] Testing {min(len(self.proxies), 300)} proxies with Discord...")
        
        working = []
        
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(self.test_discord_proxy, proxy): proxy 
                      for proxy in self.proxies[:300]}
            
            for future in as_completed(futures):
                proxy, latency = future.result()
                if proxy:
                    working.append((proxy, latency))
                    if len(working) % 5 == 0:
                        print(f"  ✓ Found {len(working)} working Discord proxies...")
                    
                    if len(working) >= target:
                        break
        
        if not working:
            print("[!] No working proxies found!")
            return []
        
        working.sort(key=lambda x: x[1])
        self.proxies = [proxy for proxy, _ in working]
        
        print(f"\n[✓] Found {len(working)} proxies that work with Discord!")
        print(f"\n📊 Fastest working proxies:")
        for i, (proxy, latency) in enumerate(working[:10], 1):
            print(f"  {i}. {proxy:25} - {latency:.2f}s")
        
        return self.proxies
    
    def get_proxy(self):
        """Get next proxy"""
        with self.lock:
            if not self.proxies:
                return None
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}

def check_username(name, proxy_manager, retry=0):
    """Check username with proxy"""
    try:
        proxies = proxy_manager.get_proxy()
        if not proxies:
            return name, "NO_PROXY"
        
        response = requests.post(url, json={'username': name}, 
                                headers=headers, proxies=proxies, timeout=8)
        
        if response.status_code == 200:
            result = response.json()
            if not result.get('taken', True):
                return name, "AVAILABLE"
            else:
                return name, "TAKEN"
        elif response.status_code == 429 and retry < 2:
            time.sleep(1)
            return check_username(name, proxy_manager, retry + 1)
        else:
            return name, f"ERR_{response.status_code}"
            
    except Exception as e:
        if retry < 2:
            time.sleep(0.5)
            return check_username(name, proxy_manager, retry + 1)
        return name, "TIMEOUT"

def main_checker():
    """Main checking function"""
    input_file = os.path.join('data', 'names_to_check.txt')
    output_file = os.path.join('data', 'checked.txt')
    
    if not os.path.exists(input_file):
        print(f"\n❌ Error: '{input_file}' not found!")
        return False
    
    # Load usernames
    with open(input_file, 'r') as f:
        usernames = [line.strip() for line in f if line.strip()][:100]  # Start with 100
    
    print(f"\n📋 Loaded {len(usernames)} usernames")
    
    # Get proxies
    proxy_manager = ProxyManager()
    proxy_manager.fetch_proxies()
    
    if not proxy_manager.proxies:
        print("\n[!] No proxies found. Using direct connection (slower)...")
        return check_direct(usernames, output_file)
    
    working = proxy_manager.get_working_proxies(target=20)
    
    if len(working) < 5:
        print("\n[!] Not enough working proxies. Using direct connection...")
        return check_direct(usernames, output_file)
    
    print(f"\n{'='*60}")
    print(f"🚀 CHECKING {len(usernames)} USERNAMES")
    print(f"📡 Using {len(working)} verified proxies")
    print(f"{'='*60}\n")
    
    # Clear previous results
    if os.path.exists(output_file):
        os.remove(output_file)
    
    available = []
    completed = 0
    start_time = time.time()
    
    # Use single thread for reliability with free proxies
    for name in usernames:
        result_name, status = check_username(name, proxy_manager)
        completed += 1
        
        elapsed = time.time() - start_time
        speed = completed / (elapsed / 60) if elapsed > 0 else 0
        
        if status == "AVAILABLE":
            print(f"\033[92m✅ [{completed:3}/{len(usernames)}] {name:20} -> AVAILABLE! ({speed:.0f}/min)\033[0m")
            available.append(name)
            with open(output_file, 'a') as f:
                f.write(f"{name}\n")
        elif status == "TAKEN":
            if completed % 5 == 0:
                print(f"\033[90m❌ [{completed:3}/{len(usernames)}] {name:20} -> TAKEN\033[0m")
        else:
            print(f"\033[93m⚠️ [{completed:3}/{len(usernames)}] {name:20} -> {status}\033[0m")
        
        # Small delay to avoid overwhelming proxies
        time.sleep(0.3)
    
    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE!")
    print(f"✅ Available: {len(available)}")
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"⚡ Speed: {completed / (elapsed/60):.0f} names/minute")
    print(f"📁 Results: {output_file}")
    
    if available:
        print(f"\n🎉 Available usernames:")
        for name in available[:10]:
            print(f"   ✅ {name}")
    
    return True

def check_direct(usernames, output_file):
    """Fallback without proxies (slower but works)"""
    print(f"\n{'='*60}")
    print(f"🐢 SLOW MODE (No proxies - respects rate limits)")
    print(f"{'='*60}\n")
    
    available = []
    
    for i, name in enumerate(usernames, 1):
        try:
            response = requests.post(url, json={'username': name}, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if not result.get('taken', True):
                    print(f"✅ [{i:3}/{len(usernames)}] {name} -> AVAILABLE!")
                    available.append(name)
                    with open(output_file, 'a') as f:
                        f.write(f"{name}\n")
                else:
                    print(f"❌ [{i:3}/{len(usernames)}] {name} -> TAKEN")
            
            elif response.status_code == 429:
                wait = response.json().get('retry_after', 10)
                print(f"⚠️ Rate limited! Waiting {wait}s...")
                time.sleep(min(wait, 15))
                continue
            
            # Wait 5-7 seconds between requests
            time.sleep(random.uniform(5, 7))
            
        except Exception as e:
            print(f"⚠️ [{i:3}/{len(usernames)}] {name} -> ERROR")
            time.sleep(8)
    
    print(f"\n✅ Found {len(available)} available usernames!")
    return available

if __name__ == "__main__":
    print(""" 
          ═══════════════════════════════════════════════════════════════════
                                        ! Walker
                         Discord Username Checker  Verified Proxies 
          ═══════════════════════════════════════════════════════════════════
          """)
    
    if not os.path.exists('data'):
        os.makedirs('data')
        print("[📁] Created 'data' folder")
        print("[💡] Add 'names_to_check.txt' with usernames\n")
    else:
        main_checker()