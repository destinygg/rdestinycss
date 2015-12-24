#!/usr/bin/env python3
import praw
import json
import urllib.request
import html.parser
import configparser
from string import Template

# Author: Xiphirx (github/xiphirx)


class DestinySidebarUpdater:
    STREAM_THUMB_FILENAME = "streamThumb.jpg"
    configFile = "rdestiny_bot_credentials.ini"

    streamInformationTemplate = Template("""-----

[](http://www.destiny.gg/?from=reddit)


[LIVE](http://www.destiny.gg/?from=reddit#live)!
 with **$streamViewers** viewers.

Playing:

[**$streamGame**]($streamGameHomepage#gamePlaying)

-----
""")

    template = Template("""$streamInformation $sentinel $currentSidebar""")

    def __init__(self):
        # Load the bot's configuration
        self.readConfig()

        # Initialize reddit instance and login
        self.reddit = praw.Reddit(user_agent=self.redditUserAgent)
        self.reddit.set_oauth_app_info(client_id=self.oauth_client_id,
                                       client_secret=self.oauth_client_secret,
                                       redirect_uri=self.oauth_redirect_uri)

        # print(self.reddit.get_authorize_url('destinygg', 'modconfig', True))
        # self.oauth_access_info = self.reddit.get_access_information(code)
        # print(self.oauth_access_info['refresh_token'])

        self.oauth_access_info = self.reddit.refresh_access_information(
            self.oauth_refresh_token)

        # Grab the current sidebar
        self.subreddit = self.reddit.get_subreddit(self.redditSubreddit)
        self.subredditSettings = self.subreddit.get_settings()
        self.subredditDescription = self.subredditSettings["description"][
            (self.subredditSettings["description"]
                 .find(self.sentinel) + len(self.sentinel)):]

        # Grab the stylesheet
        self.subredditStylesheet = self.subreddit.get_stylesheet()
        self.subredditStylesheet = self.subredditStylesheet["stylesheet"]

        self.subredditDescription = html.unescape(self.subredditDescription)
        self.subredditStylesheet = html.unescape(self.subredditStylesheet)

    def streamInformation(self):
        # Request stream information from Twitch's REST API
        response = urllib.request.urlopen(
            "https://api.twitch.tv/kraken/streams/%s?client_id=%s"
            % (self.twitchStream, self.twitchClientID))

        encoding = response.headers.get_content_charset()
        response = response.read().decode(encoding)
        responseJSON = json.loads(response)

        # Determine if the stream is online, if so gather information
        # and return the information blurb
        if responseJSON["stream"] == None:
            return self.twitchStream + " is offline."
        else:
            streamViewers = responseJSON["stream"]["viewers"]
            streamGame = responseJSON["stream"]["game"]

        # Download the preview image to upload to the subreddit
        urllib.request.urlretrieve(responseJSON["stream"]["preview"]["small"],
                                   self.STREAM_THUMB_FILENAME)
        self.subreddit.upload_image(self.STREAM_THUMB_FILENAME, "streamThumb")

        # Force an update on the subreddit's image cache
        self.subreddit.set_stylesheet(self.subredditStylesheet)

        # Grab the game's homepage (not 100% accurate, but good enough)
        # if needed
        if (self.previousGame != streamGame):
            streamGameHomepage = self.getGameHomepage(streamGame)
            self.configParser.set("PREVIOUS_DATA", "game_homepage",
                                  streamGameHomepage)
            self.configParser.set("PREVIOUS_DATA", "game", streamGame)
        else:
            streamGameHomepage = self.previousGameHomepage

        # Save config
        self.saveConfig()

        return self.streamInformationTemplate.substitute(
            streamGame=streamGame,
            streamViewers=str(streamViewers),
            streamGameHomepage=streamGameHomepage)

    def updateSidebar(self):
        # print(self.template.substitute(
        #     streamInformation=self.streamInformation(),
        #     sentinel=self.sentinel,
        #     currentSidebar=self.subredditDescription))
        self.subreddit.update_settings(
            description=self.template.substitute(
                streamInformation=self.streamInformation(),
                sentinel=self.sentinel,
                currentSidebar=self.subredditDescription))

    # TODO: This method should be overridden with proper Google API usage
    def getGameHomepage(self, game):
        print("Grabbing homepage")
        if (game != self.previousGame):
            # Anonymous api usage should be enough for this bot
            url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0"
            "&num=1&q=%s+homepage" % (game.replace(" ", "+"))

            response = urllib.request.urlopen(url)
            encoding = response.headers.get_content_charset()
            response = response.read().decode(encoding)
            responseJSON = json.loads(response)

            if responseJSON["responseData"]["results"] == None:
                return "/"

            return responseJSON["responseData"]["results"][0]["unescapedUrl"]

        return self.previousGameHomepage

    def readConfig(self):
        self.configParser = configparser.ConfigParser()
        self.configParser.read(self.configFile)

        self.redditUser = self.configParser.get("REDDIT", "user")
        self.redditPassword = self.configParser.get("REDDIT", "password")
        self.redditUserAgent = self.configParser.get("REDDIT", "user_agent")
        self.redditSubreddit = self.configParser.get("REDDIT", "subreddit")

        self.oauth_client_id = self.configParser.get("REDDIT",
                                                     "oauth_client_id")
        self.oauth_client_secret = self.configParser.get("REDDIT",
                                                         "oauth_client_secret")
        self.oauth_redirect_uri = self.configParser.get("REDDIT",
                                                        "oauth_redirect_uri")
        self.oauth_refresh_token = self.configParser.get("REDDIT",
                                                         "oauth_refresh_token")

        self.twitchClientID = self.configParser.get("TWITCH", "client_id")
        self.twitchStream = self.configParser.get("TWITCH", "stream")

        self.previousGame = self.configParser.get("PREVIOUS_DATA", "game")
        self.previousGameHomepage = self.configParser.get("PREVIOUS_DATA",
                                                          "game_homepage")

        self.sentinel = self.configParser.get("REDDIT", "sentinel")

    def saveConfig(self):
        with open(self.configFile, "w") as config:
            self.configParser.write(config)


def main():
    sidebarBot = DestinySidebarUpdater()
    sidebarBot.updateSidebar()

if __name__ == '__main__':
    main()
