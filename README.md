# project-lite
Discord CLI Client made in python.

> [!IMPORTANT]  
> This project is in **alpha**. Expect some things not working.

> [!NOTE]
> The client doesn't send your token to anyone.
## is it against tos of discord?
> this client uses the Discord API to perform actions. discord does not allow this. use the client at your own risk



## Progress (current version)
- Messaging
  - [x] Sending text
  - [x] Recieving text
  - [x] Format mentions
  - [ ] Sending attachments
  - [ ] Recieving attachments
  - [ ] App commands
  - ~~[ ] Emojis~~
  - ~~[ ] Stickers~~
  - ~~[ ] Gifs~~
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
Once you open the client
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
