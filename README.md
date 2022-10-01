<h1 align="center">hermes</h1>
<p align="center">Telegram Bot for system control and live code notifications.</p>

**Current development status: BETA** - All the main functions are implemented. Need to make debug before release.

Ver 0.7, 01 October 2022



## What can Hermes do?

eheh... make pictures! TODO




## How to install (wizard)

I will assume that you **already have a Telegram bot and its authorization token**. It is better to know also your **chatid**, as it will be requested by the wizard. Anyway, it is possible to add new users later, with a registration procedure or manually.

If you wish to perform a **full manual installation**, take a look at [this](./manual-install.md) readme file.


1) Clone this repo in `/opt/hermes` (my suggested installation path).
```bash
cd /opt/
sudo git clone https://github.com/baronefr/hermes.git --depth=1
cd hermes
chmod +x bin/*
```


2) Install the Hermes Python library.
```bash
pip3 install -e /opt/hermes/src/
```


3) Create your configuration files (path, telegram bot token). The following script will guide you through the necessary steps:
```bash
bin/make-config.sh
```
The requested inputs are
- `Hermes hostname` \[string\] - basically, the name of your host machine
- `Telegram bot token` - something that looks like `0123456789:abcdefghijklmnopqrstuvwxy_ABCDEFGHI`
- `chatid` \[number\] (optional) - if you don't know it, there are other bots that will echo your chat id (like `@chatid_echo_bot`)
    - userid \[string\] - a string associated to your chatid, for friendly reference (if a chatid is prompted)

By default, the configuration files are placed in `/home/YOUR_USERNAME/.local/hermes/`. *Remark*: the script will also append a new line to your .bashrc file. Don't worry, it also creates a backup copy of it... :)

If the process is successful, check that the environment variable exists:
```bash
source bin/reload-env.sh
echo "$HERMES_ENV_SETTINGS"
```
Anyway, also opening a new bash shell will make the trick (recall to cd again into `/opt/hermes`).


4) Execute the bot to make sure that everything is configured properly.
```
bin/start-bot.py --dry-run
```
In case of errors in the bot initialization, use the error messages to spot the error among the previous steps.





### How to install (full manual)

Read [this](./manual-install.md).



## Make the bot execute at startup

We need to setup a systemd service to make the bot execute at boot before the user login. The following wizard will guide you

```
bin/make-service.sh
```







## Add a new user with wizard

extra) Add yourself as authorized user.
```
bin/register.sh
```







