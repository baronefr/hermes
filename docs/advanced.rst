Advanced configuration
######################


.. _confdir:

About the Hermes configuration directory
========================================

The **Hermes configuration directory** (by default ``~/.local/hermes``) contains several files that are used to configure Hermes:

- **settings.cfg** - A file specifying the configuration of Hermes. 
- **users.key** - A CSV file defining the authorized users. Only the users with a chatid specified in this file will have access to the bot functionalities. All the commands from unauthorized users will be ignored.

The usage **logs** are collected in the ``logs/`` folder. The log policy of Hermes is strict:

- Each authorized user has a unique log file, containing the history of all the commands that have been requested to the bot. The name of the file is determined by the user chatid.
- The commands received from unauthorized users are logged in the ``unauth.log`` file, saving the command and the source chatid.

Finally, the Hermes configuration directory contains the declarations of **custom bot commands**. For instance, the file ``oneshot.py`` will contain some custom commands. See the :ref:`specific section<customcommands>` for more information.

|

.. _moreuser:

Setting up more users
=====================

By default, the bot is created with only one authorized user. To add more, edit the ``users.key`` file in your Hermes configuration directory:

.. code-block:: bash

    chatid,name,bonjour,active
    1234567890,baronefr,true,true
    9876543210,newton,true,true
    9070503010,fermi,true,true

For each user, you must specify the ``chatid`` and a ``name`` string, followed by two boolean values:

- ``bonjour`` - If true, the user will be notified with a message when the bot is started.
- ``active`` - If true, the user is authorized. If false, the user is discarded.

Please use an unique ``name`` value for each user.

.. note::
    It is possible to print a list of the available users via CLI: ``hermes --list-users``.

.. _moreusercli:

Selecting user(s) in CLI
------------------------

Once the configuration file defines more users, it is possible to choose one via the CLI interface:

* enter the name of a specific user
    .. code-block:: bash

        hermes -u fermi -m 'message to send to Fermi only'

* enter the name of more users separated by a comma
    .. code-block:: bash

        hermes -u fermi,newton -m 'message to send to Fermi and Newton'

* explicitly select all the users
    .. code-block:: bash

        hermes -u all -m 'message to send to all the users'


The **default behavior** is to send the message to all the users that are marked as *active* in the ``users.key`` file.

.. _moreusertasks:

Selecting user(s) in Tasks
--------------------------

It is possible to specify the users that will receive the messages at the creation of the Task object (:py:meth:`hermes.task.task`).

* enter the name of a specific user
    .. code-block:: python

        from hermes.task import task as htask
        ht = htask(alias = 'demo', user = 'fermi')

* enter the name of more users through a list
    .. code-block:: python

        from hermes.task import task as htask
        ht = htask(alias = 'demo', user = ['fermi', 'newton'])

* explicitly select all the users
    .. code-block:: python

        from hermes.task import task as htask
        ht = htask(alias = 'demo', user = 'default')

The **default behavior** is to send the message to all the users that are marked as *active* in the ``users.key`` file.


|

.. _customcommands:

Create custom bot commands
==========================

Hermes allows to **add custom commands to the Telegram Bot**. We differentiate two types of commands: **oneshot** and **queries**.

- **Oneshot** commands are functions that are executed when the Bot receives the command from the user. The function returns a string, which is sent back to the user.

- **Queries** commands are implemented as Python classes. The user prompting the command for a query will receive a menu with several buttons. If the user presses one button, the Bot will perform a function associated to that button and send the output (which is a string, like the oneshot commands) back to the user.


Oneshot custom commands
-----------------------

A oneshot command is defined via the following template:

.. code-block:: python

    def lol() -> str:
        """description for the help menu"""
        ...
        message : str = "What are you laughing at?"
        return message

- The **name** of the function fixes the command name (i.e., the function in the template would be called by sending to the Bot the command ``\lol``).
- The function must **return** a string, which is sent back as reply to the user that triggers the Telegram command.
- The **docstring** is used by the Hermes bot to compose the entry of this command in the ``/help`` menu.

The command function, as described above, **must be defined in a file** named ``oneshot.py`` **contained in the Hermes configuration directory**.



Query custom commands
-----------------------

A query custom command is defined by a Python class that contains some fixed elements. The following block of code is an example of functioning query, called ``rgb``:

.. code-block:: python

    class rgb:
        """ 💡 RGB query""" # <- docstrings are used to compose the help menu
        
        # markup menu text
        msg = "💡 RGB: pick a color" # <- message sent to the user requesting this query
        
        # markup menu buttons ('name of botton', 'name of associated action')
        menu = [
                ("🟡 yellow", 'YEL'),
                ("🔴 red",    'RED'),
                ("⚫ off",    'OFF')
            ]
        
        # action handler - execute your action, send back a txt
        def event(event = '') -> str:
        
            if event == 'YEL':\
                ...
                message = 'leds are turned yellow'
                
            elif event == 'RED':
                ...
                message = 'leds are turned red'
                
            elif event == 'OFF':
                ...
                message = 'leds are turned off'

            else:
                message = 'unhandled option'
                
            return(message)

The class must have a specific structure:

- The **docstring** of the class is used by the Hermes bot to compose the entry of this command in the ``/help`` menu.
- A **variable msg** containing the string that will be the header markup menu.
- A **variable menu**, which is a list of tuples. Each tuple consists of a couple of strings, the first one being the name of the entry of the query menu, the second one being the callback identifier. The callback identifier will be used to perform a task when the user presses a button on the query menu.
- A **function event**, whose argument is the string corresponding to a callback identifier. This function must return a string, which is sent back to the user.

The query class, as described above, **must be defined in its own Python (.py) file**, named after the name of the class itself, **contained in the Hermes configuration directory**.
For instance, the class *rgb* shown in the template above would be defined in a file *rgb.py*.



Insert the custom commands in the Hermes settings file
------------------------------------------------------

After the custom commands have been declared as described above, **the user must enable the command** in the ``settings.cfg`` file contained in the Hermes configuration directory.

For instance, suppose that you want to enable a command called ``netstat`` (defined in the file ``oneshot.py``) and a query called ``rgb`` (defined in the file ``rgb.py``). The corresponding lines of the ``settings.cfg`` file would be:

.. code-block:: bash

    ...
    [modules]
    oneshot=netstat
    query=rgb

To specify more oneshot/queries, separate the name of the commands with commas: ``oneshot=netstat,othercommand,thirdcommand``.
