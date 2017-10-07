# Calvin Lui
# Instagram Unfollowing Checker

import re
from selenium import webdriver
from instagram_scrapper import setup_account, scrape_list

# import data from previous session
def importOldData(file):
    dataFile = open(file, "r", encoding="utf-8").read()
    data = dataFile.split()
    return data

# import data from current session
def importNewData():
    chromedriver_path = 'C:\Program Files (x86)\Google\Chrome\chromedriver'
    driver = webdriver.Chrome(chromedriver_path)

    username = setup_account(driver)
    followers = scrape_list(driver, "followers", username)
    following = scrape_list(driver, "following", username)

    driver.quit()
    return followers, following

# parse through html to obtain users
def obtainUserList(list):
    compiledList = set()
    param = "title="
    for chunk in list:
        if param in chunk:
            userBounds = [m.start() for m in re.finditer('"', chunk)]
            start, end = userBounds[0], userBounds[1]
            username = chunk[start+1:end]
            if username != "Verified":
                compiledList.add(username)
    return compiledList

#######################################################################################################################

print("Importing Data...")

oldFollowersData = importOldData("Followers.txt")
oldFollowingData = importOldData("Following.txt")

followers, following = importNewData()
followersData = followers.split()
followingData = following.split()

print("Done!")
print()

print("Obtaining Users...")

oldFollowers = obtainUserList(oldFollowersData)
oldFollowing = obtainUserList(oldFollowingData)
newFollowers = obtainUserList(followersData)
newFollowing = obtainUserList(followingData)

print("Done!")
print()

# discriminate for non-followers
print("Compiling Non-Followers List...")

# (replace following with followers to obtain "fans")
mutualFollowers = newFollowers.intersection(newFollowing)
nonFollowers = newFollowing - mutualFollowers

print("Non-Followers:")
for liquidate in nonFollowers:
    print(liquidate)
print()

"""
timePhrase = ""
if len(oldFollowers) > len(newFollowers):
    timeChange = oldFollowers - newFollowers
    timePhrase = "Lost Followers:"
elif len(newFollowers) > len(oldFollowers):
    timeChange = newFollowers - oldFollowers
    timePhrase = "Gained Followers:"
else:
    timeChange = []
    timePhrase = "No Change in Followers."

print("Done!")
print()

print(timePhrase)
for user in timeChange:
    print(user)
print()
"""

#######################################################################################################################

print("Writing Information to Text Files...")
followersFile = open("Followers.txt", "w", encoding="utf-8")
followersFile.write(followers)
followersFile.close()

followingFile = open("Following.txt", "w", encoding="utf-8")
followingFile.write(following)
followingFile.close()
print("Done!")
