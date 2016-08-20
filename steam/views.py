from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import urllib2
import json

# Create your views here.
def home(request):
	return render(request, 'steam/home.html')

def results(request):
	if request.method == 'POST':
		
		steamid = request.POST.get('steamid')
		try:
			#extract steamid 64 from custom id
			if not steamid[:6] == "765611":
				getId = urllib2.urlopen('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=2BF34BF3688F0651D3D5A96C93740CB5&vanityurl=' + steamid)
				jsonIdData = json.load(getId)
				if jsonIdData['response']['success'] == 1:
					steamid = jsonIdData['response']['steamid']
				else:
					return render(request, 'steam/notfound.html')

			#extract data using steamid 64
			file = urllib2.urlopen('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=2BF34BF3688F0651D3D5A96C93740CB5&steamid=' + steamid + '&include_appinfo=1&include_played_free_games=1&format=json')
		
		except urllib2.HTTPError, e:
			if e.code == 500:
				return render(request, 'steam/notfound.html')
		else:
			data = json.load(file)
			file.close()
			#games key only exists if profile is public
			if 'games' in data["response"]:
				gamesSorted = sorted(data["response"]["games"], key=lambda time: time["playtime_forever"], reverse=True)[:10]
				json_data = json.dumps(gamesSorted, indent=2)
				return render_to_response('steam/results.html', {'json_data': json_data})
			else:
				return render(request, 'steam/private.html')
