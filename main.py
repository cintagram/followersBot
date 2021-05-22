import requests
from bs4 import BeautifulSoup as bs
import re
import time
import random
from datetime import datetime
import json
import string
import threading
from os import listdir, chdir

# move to .accounts/ folder
chdir('.accounts/')


# generate random user-agent
def randUserAgent():
    x = str(random.randint(100, 999))
    y = str(random.randint(10, 99))
    brands = ['xiaomi', 'vivo', 'samsung', 'micromax', 'oppo']
    rand_userAgent = f"""Mozilla/5.0 (Linux; Android {str(random.randint(9, 11))}; {random.choice(brands)} {str(random.randint(1000, 9999))}) AppleWebKit/{x}.{y} (KHTML, like Gecko) Chrome/{str(random.randint(10, 99))}.0.{str(random.randint(1000, 9999))}.{str(random.randint(100, 999))} Mobile Safari/{x}.{y}"""
    return rand_userAgent

# generate random pasword
def generate_password(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# check insternet connection
def check_connection():
    print("Checking Internet Connection...", end="")
    try:
        requests.get("https://www.wikipedia.com/", timeout=1)
        requests.get("https://www.github.com/", timeout=1)
        print("OK")
        time.sleep(1)
        return True
    except:
        print("\rNo Internet Connection...Exiting")
        quit()

# time elapsed counter
run = True
def time_elapsed(string):
    timerCount = 0
    second_count = "00"
    minute_count = 0
    while True:
        global run
        if run:
            print(f"\r{string}{str(minute_count)} : {second_count}", end="")
            time.sleep(0.999)
            timerCount += 1
            if len(str(timerCount)) == 1:
                second_count = "0" + str(timerCount)
            elif timerCount//60 > 0:
                minute_count += 1
                timerCount = 0
                second_count = "0"+str(timerCount)
            else:
                second_count = str(timerCount)
        else:
            return False

# instagram links
login_url = 'https://www.instagram.com/accounts/login/'
login_post_url = 'https://www.instagram.com/accounts/login/ajax/'
pass_change_page_and_post_url = "https://www.instagram.com/accounts/password/change/"

# Site links
login_page = "https://begeni.vip/girisyap" # login page and post req. page

# logging in to instagram
def loginInsta(username, password):
    r = requests.Session()
    user_agent = randUserAgent()
    r.headers = {"user-agent": user_agent}
    r.headers.update({"Referer": login_url})
    response = r.get(login_url)
    csrf = re.findall(r"csrf_token\":\"(.*?)\"", response.text)[0]
    dateTime = int(datetime.now().timestamp())
    payload = {'username': username, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{password}',
              'queryParams': {},
              'optIntoOneTap': 'false'}
    headers = {"User-Agent": user_agent, "X-Requested-With": "XMLHttpRequest", "Referer": login_url, "x-csrftoken": csrf}
    insta_response = r.post(login_post_url, data=payload, headers=headers)
    loggedSession = r
    return loggedSession, insta_response, user_agent

def changeInstaPassword(instaSession, username, password, newPassword, sessionUseragent):
    instaSession.get(f"https://www.instagram.com/{username}/")
    dateTime = int(datetime.now().timestamp())
    payload = {'enc_old_password': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{password}',
               'enc_new_password1': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{newPassword}',
               'enc_new_password2': f'#PWD_INSTAGRAM_BROWSER:0:{dateTime}:{newPassword}'
               }
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": sessionUseragent,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": pass_change_page_and_post_url,
        "X-CSRFToken": instaSession.cookies['csrftoken'],
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "TE": "Trailers",
        "Connection": "keep-alive",
        "Cookie": instaSession.request.headers['cookie']
    }
    pass_response = instaSession.post(pass_change_page_and_post_url, headers=headers, data=payload)
    return pass_response

def loginSite(username, password, userid):
    s = requests.Session()
    site = s.get(login_page)
    bs_content = str(bs(site.content, "html.parser"))
    token = re.search('antiForgeryToken=(.*)', bs_content)
    token = str(token.group(1).removesuffix('";'))
    payload = {'username': username, 'password': password, 'userid': userid,
               'antiForgeryToken': token}
    site_response = s.post(login_page, data=payload)
    siteLoggedSession = s
    return siteLoggedSession, site_response


