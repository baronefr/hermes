<h1 align="center">hermes</h1>
<p align="center">Telegram Bot for system control and live code notifications.</p>

## Manual installation procedure

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



**In case you wish to proceed manually (for this step)** you can create yourself the configuration directory, which consist of two files:
- `auth.txt`: txt file (csv-like) for authorized user chat id and preferences
- `settings.ini`: txt file with the Telegram bot name and token
Templates for those files are available in `templates/`.

Eventually, you need to append to your .bashrc the following line
```
export HERMES_ENV_SETTINGS=CUSTOM_CONFIG_PATH/hermes/settings.ini
```
which will link Hermes to your custom directory. Source again your .bashrc file.

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

