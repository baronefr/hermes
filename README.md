<h1 align="center">hermes</h1>
<p align="center">Telegram Bot for system control and live code notifications.</p>

**Current development status: BETA** - All the main functions are implemented. Need to make debug before release.

Ver 0.7, 01 October 2022



## What can Hermes do?

eheh... make pictures! TODO




## How to install

I will assume that you **already have a Telegram bot and its authorization token**.

1) Clone this repo in `/opt/hermes` (my suggested installation path).
```
cd /opt
git clone https://github.com/baronefr/hermes.git --depth=1
cd hermes
chmod +x ./bin/*
```

2) Install the Hermes Python library.
```
pip3 install -e /opt/hermes/
```

3) Create your configuration files (path, telegram bot token). The following script will guide you through the necessary steps.
```
bin/make-config.sh
```
By default, the configuration files are placed in `/home/YOUR_USERNAME/.local/hermes/`. *Remark*: the script will also append a new line to your .bashrc file. Don't worry, it also creates a backup copy of it... :)

<details>
  <summary>Manual procedure (click me)...</summary>
  
**In case you wish to proceed manually (for this step)** you can create yourself the configuration directory, which consist of two files:
- `auth.txt`: txt file (csv-like) for authorized user chat id and preferences
- `settings.ini`: txt file with the Telegram bot name and token
Templates for those files are available in `templates/`.

Eventually, you need to append to your .bashrc the following line
```
export HERMES_ENV_SETTINGS=CUSTOM_CONFIG_PATH/hermes/settings.ini
```
which will link Hermes to your custom directory.
</details>



4) Execute the bot to make sure that everything is configured properly.
```
./bin/start_bot.py --dry-run
```

5) Add yourself as authorized user.
```
bin/register.sh
```

<details>
  <summary>Manual procedure (click me)...</summary>
  
**In case you wish to proceed manually (for this step)** you have to edit the `auth.txt` in your configuration directory, adding a line matching the following fields:
```
chatid,name,bonjour,active
```
- **chatid** (number) - the number associated to your Telegram account. There are many ways to retrieve it, like [this one](https://web.telegram.org/#/im?p=@myidbot).
- **name** (string) - identify the user with a readable name
- **bonjour** (true/false) if true, the bot will send a bonjour message to the user when the bot is executed
- **bonjour** (true/false) if true, the user is enabled

Just for example, a valid `auth.txt` file would appear this way:
```
chatid,name,bonjour,active
1234554321,baronefr,true,true
```
</details>





### To make the bot execute at startup

We need to setup a systemd service to make the bot execute at boot before the user login.


```
systemctl start hermes
systemctl enable hermes
```
