import urllib2, json
PA_TWITCH = 'https://api.twitch.tv/kraken/streams?game=Planetary%20Annihilation'
def twitch_streams():
    response = urllib2.urlopen(PA_TWITCH)
    print response
    return json.load(response)['streams']
