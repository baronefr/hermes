# How to use and customize Hermes


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

