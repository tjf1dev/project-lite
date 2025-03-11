from login import config
from functions import *
from logger import logger
def Login(after_fail:bool=False):
    global save,token,saving
    conf = config.Load()
    if after_fail:
        logger.debug("restarting after authentication failure")
    if conf==None or after_fail:
        
        print("Welcome to project-lite.\nTo start, you need to login to your Discord account.")
        token = input("Enter your token: ")
        val = validate_token(token)
        while val!=True:
            logger.debug("could not validate token")
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
        username = get_discord_username(get_discord_user_info(conf['token']))
        if not username:
            logger.warning("could not fetch username")
            print("Your token appears to be invalid. Please re-authenticate.")
            Login(after_fail=True)
        print(f"Welcome back, {username}")
        token=conf['token']
if __name__ == "__main__":
    raise RuntimeError("You should not run this script directly. Use the main script.")