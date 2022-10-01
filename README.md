<h1 align="center">hermes</h1>
<p align="center">Telegram Bot for system control and live code notifications.</p>

**Current development status: BETA** - All the main functions are implemented. Need to make debug before release.

Ver 0.7, 01 October 2022



## What can Hermes do?

eheh... make pictures! TODO


## Setup (wizard)

1) Clone this repo in `/opt/hermes` (my suggested installation path).
```bash
sudo git clone https://github.com/baronefr/hermes.git /opt/hermes
chmod +x /opt/hermes/bin/*
```

2) Install the Hermes Python library.
```bash
pip3 install -e /opt/hermes/src/
```


3) Create your **Hermes private directory**. Hermes requires a directory to store logs and user private settings (Telegram token, chatid). I suggest to use `~/.local/hermes/`.
```bash
mkdir -p /home/$USER/.local/hermes/ && cd "$_"
```


4) Create a `setup.hermes` file
```bash
touch setup.hermes
```
and edit it, providing the following values:
- `hostname` \[string\] - basically, the name of your host machine
- `token` \[string\] - the Telegram bot token
- `chatid` \[number\] - ID associated to your Telegram account. If you don't know it yet, there are other bots that will echo your chat id (like @chatid\_echo\_bot).
- `userid` \[string\] - a string associated to your chatid, for friendly reference

As an example, the file should look like this:
```python
hostname=mars
token=0123456789:abcdefghijklmnopqrstuvwxy_ABCDEFGHI
chatid=1234567890
userid=baronefr
```


5) Let the bot create the definitive configuration files
```bash
python3 -c "import hermes; hermes.setup();"
```


6) Append to your bashrc the environment variable (if you are NOT root user)
```bash
cd
cp .bashrc .bashrc.bak
echo -e "# hermes env\nexport HERMES_ENV_SETTINGS=\"/home/$USER/.local/hermes/settings.ini\"" >> .bashrc
source .bashrc
```

7) Test the bot with a dry run (if you are NOT root user)
```bash
/opt/hermes/bin/start-bot.py --dry-run
```




## Execute the bot

By default, the bot is not running in background. You can execute it through this script, leaving the terminal active as long as you wish.
```bash
/opt/hermes/bin/start-bot.py
```
However, I find far more useful to setup the bot as a service which executes at boot!


### Make the bot autorun at boot

We need to setup a systemd service to make the bot execute at boot before the user login. The following wizard will guide you

```bash
/opt/hermes/bin/make-service.sh
```




## Add a new user with wizard

```bash
bin/register.sh
```







