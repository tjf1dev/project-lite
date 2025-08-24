# hello! this is an example of a project-lite extension.
# to load this one, remove the dash (-) from the filename.

# 1. registering basic commands

# import the command decorator from the main parser
from parser import command  # located in src/parser.py

# hook into global logger
# you can use it as usual
# e.g. logger.info("hello!")
from logger import logger  # located in src/logger.py


# we register a regular command, without arguments.
@command(
    name="example_regular_command",
    description="normal command from an extension.",
    aliases=["erc"],
)  # you can use any arguments the Command model has
# the function name doesn't matter (it must be unique though)
# we don't need any function arguments
def regular_command_function():
    # this command just prints a log
    logger.info("hello from the example extension!")
    # generally there's no need to return in commands. you can still do it if you want.


# when loaded, the command will behave just like a built in one.
# if you run it:
# ~$ example_regular_command
# [ INFO ] hello from the example extension!
# ~$

# 2. using context
# context is a part of project-lite that stores basic information persistent across all commands
# (channel id, user info, etc.)

# to use it, we have to import the context file
import context  # located in src/context.py
# most of the fields in context get initiated in the main file, so no need to wait for it.


# we now register simple another command that prints the current selected channel id
@command(
    name="example_using_context", description="sends the current channel id!"
)  # do not use duplicate command names (and function names)
def channel_id():
    # this logs the numeric id of the channel
    logger.info(
        f"channel: {context.channel_id}"
        if context.channel_id
        else "no channel selected."
    )


# now, let's show information about the logged in user
@command(
    name="example_discord_bio", description="sends your discord bio"
)  # do not use duplicate command names (and function names)
def bio():
    # here, the information about the user is stored in context.user
    # object it returns: https://discord.com/developers/docs/resources/user#user-object
    user = context.user
    # use print instead of the logger because of coloring and prefixes
    print(user.get("bio", "user has no bio."))


# 3. using arguments
# for arguments we use the Argument and DataType models
import models  # models.Argument, models.DataType


# we then put the arguments in the command decorator
@command(
    name="example_echo",
    description="repeats your message",
    args=[
        models.Argument(
            datatype=models.DataType.WildString,  # DataType.WildString has to be the last unique argument. it allows strings with spaces without quotes.
            name="content",
            required=True,
        )
    ],
)
def echo(**kwargs):  # to get the argument we use keyword arguments
    content = kwargs["content"]
    # if the argument wasnt required, we would have had to handle a lack of it.
    logger.info(content)


# 4. custom api requests
# to send GET requests to the discord api, we will use on of the functions features
from functions import custom_get_request
# the functions script has a lot of useful tools, you should check it out!


@command(name="example_api", description="lists the amount of servers you're in")
def api():
    #! it is recommended, even required to cache all of api responses to context
    #! if context doesn't have the field built-in, you will have to use hasattr.
    if hasattr(context, "guild"):
        data = context.guild
        logger.debug("using cached data")
    else:
        # we will also use the token from context
        req = custom_get_request("users/@me/guilds", context.token)
        # this returns a requests.Response object
        data = req.json()
    context.guild = data
    logger.info(f"you are in: {len(data)} servers.")
