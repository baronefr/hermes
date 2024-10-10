hermes.bot package
##################

.. automodule:: hermes.bot
   :members:
   :special-members: __init__
   :show-inheritance:

|
|

Internal modules
================

The following modules are used by the package.
I recommend working with this functions only if you are developing Hermes.
Ideally, the user should not need to access these modules.


hermes.bot.linguist module
--------------------------

This submodule provides the message templates that are used by the Hermes bot.
If you want to customize the messages (for example, to rewrite them in your language), edit the strings contained in the following classes.

.. automodule:: hermes.bot.linguist
   :members:
   :undoc-members:
   :show-inheritance:

hermes.bot.handlers module
--------------------------

This submodule provides the handler functions that are executed when the bot server receives a command.

.. automodule:: hermes.bot.handlers
   :members:
   :undoc-members:
   :show-inheritance:

hermes.bot.fpower module
------------------------

This submodule handles the power management functions of the bot server.

.. automodule:: hermes.bot.fpower
   :members:
   :undoc-members:
   :show-inheritance:

hermes.bot.logger module
------------------------

This submodule logs the user activities. By default, the logs are stored in a folder `logs/` in the Hermes configuration directory.

.. automodule:: hermes.bot.logger
   :members:
   :undoc-members:
   :show-inheritance:

