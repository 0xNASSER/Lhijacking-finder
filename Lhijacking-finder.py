import re
import requests
import sys

# These lists will contains the social media accounts, to avoid testing the same account multiple times
tw_accounts = []
sn_accounts = []
yt_accounts = []
fc_accounts = []
tel_accounts = []
ig_accounts = []


def find_social_media_links(url):
    # Send a request to get the website content
    website_content = requests.get(url, allow_redirects=True).text

    # regex to find the social media links
    social_media_links = re.findall(r'https?:\/\/(?:www\.)?(instagram\.com|twitter\.com|facebook\.com|snapchat\.com|youtube\.com|t\.me)\/(channel\/|user\/|c\/|add\/)?([^\s\"\'\?\/\\]+)', website_content)

    for link in social_media_links:

        # Check if the link is a Twitter profile, then check if it's exist or not
        if "twitter" in link[0] and link[2] not in tw_accounts:
            tw_accounts.append(link[2])

            # send a request to Twitter API to check if the username of the account exist or not
            try:
                twitter_profile_page = requests.get(
                    "https://api.twitter.com/i/users/username_available.json?username=" + link[2]).text
                # If the username not exist tell me!
                if "Available!" in twitter_profile_page:
                    print("Result for: " + url)
                    print("\033[92m[*] Twitter account doesn’t exist: https://twitter.com/" + link[2] + "\033[0m\n\n")
            except:
                pass

        # Check for Snapchat
        elif "snapchat" in link[0] and link[2] not in sn_accounts:
            sn_accounts.append(link[2])
            # check if the status code is 404 that's mean the username is not exist
            try:
                snapchat_profile_page = requests.get("https://www.snapchat.com/add/" + link[2]).status_code
                if snapchat_profile_page == 404:
                    print("Result for: " + url)
                    print(
                        "\033[92m[*] SnapChat account doesn’t exist: https://snapchat.com/add/" + link[2] + "\033[0m\n")
            except:
                pass

        # Check for YouTube
        elif "youtube" in link[0] and "iframe_api" not in link[2] and link[2] not in yt_accounts:
            yt_accounts.append(link[2])

            try:
                youtube_profile_page = requests.get("https://youtube.com/" + link[1] + link[2]).status_code
                if youtube_profile_page == 404:
                    print("Result for: " + url)
                    print("\033[92m[*] YouTube account doesn’t exist: https://youtube.com/" + link[1] + link[2] + "\033[0m\n\n")
            except:
                pass

        # Check for FaceBook
        elif "facebook" in link[0] and link[2] not in fc_accounts:
            fc_accounts.append(link[2])

            try:
                facebook_profile_page = requests.get("https://graph.facebook.com/" + link[2]).text
                if "does not exist" in facebook_profile_page:
                    print("Result for: " + url)
                    print("\033[92m[*] Facebook account doesn’t exist: https://facebook.com/" + link[2] + "\033[0m\n\n")
            except:
                pass

        # Check fro Telegram
        elif "t.me" in link[0] and link[2] not in tel_accounts:
            tel_accounts.append(link[2])

            try:
                telegram_profile_page = requests.get(("https://t.me/" + link[2])).text
                if "you can contact" in telegram_profile_page:
                    print("Result for: " + url)
                    print("\033[92m[*] Telegram account doesn’t exist: https://t.me/" + link[2] + "\033[0m\n\n")
            except:
                pass

        # Check for instagram
        elif "instagram" in link[0] and link[2] not in ig_accounts:
            ig_accounts.append(link[2])

            try:
                instagram_profile_page = requests.get(
                    "https://www.instagram.com/web/search/topsearch/?query=" + link[2]).text
                if 'users":[]' in instagram_profile_page:
                    print("Result for: " + url)
                    print(
                        "\033[92m[*] Instagram account doesn’t exist: https://instagram.com/" + link[2] + "\033[0m\n\n")

            except:
                pass


arg = sys.argv[1]
# Check if the input is a link or a file
if arg.startswith('https://') or arg.startswith('http://'):
    # Execute the function with the link
    find_social_media_links(arg)
else:
    # The argument is a file, so read the file line by line
    with open(arg, 'r') as file:
        for line in file:
            # Pass each line (URL) to the function
            find_social_media_links(line.strip())
