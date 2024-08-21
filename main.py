import http.client
import time
import random
import json


#"global" variables
#   parsedToken
#client_id = 'e34ac0a7cfae48e5a96fa865b56bd517'
#client_secret = '3a259788d9424d369768d8ed90c5d71d'
redirect_uri = 'http://127.0.0.1:5000/index.html'

client_id = 'cd7c56ab14c94d5daf2c689fd6890fc5' #gillians
client_secret = '8a96d2cbac3045aabe53960ed9a212ee'

class Song():
  ID = ""
  Title = ""

#gives a value to parsedToken global var
def updateToken():
  conn = http.client.HTTPSConnection("accounts.spotify.com")
  payload = "grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__Host-device_id=AQBuSgKYyiF5Q6YZl-icOMjIdgcE2mBgbUrh2dQfqUpZW9UTNASE-vuxKrQkX8XMHpuGYg8fO4cMeawDNZGlArEKzk48pijwc4k'
  }
  conn.request("POST", "/api/token", payload, headers)
  res = conn.getresponse()
  data = res.read()
  token = data.decode("utf-8")
  global parsedToken #this is the global token variable... pretty important
  parsedToken = token[17:132]
  #print(parsedToken)

def requestAuthorization(): #copied this from yt video w/ program written in js
  AUTHORIZE = "https://accounts.spotify.com/authorize"
  url = AUTHORIZE
  url += "?client_id=" + client_id
  url += "&response_type=code"
  url += "&redirect_uri=" + str(redirect_uri.encode("utf-8"))
  url += "&show_dialog=true"
  url += "&scope=playlist-modify-public playlist-modify-private"
  #find way to call url and display the spotify iframe
  return url

#given: playlist URL ||| return: a list of song classes
def retrievePlaylist(givenUrl):
  conn = http.client.HTTPSConnection("api.spotify.com")
  payload = ''
  headers = {
    'Authorization': 'Bearer ' + parsedToken
  }
  conn.request("GET", "/v1/playlists/" + givenUrl + "/tracks", payload, headers)
  res = conn.getresponse()
  data = res.read()
  output = (data.decode("utf-8"))  # end of postman translated call

  jObj = json.loads(output)
  # print(jObj['total']) #get songCT

  songList = []
  for item in jObj['items']:
    song = Song()
    track = item['track']
    song.ID = track['id']
    song.Title = track['name']
    songList.append(song)

  return songList

def printPlaylist(songList):
  for s in songList:
    print(s.ID + " " + s.Title)

#given: ordered list of song ID's ||| return: a new, randomly ordered list of song ID's
def realShuffle(ogList):
  random.seed(int(round(time.time() * 1000)))
  listLen = len(ogList)
  tempList = []
  nonoList = []
  #print("List Length: " + str(listLen))

  #randomizing ints
  x = 0
  while x < listLen:
    doneYet = False
    while doneYet == False:
      randNum = random.randint(0, listLen - 1)
      if randNum not in nonoList:
        tempList.append(randNum)
        nonoList.append(randNum)
        doneYet = True
    x += 1
  #print(tempList)

  #taking randomized ints and re-assigning song IDs
  global shuffledList
  shuffledList = []
  for y in tempList:
    shuffledList.append(ogList[y].ID)
  return shuffledList

#given: unshuffled list ||| returns: nothing.                   #every function api call within this needs authorization flow...
def playPlaylist(givenList):                                    #every function api call within this needs to be parsed
  def addToQueue(songID):
    #get song info and save the title as a variable to use in the final print statement
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("POST", "/v1/me/player/queue?uri=spotify%253Atrack%253A" + songID, payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    fullText = data.decode("utf-8")

    print("Added " + songID + " to Queue.") #eventually exchange this for the actual song title

  def skipCurrent():
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("POST", "/v1/me/player/next", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    print("Track Skipped")

  def getQueue():
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("GET", "/v1/me/player/queue", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

  def getPBState():
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("GET", "/v1/me/player", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

  def pause():
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("PUT", "/v1/me/player/pause", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    print("Track Paused")

  def resume():
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("PUT", "/v1/me/player/play", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    print("Track Started/Resumed")

  def repeatOff():
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("PUT", "/v1/me/player/repeat?state=off", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    print("Repeat Turned Off.")

  def shuffleOff():
    conn = http.client.HTTPSConnection("api.spotify.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + parsedToken
    }
    conn.request("PUT", "/v1/me/player/shuffle?state=false", payload, headers) #spotify site uses this format for the true statement and the false one gave an error so I'm guessing...
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    print("Shuffle Turned Off.")

  getPBState()
  #if playing
  pause()
  #if shuffle
  shuffleOff()
  #if repeat
  repeatOff()

  getQueue()
  skipCurrent()
  #repeat as needed. depends on what getQueue returns

  for x in givenList:
    addToQueue(x)
  resume()


updateToken()

#fiveSongPL = retrievePlaylist("3cEYpjA9oz9GiPac4AsH4n")
#minecraftPL = retrievePlaylist("3XCD3qCast9BQZgxSHEzP8")
gillians = retrievePlaylist("5l2YXYL3Bydr69SYIZIJT5")

#printPlaylist(fiveSongPL)
#print()
#printPlaylist(minecraftPL)
#print()
printPlaylist(gillians)
print()

# realShuffle(fiveSongPL)
# realShuffle(minecraftPL)

#print(realShuffle(fiveSongPL))
#print(realShuffle(minecraftPL))
print(realShuffle(gillians))
playPlaylist(gillians)
#playPlaylist(fiveSongPL) #the operations within this shouldn't work without a device id and user approval of third-party API control
#playPlaylist(minecraftPL)