import urllib.request
import json
import time
import os 
import sys 
import configparser
from pypresence import Presence
from pypresence.types import ActivityType

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    global discordAppID
    global urlToSonosAPI
    discordAppID = int(config.get('General', 'discordAppID'))
    urlToSonosAPI = config.get('General', 'urlToSonosAPI')

def getJson():
    try:
        unparsedJson = urllib.request.urlopen(urlToSonosAPI).read()
    except urllib.error.HTTPError as e:
        print("Sonos API connection error,Is it running properly?")
        sys.exit()
    except urllib.error.URLError as e:
        print("Sonos API connection error,Is it running properly?")
        sys.exit()
    parsedJson = json.loads(unparsedJson)
    return parsedJson

def timeSyncCheck(songTimeStart,parsedJson,songTimeEnd):
    elapsedTime = int(parsedJson["elapsedTime"])
    #This checks if the time difference has changed by more than or less than 2 seconds 
    #and update the time if it has 
    if songTimeStart+elapsedTime >2+int(time.time()) or songTimeStart +elapsedTime < int(time.time())-2:
        songTimeStart,songTimeEnd = timeConstruct(parsedJson)
    return songTimeStart,songTimeEnd

def timeConstruct(parsedJson):
    elapsedTime = int(parsedJson["elapsedTime"])
    songTimeStart=int(time.time())-elapsedTime
    songTimeEnd = songTimeStart +int(parsedJson["currentTrack"]["duration"])
    return songTimeStart,songTimeEnd

def rpcConstructer(parsedJson,songTimeStart,songTimeEnd):
    RPC.update(
        name = parsedJson["currentTrack"]["artist"],
        activity_type=ActivityType.LISTENING,
        details = parsedJson["currentTrack"]["title"],
        state = parsedJson["currentTrack"]["artist"],
        large_image=(parsedJson["currentTrack"]["absoluteAlbumArtUri"]),
        start = songTimeStart,
        end = songTimeEnd)
    return

read_config()
RPC = Presence(discordAppID)
RPC.connect()
songTimeStart,songTimeEnd=0,0
while True:
    parsedJson = getJson()
    #clear the queue if the playback is paused or stopped or if duration is at default(0)
    while parsedJson["playbackState"] !="PLAYING" or parsedJson["currentTrack"]["duration"] ==0:
        parsedJson = getJson()
        RPC.clear(pid=os.getpid())
        time.sleep(2)
    songTimeStart,songTimeEnd=timeSyncCheck(songTimeStart,parsedJson,songTimeEnd)
    rpcConstructer(parsedJson,songTimeStart,songTimeEnd)
    time.sleep(0.8)

