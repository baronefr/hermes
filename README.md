<h1 align="center">hermes</h1>
<p align="center">Telegram Bot for system control and runtime notifications.</p>

**Current development status: first release** Please open an Issue if something does not work. :)

Ver 1.0, 31 October 2022


<br>

## What can Hermes do?

- **Bot**
    - poweroff / reboot your system
    - power status
    - network status
    - implement your own **custom functions**
    
- **Tasks**
    - init a task in your Python script and get notifications
    - failsafe: an error in Hermes does not stop your code
    - send images
    - send Matplotlib plots
    - use the Bot to check an internal log of your task

<br><br>

## Setup

In this guide, I will walk you through the installation of Hermes in a Linux system. I suggest to use the following default directories:
- `/opt/hermes` for the Hermes Python library & bin files
- `~/.local/hermes/` for the private keys, settings and logs (*Hermes private directory*)

**1)** Clone this repo in `/opt/hermes` and free the folder from r/w restrictions. The folder in /opt/ will not contain any data of yours.
```bash
sudo git clone https://github.com/baronefr/hermes.git /opt/hermes
sudo chmod 777 /opt/hermes/ -R
```

**2)** Install the Hermes Python library.
```bash
pip3 install -e /opt/hermes/src/
```

**3)** Create your **Hermes private directory**, which will store store logs and user credentials (Telegram token, chatid table).
```bash
mkdir -p /home/$USER/.local/hermes/ && cd "$_"
```

**4)** In the private directory, you shall create a `setup.hermes` file
```bash
nano setup.hermes
```

As an example, the file should look like this:
```python
hostname=mercury
token=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
chatid=1234567890
userid=baronefr
```
where
- `hostname` (string) - the name you would like to assign to your computer
- `token` (string) - the [Telegram bot](https://core.telegram.org/bots/api#authorizing-your-bot) token
- `chatid` (number) - ID associated to your Telegram account. If you don't know it yet, there are other bots that will echo your chat id (like @chatid\_echo\_bot).
- `userid` (string) - a string associated to your chatid, for friendly reference


**5)** Use the bot automatic wizard to complete the setup.
```bash
python3 -c "import hermes; hermes.setup();"
```

**6)** If you are **not root user**, add to your `.bashrc` file the environment variable pointing to the private directory
```bash
cd
cp .bashrc .bashrc.bak
echo -e "# hermes env\nexport HERMES_ENV_SETTINGS=\"/home/$USER/.local/hermes/\"" >> .bashrc
source .bashrc
```

**7)** Test the bot with a dry run
```bash
/opt/hermes/bin/start-bot.py --dry-run
```

*Note*: Access to your Telegram bot first, if you want to receive messages!

<br>


## Execute the bot

You can launch the bot through this script.
```bash
/opt/hermes/bin/start-bot.py
```
In this way, killing the terminal will also kill the bot. I find much more useful to **setup the bot as a systemd service**, which starts at boot and stays in background.


### Setup systemd service

**Note**: Please be sure that at this stage the bot is working properly when launched through the bin script.

A [systemd](https://wiki.archlinux.org/title/systemd) service can be configured to execute automatically the bot, keeping it running in background. The following wizard will do it for you.
```bash
cd /opt/hermes
bin/make-service.sh
```

- **In case of issues in the systemd setup**, you can configure it from scratch. I placed in `lib/hermes.service` a template for a systemd service. You should already know how to deal with this files, otherwise it is a good chance to learn. :)

- **In case of issues in the execution of Hermes as a service**, you would like to check the stdout of the service with `sudo journalctl -u hermes`. In most cases, the problems are file permissions.


### Authorize bot to poweroff/reboot system

Hermes includes functions to poweroff and reboot your computer. But to do so, your user should have permissions to execute `/bin/systemctl` without password. In most of the cases, this should make the trick:
```bash
echo  'echo -e "#hermes priv\n%$USER ALL=NOPASSWD: /bin/systemctl" >> /etc/sudoers' | sudo -s
```

Otherwise, just find the proper way for your OS to edit the **sudoers** file.



<br><br>

## Use the bot

Once the bot is running, send `/help` to get a list of the available commands and a short description of them.

To add custom commands, go to [this section](###-Add-custom-functions)


<br><br>

## Use the task manager

If the library is correctly installed and configured, you can use Hermes in any Python script.

```python
import hermes.task as htask
ht = htask(alias = 'whatever')

ht.notify('This is a demo of a task!')
```

For more examples, look at the Jupyter notebooks in `examples` repo directory.

<br><br>

## Customize your bot

### Add users

By default, the bot is created with only one authorized user. To add more, edit `~/.local/hermes/users.key` in csv format:
```bash
chatid,name,bonjour,active
1234567890,baronefr,true,true
9876543210,new_user,true,true
```

- `bonjour` - If true, the user will be notified with a message when the bot is started.
- `active` - If true, the user is authorized. If false, the user is discarded.

Please use an unique `name` value for each user.

<br>

### Add custom functions

Hermes allows to add custom functions. You might like to dive into the Hermes library itself, but I provide you an easier way.

In the *Hermes private directory* (default: `~/.local/hermes/`) there is a `external.py`. In such file, you can write your own functions.

#### Oneshot

Oneshot functions shall not take any argument and must return a string, which will be the Bot reply to the command sent by the user. Inside the function you can do whatever you want. For example, the following is a valid function.
```python
def lol() -> str:
    """a description"""  # <- docstrings are used to compose the help menu
    return "What are you laughing at?"
```

To enable this function, edit `settings.ini` and add the name of the function to the variable `oneshot`:
```python
...

[external]
oneshot=netstat,lol
query=None
```

In case of **multiple functions**, the names should be separated by a comma.

#### Query

`external.py` will use Python classes to handle [queries](https://core.telegram.org/bots/api#callbackquery). In `lib/example.py` there is an example of Query handler that you might adapt to your needs.

To enable a custom query handler, edit `settings.ini` and add the name of the class to the variable `oneshot`.

As an example, if you implement in `external.py` the class `rgb` ...

```python
class rgb:
    """ 💡 OpenRGB query"""
    
    # markup menu text
    msg = "💡 OpenRGB: pick a color"
    
    # markup menu buttons ('name of botton', 'name of associated action')
    menu = [
             ("🟡 yellow", 'YEL'),
             ("🔴 red",    'RED'),
             ("⚫ off",    'OFF')
           ]
    
    # action handler - execute your action, send back a txt
    def event(event = '') -> str:
    
        if event == 'YEL':
            msg = 'yellow'
            
        elif event == 'RED':
            msg = 'yellow'
            
        else:
            msg = 'poweroff'
            
        return(msg)
```

... then you can enable it in `settings.ini`:
```python
...

[external]
oneshot=netstat
query=rgb
```

