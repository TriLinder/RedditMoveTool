import time
import praw

def createAppTutorial(wait) :
    time.sleep(wait)
    print("Click on \"Create another app\"")
    time.sleep(wait)
    print("Fill it out like in this screenshot https://i.imgur.com/7ne1Gdu.png")
    time.sleep(wait)
    print("Click on \"create app\"")
    time.sleep(wait)

print("Reddit Move Tool")
print("By TriLinder\n")

srcUsername = input("Please enter the username of the source Reddit account: ").strip("u/").strip()
srcPswd = input("Please input %s's password: " % (srcUsername))
srcHas2FA = input("Does %s have 2FA on? y/N: " % (srcUsername)).lower() == "y"

print("\n-------\n\nPlease log in as %s and then go to https://www.reddit.com/prefs/apps" % (srcUsername))
createAppTutorial(.2)

srcID = input("\nPlease input the Client ID https://i.imgur.com/7dPQOWp.png : ")
srcSecret = input("Please input the Secret https://i.imgur.com/JmPKYVj.png : ")
time.sleep(.4)

if srcHas2FA :
    src2FA = ":" + input("\nPlease input %s's 2FA Code: " % (srcUsername)).replace(" ", "")
else :
    src2FA = ""

srcReddit = praw.Reddit(
    client_id=srcID,
    client_secret=srcSecret,
    user_agent="A Python tool to move saved posts and subscribed subreddits to a diffrent account.",
    username=srcUsername,
    password=srcPswd + src2FA,
)


print("\nDownloading info, this may take up to a few minutes..")

try :
    srcSubreddits = list(srcReddit.user.subreddits(limit=None))
except :
    input("Oh no! Downloading failed, please check that you entered the right info..")
    quit()

srcSaved = []

for item in srcReddit.user.me().saved(limit=None) :
    srcSaved.append(item)

print("\n%s connected!" % (srcUsername))


#------------------------------

dstUsername = input("\n\nPlease enter the username of the destination Reddit account: ").strip("u/").strip()
dstPswd = input("Please input %s's password: " % (dstUsername))
dstHas2FA = input("Does %s have 2FA on? y/N: " % (dstUsername)).lower() == "y"

print("\n-------\nPlease log in as %s and then go to https://www.reddit.com/prefs/apps" % (dstUsername))
createAppTutorial(.2)

dstID = input("\n\nPlease input the Client ID https://i.imgur.com/7dPQOWp.png : ")
dstSecret = input("Please input the Secret https://i.imgur.com/JmPKYVj.png : ")
time.sleep(.1)

if dstHas2FA :
    dst2FA = ":" + input("\nPlease input %s's 2FA Code: " % (dstUsername)).replace(" ", "")
else :
    dst2FA = ""

dstReddit = praw.Reddit(
    client_id=dstID,
    client_secret=dstSecret,
    user_agent="A Python tool to move saved posts and subscribed subreddits to a diffrent account.",
    username=dstUsername,
    password=dstPswd + dst2FA,
)

print("\nDownloading info, this may take up to a few minutes..")

try :
    dstReddit.user.me().id
except :
    input("Oh no! Downloading failed, please check that you entered the right info..")
    quit()

print("\n%s connected!" % (dstUsername))

#------------------------------

transferSubreddits =  not input("\nTransfer %d subreddits? This should take about %d seconds. Y/n " % (len(srcSubreddits), len(srcSubreddits) * 4)).lower() == "n"
transferSaved =  not input("Transfer %d saved posts and comments? This should take about %d seconds. Y/n " % (len(srcSaved), len(srcSaved) * 8)).lower() == "n"

#------------------------------

startTime = time.time()
expectedTime = 0

print("\n")

i = 0

if transferSubreddits :
    expectedTime = expectedTime + len(srcSubreddits) * 4
    for x in srcSubreddits :
        i = i + 1
        try :
            subreddit = dstReddit.subreddit(str(x))
            subreddit.subscribe()
            time.sleep(4)
        except :
            pass
        print("Transfering subreddits: %d/%d" % (i, len(srcSaved)))

print("\n----\nSubreddits transferd!\n----\n")
i = 0

if transferSaved :
    expectedTime = expectedTime + len(srcSaved) * 8
    for x in srcSaved :
        i = i + 1
        try :
            submission = dstReddit.submission(id=x)
            submission.save()
        except :
            try :
                comment = dstReddit.comment(id=x)
                comment.save()
            except :
                pass
        print("Transfering saved: %d/%d" % (i, len(srcSaved)))
        time.sleep(8)

print("\n\nFinished in %d seconds, expected time was %d seconds." % (round(time.time() - startTime), expectedTime))
input("Press [ENTER] to quit..")
quit()