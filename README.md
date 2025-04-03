# project-lite
Discord CLI Client made in python.

> [!IMPORTANT]  
> This project is in **alpha**. Expect some things not working.

> [!NOTE]
> The client doesn't send share your token with anyone.

## is it against tos of discord?
> this client uses the Discord API to perform actions. discord does not allow this. use the client at your own risk

# How do i use the client?
project-lite may be a bit complicated to use, so here's a simple explanation on how to log in and read/send messages.
## 1. Download and start project-lite
Make sure you have [Python](https://python.org) and [Git](https://git-scm.com) downloaded. This guide should work on most platforms.

1. Open a terminal (e.g. for Windows: press Win+R and type `cmd`)
2. Copy and paste the following commands in a terminal: 
```sh
mkdir project-lite
git clone https://github.com/tjf1dev/project-lite project-lite
pip install -r requirements.txt
```
> [!WARNING]
> On Windows, you also need to run the `pip install windows-curses` command.
3. Run the `start.bat` file (on windows) or `start.sh` (on linux)

## 2. Log into the client
Once you open the client you will be asked for your **discord token**. You can find a guide on how to get it below. 

## 3. Select a channel
When you finish logging in, you will be on the default screen of project-lite. it should look similar to this.

![default screen of project-lite](https://github.com/user-attachments/assets/12cc28e2-afb8-4cdb-8324-1d1de4b03904)

To select a channel you want to write in, the easiest method is the browse command. Type `browse` in the text box and hit enter.

![default screen of project-lite with browse entered as a command](https://github.com/user-attachments/assets/607f8478-0931-4dae-8245-f2ede887ab3c)

Next, use your arrow keys/mouse to hover over your server and press space/click. A star will appear next to the server name, indicating its selected.
Press Tab to switch to the bottom bar. Navigate to the `OK` button and press it. (You can also just click the button with your mouse)
Then repeat the process again but with the channel.
When you're in a channel, the screen should look similar to this:

![screen with a selected channel](https://github.com/user-attachments/assets/0d054f38-6fd6-4b16-bc29-088ec93b0e36)

The `[CMD]` next to the name is indicating you are in **command mode**. You can type /help and hit enter to see a list of available commands.
To send messages to the channel, you can enter **rs** *(read-send)* **mode**. Type `rs` in the text box and hit enter.
The `[CMD]` should now change to `[RS]`. **Every message you type now will be sent in the channel**
Your screen should look like this now:

![rs mode example](https://github.com/user-attachments/assets/208e82ad-ea5a-45e5-8650-00b1b2c6d496)

To exit `[RS]` mode, type `/exit`. You can also use `/help` to view other commands.


# Frequently asked questions
### How do i get my token?

> There are a few ways to get your token, but i don't recommend pasting code into your console.
> Here is the one i use:
> 1. Log in into your Discord Web App
> 2. Open the DevTools Tab using `F12` or `Ctrl + Shift + I`
> 3. Go to the Network tab and press `F5` (this will disconnect you from vc's)
> 4. Find a record saying `@me`
> 5. In the headers view search for Authorization and copy it.
> 6. That's your token! Paste it into the input token field to log in. Make sure to save it well so others cant access it!

> [!CAUTION]
> NEVER share your token with anyone. This can make someone log in without a password or 2FA.

## Progress (current version)
- Messaging
  - [x] Sending text
  - [x] Recieving text
  - [ ] Format mentions
  - [ ] Sending attachments
  - [ ] Recieving attachments
  - [ ] App commands
  - [ ] ~~Emojis~~
  - [ ] ~~Stickers~~
  - [ ] ~~Gifs~~
  - [ ] Polls
- Information
  - [x] List guilds
  - [x] List channels
  - [x] Select guilds
  - [x] Select channels
  - [x] Get username
  - [x] Get profile picture
- Voice
  - project-lite will not have voice features.
- Other
  - [ ] Log in as bot
