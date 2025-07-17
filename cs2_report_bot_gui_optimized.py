import json
import random
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests import get
import imaplib
import email
from email.header import decode_header
import os

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

report_reasons = [
    "Suspected aimbot in CS2 match",
    "Suspected wallhack in CS2 match",
    "Detected cheating in CS2 match",
    "Unfair advantage in CS2 match"
]

if not os.path.exists("proxies.json"):
    with open("proxies.json", "w") as f:
        json.dump([], f)

if not os.path.exists("accounts.json"):
    with open("accounts.json", "w") as f:
        json.dump([], f)

with open("proxies.json", "r") as f:
    proxies_list = json.load(f)

with open("accounts.json", "r") as f:
    steam_accounts = json.load(f)

report_count = len(steam_accounts) * 2
max_workers = 3
valid_proxies = []
last_report_time = 0

def check_proxy(proxy):
    try:
        response = get("https://api.ipify.org", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def get_steam_guard_code(email_address, email_password):
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(email_address, email_password)
        imap.select("INBOX")
        _, data = imap.search(None, '(FROM "no-reply@steampowered.com" UNSEEN)')
        if not data[0]:
            imap.logout()
            return None
        email_id = data[0].split()[-1]
        _, data = imap.fetch(email_id, "(RFC822)")
        email_message = email.message_from_bytes(data[0][1])
        subject = decode_header(email_message["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        if "Steam Guard" in subject:
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    code = "".join(filter(str.isdigit, body.split("Steam Guard code:")[1][:10]))
                    imap.store(email_id, "+FLAGS", "\\Seen")
                    imap.logout()
                    return code
        imap.logout()
        return None
    except:
        return None

def update_countdown(submit_button, countdown_label, remaining_time):
    if remaining_time > 0:
        countdown_label.configure(text=f"Cooldown: {remaining_time} seconds")
        root.after(1000, update_countdown, submit_button, countdown_label, remaining_time - 1)
    else:
        countdown_label.configure(text="")
        submit_button.configure(state=NORMAL)

def send_report(account, proxy, profile_url, index, log_text):
    try:
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        chrome_options.add_argument(f"--proxy-server={proxy}")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random.choice(user_agents)})
        driver.get("https://steamcommunity.com/login/home/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "steamAccountName")))
        driver.find_element(By.ID, "steamAccountName").send_keys(account["username"])
        driver.find_element(By.ID, "steamPassword").send_keys(account["password"])
        driver.find_element(By.ID, "imageLogin").click()
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "authcode")))
            code = get_steam_guard_code(account["email"], account["email_password"])
            if code:
                driver.find_element(By.ID, "authcode").send_keys(code)
                driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
            else:
                log_text.insert(tk.END, f"Steam Guard code not found: {account['username']} | Request: {index}\n")
                driver.quit()
                return
        except:
            pass
        driver.get(profile_url)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn_profile_action")))
        driver.find_element(By.CLASS_NAME, "btn_profile_action").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Report')]")))
        driver.find_element(By.XPATH, "//a[contains(text(), 'Report')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "report_type")))
        driver.find_element(By.ID, "report_type").send_keys("Cheating")
        driver.find_element(By.ID, "report_desc").send_keys(random.choice(report_reasons))
        driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
        log_text.insert(tk.END, f"Successful report: {profile_url} | Proxy: {proxy} | Account: {account['username']} | Request: {index}\n")
        driver.quit()
    except Exception as e:
        log_text.insert(tk.END, f"Error occurred: {e} | Proxy: {proxy} | Account: {account['username']} | Request: {index}\n")
        if 'driver' in locals():
            driver.quit()
    log_text.see(tk.END)

def start_reporting(profile_entry, log_text, submit_button, countdown_label):
    global last_report_time
    current_time = time.time()
    if current_time - last_report_time < 20:
        log_text.insert(tk.END, f"Please wait {20 - (current_time - last_report_time):.1f} seconds before starting a new operation!\n")
        log_text.see(tk.END)
        return
    profile_url = profile_entry.get()
    if not profile_url or not profile_url.startswith("https://steamcommunity.com/profiles/"):
        log_text.insert(tk.END, "Invalid Steam profile URL!\n")
        log_text.see(tk.END)
        return
    global valid_proxies
    valid_proxies = [proxy for proxy in proxies_list if check_proxy(proxy)]
    if not valid_proxies or not steam_accounts:
        log_text.insert(tk.END, "No valid proxies or Steam accounts!\n")
        log_text.see(tk.END)
        return
    submit_button.configure(state=DISABLED)
    log_text.delete("1.0", tk.END)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(report_count):
            account = random.choice(steam_accounts)
            proxy = valid_proxies[i % len(valid_proxies)]
            executor.submit(send_report, account, proxy, profile_url, i+1, log_text)
            time.sleep(random.uniform(3, 10))
    log_text.insert(tk.END, "Operation completed!\n")
    log_text.see(tk.END)
    last_report_time = time.time()
    update_countdown(submit_button, countdown_label, 30)

def create_gui():
    global root
    root = ttk.Window(themename="darkly")
    root.title("CS2 Report Bot")
    root.geometry("600x400")
    ttk.Label(root, text="Steam Profile URL:", bootstyle=PRIMARY).pack(pady=10)
    profile_entry = ttk.Entry(root, width=50, bootstyle=INFO)
    profile_entry.pack(pady=5)
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    submit_button = ttk.Button(button_frame, text="Submit", command=lambda: start_reporting(profile_entry, log_text, submit_button, countdown_label), bootstyle=SUCCESS)
    submit_button.pack(side=LEFT, padx=5)
    countdown_label = ttk.Label(button_frame, text="", bootstyle=WARNING)
    countdown_label.pack(side=LEFT, padx=5)
    log_text = ttk.Text(root, height=10, width=60)
    log_text.pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    create_gui()