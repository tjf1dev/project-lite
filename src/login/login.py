from login import config
from functions import *
def Login():
    global save,token,saving
    conf = config.Load()
    if conf==None:
        print("Welcome to project-lite.\nTo start, you need to login to your Discord account.")
        token = input("Enter your token: ")
        val = validate_token(token)
        while val!=True:
            print("Couldn't log in, please check your token.")
            token = input("Enter your token: ")
        save = input("Save login? [Y/n] >")
        if save.lower() not in ["n","no","false"]:
            config.Save({
                "token": token,
                "saving": 1,
                "favorites":[],
                "channelid":0
            })
            saving = 1
            print("Saved info (config.json)")
        else:
            config.Save({
                "token": ""
            })
            print("Warning: your token will not be stored, and you will need to login each time you start the client.")
            token = input("Enter your token: ")
            saving = 0
    elif conf['token']=="":
        print("Welcome to project-lite.\n")
    else:
        print("Welcome back,",get_discord_username(get_discord_user_info(conf['token'])))
        token=conf['token']
if __name__ == "__main__":
    raise RuntimeError("You should not run this script directly. Use the main script.")