# getting usernames and userid
while True:
    k = input("\nsend followers to avi? ")
    if k == "":
        targetUsername = "aviiiii_07"
        targetUserid = "47370280198"
        break
    elif k == "add":
        fileName = input("username : ")
        fileContent = input("password : ")
        with open(fileName, "w+") as f:
            f.write(fileContent)
            print(f"{fileName} added !")
        continue
    else:
        targetUsername = input("username : ")
        challenge_user = "adhiraj_ranjan"
        challenge_pass = "eplrainjdc"
        logIn, insResponse = loginInsta(challenge_user, challenge_pass)
        print(insResponse.text)
        profileJsonInfo = logIn.get(f"https://www.instagram.com/{targetUsername}/?__a=1")
        try:
            targetUserid = (json.loads(profileJsonInfo.text))['graphql']['user']['id']
            logIn.close()
            break
        except:
            print("Username entered is incorrect ! ")
            exit()

#system("clear") from os import system

# fake accounts dictionary
user_accs = {}

# Adding usernames and password to dict ( filenames in .accounts/ and file content respectively )
fileNames = listdir()
for eachName in fileNames:
    with open(eachName, "r") as f:
        accPass = f.read().strip()
    user_accs[eachName] = accPass

print("\n")
check_connection()

print(f"Initiating script to {targetUsername}...OK\n")

# starting time counter thread
startTime = threading.Thread(target=time_elapsed, args=["Time Elapsed - "]).start()


def initiate_script(fake_username, fake_password):
    global run
    # login to instagram
    instaSession, instaResponse, sessionAgent = loginInsta(fake_username, fake_password)
    try:
        fake_userid = json.loads(instaResponse.text)['userId']
    except:
        run = False
        print("\nAccount : " + fake_username + f"\033[91m - Error\033[0m\n\033[93mInstagram Response: \033[0m{instaResponse.text}\n")
        instaSession.close()
        return False
    # login to followers site
    siteSession, siteResponse = loginSite(fake_username, fake_password, fake_userid)
    new_pass = generate_password(10)
    if "success" not in siteResponse.text:
        # change password if site login fails
        isPasswordChanged = changeInstaPassword(instaSession, fake_username, fake_password, new_pass, sessionAgent)
        if "ok" in isPasswordChanged.text:
            with open(fake_username, 'w+') as f:
                f.write(new_pass)
        run = False
        print("\nAccount : " + fake_username + f"\033[91m - Error\033[0m\n\033[93mInstagram Response: \033[0m{instaResponse.text}\n\033[93mSite Response: \033[0m{siteResponse.text}\n\033[93mPassword Changed: \033[0m" + isPasswordChanged.text + "\n")
        instaSession.close()
        siteSession.close()
        return False
    sleep_time = 30
    # send followers if site login succes
    payload = {'adet': '20', 'userID': targetUserid, 'userName': targetUsername}
    siteSession.post(f"https://begeni.vip/tools/send-follower/{targetUserid}?formType=send", data=payload)
    time.sleep(sleep_time)
    siteSession.post(f"https://begeni.vip/tools/send-follower/{targetUserid}?formType=send", data=payload)
    time.sleep(sleep_time)
    siteSession.close()
    # Now change insta acc password
    isPasswordChanged = changeInstaPassword(instaSession, fake_username, fake_password, new_pass, sessionAgent)
    if 'ok' in isPasswordChanged.text:
        with open(fake_username, 'w+') as f:
            f.write(new_pass)
        run = False
        print("Account : " + fake_username + "\033[92m - OK\033[0m")
        instaSession.close()

    else:
        run = False
        print("\nAccount : " + fake_username + f"\033[91m - Error\033[0m\n\033[93mInstagram Response: \033[0m{instaResponse.text}\n\033[93mSite Response: \033[0m{siteResponse.text}\n\033[93mPassword Response: \033[0m{isPasswordChanged.text}\n")
        instaSession.close()


for fake_username, fake_password in user_accs.items():
    threading.Thread(target=initiate_script, args=[fake_username, fake_password]).start()
