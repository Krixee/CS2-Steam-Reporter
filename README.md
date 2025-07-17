# CS2-Steam Account Reporter

A Python-based tool for reporting Steam profiles via the Steam web interface, designed with a user-friendly GUI. This project is intended for educational purposes only to demonstrate web automation with Selenium and GUI development with ttkbootstrap. Please use responsibly and adhere to Valve's Steam Subscriber Agreement and Community Guidelines.

## Features

**Graphical User Interface:** Modern, dark-themed interface using ttkbootstrap for ease of use.

**Steam Profile Reporting:** Automates reporting of Steam profiles for suspected cheating in Counter-Strike 2 (CS2).
 
**Steam Guard Automation:** Retrieves Steam Guard codes from a specified email account (e.g., Gmail) using IMAP.

 **Proxy Support:** Utilizes Webshare proxies for IP rotation to reduce detection risk. 

**Cooldown Mechanism:** Enforces a 20-second delay between operations and a 30-second cooldown after each operation, with a countdown display.

## Requests
```bash
pip install requests selenium ttkbootstrap
```

## Usage
Add your Steam accounts and a shared email account for Steam Guard codes.
```
Example: [ 
{ "username": "your_steam_username1", "password": "your_steam_password1", "email": "your_email@gmail.com", "email_password": "your_email_app_password" }, 
{ "username": "your_steam_username2", "password": "your_steam_password2", "email": "your_email@gmail.com", "email_password": "your_email_app_password" } ]
```
Add your *Webshare* proxy list in HTTP format.
```
[ 
"http://username:password@ip:port", 
"http://username:password@ip:port" 
]
```

## Legal and Ethical Considerations

**Valve's Policies**: Automated reporting may violate Valve's Steam Subscriber Agreement (Section 3.C). Use this tool responsibly and only for educational purposes.

**Ethical Use:** Only report profiles with verified evidence of cheating. Misreporting can harm innocent users' Trust Factor.

**Risks:** Excessive reporting may lead to account restrictions. The script includes detection prevention (proxy rotation, delays), but risks remain.

**Alternatives:** Use in-game reporting or platforms like FaceIT for safer reporting.

## Limitations
**Effectiveness:** Steam profile reports may have limited impact on CS2 Overwatch compared to in-game reports. 

**Steam Guard:** Email server delays may affect code retrieval. 

**Proxies:** Proxy quality affects performance; invalid proxies are filtered automatically.



## License

[MIT]([https://choosealicense.com/licenses/mit/](https://github.com/Krixee/CS2-Steam-Reporter/blob/main/LICENSE))
