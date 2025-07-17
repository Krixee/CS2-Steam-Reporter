**CS2 Report Bot**
A Python-based tool for reporting Steam profiles via the Steam web interface, designed with a user-friendly GUI. This project is intended for educational purposes only to demonstrate web automation with Selenium and GUI development with ttkbootstrap. Please use responsibly and adhere to Valve's Steam Subscriber Agreement and Community Guidelines.

**Features**

**Graphical User Interface:** Modern, dark-themed interface using ttkbootstrap for ease of use.
**Steam Profile Reporting:** Automates reporting of Steam profiles for suspected cheating in Counter-Strike 2 (CS2).
**Steam Guard Automation:** Retrieves Steam Guard codes from a specified email account (e.g., Gmail) using IMAP.
**Proxy Support:** Utilizes Webshare proxies for IP rotation to reduce detection risk.
**Cooldown Mechanism:** Enforces a 20-second delay between operations and a 30-second cooldown after each operation, with a countdown display.
**Error Handling:* Robust handling for Steam Guard, session errors, and proxy failures.
**Dynamic Report Count:** Sends reports equal to twice the number of Steam accounts provided.

**Prerequisites**

Python 3.8+
Google Chrome and ChromeDriver (matching your Chrome version)
Dependencies:pip install requests selenium ttkbootstrap



**Setup**

Clone the Repository:
git clone https://github.com/<your-username>/cs2-report-bot.git
cd cs2-report-bot


**Configure accounts.json:**

Add your Steam accounts and a shared email account for Steam Guard codes.

Example:
[
    {
        "username": "your_steam_username1",
        "password": "your_steam_password1",
        "email": "your_email@gmail.com",
        "email_password": "your_email_app_password"
    },
    {
        "username": "your_steam_username2",
        "password": "your_steam_password2",
        "email": "your_email@gmail.com",
        "email_password": "your_email_app_password"
    }
]


For Gmail, generate an App Password if 2-Step Verification is enabled.


**Configure proxies.json:**

Add your Webshare proxy list in HTTP format.

Example:
[
    "http://username:password@ip:port",
    "http://username:password@ip:port"
]




**Install ChromeDriver:**

Download ChromeDriver from here.
Add it to your system PATH or place it in the project directory.



**Usage**

Run the script:
python cs2_report_bot_gui_optimized.py


--In the GUI:--
Enter a Steam profile URL (e.g., https://steamcommunity.com/profiles/7656119XXXXXXXXX).

Click Submit to start the reporting process.

The log area displays operation status (success, errors, etc.).

After completion, the Submit button is disabled for 30 seconds with a countdown timer.




**Notes**

**Steam Guard:** The script automatically retrieves Steam Guard codes from the email specified in accounts.json. Ensure the email account is accessible via IMAP.

**Proxy Rotation:** Proxies are validated before use to ensure reliability.

**Cooldown:** A 20-second delay prevents consecutive operations, and a 30-second cooldown follows each operation to mimic natural behavior.


**Legal and Ethical Considerations**

Valve's Policies: Automated reporting may violate Valve's Steam Subscriber Agreement (Section 3.C). Use this tool responsibly and only for educational purposes.

Ethical Use: Only report profiles with verified evidence of cheating. Misreporting can harm innocent users' Trust Factor.

Risks: Excessive reporting may lead to account restrictions. The script includes detection prevention (proxy rotation, delays), but risks remain.

Alternatives: Use in-game reporting or platforms like FaceIT for safer reporting.

**Limitations**

Effectiveness: Steam profile reports may have limited impact on CS2 Overwatch compared to in-game reports.
Steam Guard: Email server delays may affect code retrieval.
Proxies: Proxy quality affects performance; invalid proxies are filtered automatically.

**Contributing**

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure code adheres to ethical and legal guidelines.

**License**

This project is licensed under the MIT License. See the LICENSE file for details.

**Disclaimer**

This tool is for educational purposes only. The author is not responsible for any misuse or consequences arising from its use. Always respect Valve's terms and community guidelines.