Setup
#####

In this section, I will walk you through the installation of Hermes on a Linux system.

The way Hermes works is quite simple.

* Hermes looks for an **environment variable** (``HERMES_ENV_SETTINGS``) which points to a directory that contains all the necessary configuration files.
* By default, this directory is located in the user HOME folder, specifically in ``~/.local/hermes/``. This location is customizable. Furthermore, it can be overridden every time the bot is loaded.

The following steps will guide you through the installation of Hermes and the creation of the configuration directory.


Requirements
------------

Before starting with the procedure, you should have created a `Telegram bot <https://core.telegram.org/bots/api#authorizing-your-bot>`_. In Telegram, open the chat with your bot and send the `\start` command. To proceed, we need the following information:

* **Telegram Bot token**: it is a long string of letters and numbers that gives acces to your bot. It should look like ``123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11``. It is provided by the Telegram API at the creation of the bot. 
* **Your chatid**: it is a sequence of numbers that identifies your Telegram account. It should look like ``1234567890``. We will use this ID to secure the access to the bot functionalities only to authorized users. If you don't know it yet, there exist other Telegram bots that can echo your chat id (like ``@chatid_echo_bot``).


Procedure
---------

**1)** Clone this repo and install the Hermes Python library.

.. code-block:: bash

    git clone https://github.com/baronefr/hermes.git
    pip3 install .


**2)** Using your preferred text editor, create a `setup.hermes` file that will be used by the Hermes installer. 

As an example, the file should look like this:

.. code-block:: python

    hostname=mercury
    token=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    chatid=1234567890
    userid=baronefr

where

- `hostname` (string) - the name you would like to assign to your computer
- `token` (string) - the `Telegram bot <https://core.telegram.org/bots/api#authorizing-your-bot>`_ token
- `chatid` (number) - ID associated to your Telegram account. If you don't know it yet, there are other bots that will echo your chat id (like @chatid\_echo\_bot).
- `userid` (string) - a string to be associated to your chatid, for friendly reference

.. note::
    ⏸ (hint) The command ``hermes-setup -m`` can create in your current folder an empty setup file, like the one shown above, that can be edited.



**3)** Use the wizard to complete the setup.

.. code-block:: bash
    
    hermes-setup

I recommend to **close and re-open your terminal** to make sure that Hermes has been linked properly.

.. note::
    ⏸ (optional) If the setup is successful, I suggest to remove the `setup.hermes` file, as it contains sensitive informations about your bot.

.. note::
    🔆 At this point, the script should have created an enviroment variable ``HERMES_ENV_SETTINGS``, which links to your private configuration files. Check that the variable exists, after refreshing your terminal, with the command ``echo $HERMES_ENV_SETTINGS``.




**4)** Test the bot with a dry run.

.. code-block:: bash

    hermes --dry-run

*Note*: You have to send the `\start` command to your Telegram bot first, if you want to receive the messages!

|
|
|


.. _systemdsetup:

Setup systemd service
#####################

.. warning::
    Please be sure that at this stage the bot is working properly.

A `systemd <https://wiki.archlinux.org/title/systemd>`_ service can be configured to execute automatically the bot, keeping it running in background. The following will create a service file based on your configuration.

.. code-block:: bash
    
    hermes-setup --systemd


If the wizard is successful, enable the service with these commands:

.. code-block:: bash

    sudo cp hermes.service /etc/systemd/system
    sudo systemctl enable hermes.service
    sudo systemctl start hermes.service

*Note*: Administrator permissions will be asked for such operations.

.. warning::
    🔆 **In case of issues in the systemd setup**, you can configure it from scratch. I placed in ``etc/hermes.service`` a template for a systemd service. You should already know how to deal with this files, otherwise it is a good chance to learn. :)
.. warning::
    🔆 **In case of issues in the execution of Hermes as a service**, you would like to check the stdout of the service with ``sudo journalctl -u hermes``. In most cases, the problems are file permissions or missing environment variables.


Authorize bot to poweroff/reboot system
---------------------------------------

Hermes includes functions to poweroff and reboot your computer. But to do so, your user should have permissions to execute ``/bin/systemctl`` without password. In most of the cases, this should make the trick:

.. code-block:: bash

    echo  'echo -e "#hermes priv\n%$USER ALL=NOPASSWD: /bin/systemctl" >> /etc/sudoers' | sudo -s


Otherwise, just find the proper way for your OS to edit the **sudoers** file and allow the execution of ``/bin/systemctl``.

