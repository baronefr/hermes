<h1 align="center">hermes</h1>
<p align="center">Telegram Bot for system control and runtime notifications.</p>

![version](https://img.shields.io/badge/version-v%202.0-blue)


<br>


## What can Hermes do?

Hermes is a Python library that controls a private Telegram bot from which you can monitor your system, run custom commands and track Python script execution. To aid integration with non-Python environments, this library includes a command line interface.

* **CLI**
    - send a message from command line
    - send a message after the execution of a specific command, even in background
    - send images and files

* **Bot**
    - poweroff / reboot your system
    - power statistics
    - network status
    - implement your own **custom functions**

* **Tasks**
    - init a task in your Python script and get notifications
    - failsafe: an error in Hermes does not stop your code
    - send images and Matplotlib plots
    - query an internal log for each task

<br><br>

### Requirements

* Linux system
* Python 3.5 or above
    - the following packages are required: `pyTelegramBotAPI termcolor`


<br><br>

## Setup

In this section, I will walk you through the installation of Hermes on a Linux system.

*Note*: **Optional steps** are marked with ⏸ and **more advanced suggestions** are marked with 🔆.

ℹ️ **about your sensitive data** | The bot will use *sensitive data*: your private bot token and chatid. The private configuration files will be stored by default in your home directory, under `~/.hermes/`. This folder will contain the private key of the bot, user settings and log files.



**1)** Clone this repo and install the Hermes Python library.
```bash
git clone https://github.com/baronefr/hermes.git
pip3 install ./hermes
```



**2)** Using your preferred text editor, create a `setup.hermes` file that will be used by the Hermes installer. 

As an example, the file should look like this:
```python
hostname=mercury
token=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
chatid=1234567890
userid=baronefr
```
where
* `hostname` (string) - the name you would like to assign to your computer
* `token` (string) - the [Telegram bot](https://core.telegram.org/bots/api#authorizing-your-bot) token
* `chatid` (number) - ID associated to your Telegram account. If you don't know it yet, there are other bots that will echo your chat id (like @chatid\_echo\_bot).
* `userid` (string) - a string associated to your chatid, for friendly reference

⏸ (optional) There is a shortcut to create a template setup file from scratch, if you wish. Just execute the command `hermes-setup -m`. The template file will be created in your current directory.



**3)** Use the wizard to complete the setup.
```bash
hermes-setup
```

I recommend to **close and re-open your terminal** to make sure that Hermes has been linked properly.

⏸ (optional) If the setup is successful, I suggest to remove the `setup.hermes` file, as it contains sensitive informations about your bot.

🔆 (optional) The script should have created an enviroment variable `HERMES_ENV_SETTINGS`, which links to your private configuration files. Check that the variable exists with:
```bash
echo $HERMES_ENV_SETTINGS
```



**4)** Test the bot with a dry run.
```bash
hermes --dry-run
```

*Note*: You have to your start your Telegram bot first, if you want to receive the messages!


<br>


## Execute the bot on current shell

You can execute the bot in your current shell using the command
```bash
hermes --server
```
However, if the terminal is killed, it will also kill the bot service. 

**If you plan to keep the bot executed in background**, I find much more useful to **setup a systemd service**, so that the bot is executed automatically at boot. Take a look at the next section!



### Setup systemd service

**Note**: Please be sure that at this stage the bot is working properly.

A [systemd](https://wiki.archlinux.org/title/systemd) service can be configured to execute automatically the bot, keeping it running in background. The following will create a service file based on your configuration.
```bash
hermes-setup --systemd
```

If the wizard is successful, enable the service with these commands:
```bash
sudo cp hermes.service /etc/systemd/system
sudo systemctl enable hermes.service
sudo systemctl start hermes.service
```
*Note*: Administrator permissions will be asked for such operations.

- 🔆 **In case of issues in the systemd setup**, you can configure it from scratch. I placed in `lib/hermes.service` a template for a systemd service. You should already know how to deal with this files, otherwise it is a good chance to learn. :)
- 🔆 **In case of issues in the execution of Hermes as a service**, you would like to check the stdout of the service with `sudo journalctl -u hermes`. In most cases, the problems are file permissions or missing environment variables.


### 🔆 Authorize bot to poweroff/reboot system

Hermes includes functions to poweroff and reboot your computer. But to do so, your user should have permissions to execute `/bin/systemctl` without password. In most of the cases, this should make the trick:
```bash
echo  'echo -e "#hermes priv\n%$USER ALL=NOPASSWD: /bin/systemctl" >> /etc/sudoers' | sudo -s
```

Otherwise, just find the proper way for your OS to edit the **sudoers** file and allow the execution of `/bin/systemctl`.


<br><br>

## Usage

TODO


---
<p align="center">
<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
</p>