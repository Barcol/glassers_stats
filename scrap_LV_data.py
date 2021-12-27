# python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime as date
from os import path
from collections import ChainMap

final_result = {}

today_date = date.today().strftime("%Y-%m-%d")

final_result["date"] = today_date
final_result["precise_date"] = date.today().strftime("%Y-%m-%d, %H:%M")


# Players Part

nicknames = ["e46-w-kompocie", "gandalf-zielony", "vinne", "jan-karze-3", "rafau", "jasen", "rebeusus", "kibel", "szaowyOl12", "nisert", "twardomir", "wujas", "azja", "huj", "trooll1980"]

raw_htmls = [requests.get(f"https://api.lost-vault.com/players/{nickname}/") for nickname in nicknames]

attribute_colours = {"str": "red", "agi": "orange", "end": "yellow", "int": "olive", "lck": "green"}
ext_attributes_colours = {"lvl": "red", "rank": "yellow", "fame": "green", "power": "olive"}
achievement_colours = {"explores": "green", "quests": "olive", "monsters": "yellow", "caravan": "orange", "vault": "pink", "survival": "red"}

final_result["players"] = []
final_result["tribes"] = []

print("Scrapowanie graczy")
for html in raw_htmls:
    soup = BeautifulSoup(html.text, 'html.parser')

    # Name
    name_soup = soup.find("h1")
    name_soup.find("div").decompose()
    player_name = name_soup.get_text().replace("[Glassers]", "").strip()

    print(player_name)


    # Attributes
    attributes = [{attribute: soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip()} for attribute, colour in attribute_colours.items()]
    attributes = dict(ChainMap(*attributes))
    soup.find(class_="ui inverted segment").decompose()

    # External Attributes
    ext_attributes = [{attribute: soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip()} for attribute, colour in ext_attributes_colours.items()]
    ext_attributes = dict(ChainMap(*ext_attributes))

    soup.find(class_="ui inverted segment").decompose()

    #Achievement Attributes
    ach_attributes = [{attribute: soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip()} for attribute, colour in achievement_colours.items()]
    ach_attributes = dict(ChainMap(*ach_attributes))

    soup.find(class_="ui inverted segment").decompose()

    # Assign to JSON
    final_result["players"].append({"name": player_name, "attributes": attributes, "ext_attributes": ext_attributes, "ach_attributes": ach_attributes})

# Tribes part

guild_names = ["glassers", "turkish-army", "stalkerz", "parlament", "axischurch", "arroyo", "idle-fix", "power-trip", "hyperia", "spirituality", "the-sphere",
 "exiled", "luscea", "guild-7", "latam_raiders", "havoc", "farmrpg", "elysium", "stormblood", "brewers-guild",
 "guild-5", "raiders", "nightmare-rats", "the-light", "fenrir", "bloodhounds", "old-guard", "real-sociedade", "bumpmap",
 "darkwarriors", "destroyers", "chayka", "skcz-legion", "foamy-scamps", "mercs", "monolit", "russians-coming",
 "desert-rangers", "star-children", "legion", "charlie-squad", "german-elite", "haventus", "guild-3", "eclipse-academy",
 "old-gamers", "free2play", "winged-hussars", "inferno", "grom", "top", "elit", "guild", "guild-2", "team-squad",
 "the-tavern", "bravo-squad", "dakar", "the-lotus", "clarity", "flawless", "eclipse", "alpha-squad"]

raw_guild_htmls = [requests.get(f"https://api.lost-vault.com/tribes/{tribe_name}/") for tribe_name in guild_names]

guild_parameter_colours = {"lvl": "red", "members": "orange", "reactor": "yellow"}
guild_result_colours = {"rank": "yellow", "fame": "green", "power": "olive"}

print("====================================")
print("Scrapowanie gildii")

for html in raw_guild_htmls:
    soup = BeautifulSoup(html.text, 'html.parser')

    # Name
    tribe_name = soup.find("h1").get_text().strip()
    print(tribe_name)

    # Guild parameters
    guild_parameters = [{attribute: soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip()} for attribute, colour in guild_parameter_colours.items()]
    guild_parameters = dict(ChainMap(*guild_parameters))

    soup.find(class_="ui inverted segment").decompose()

    # Guild results
    guild_results = [{attribute: soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip()} for attribute, colour in guild_result_colours.items()]
    guild_results = dict(ChainMap(*guild_results))

    soup.find(class_="ui inverted segment").decompose()

    # Assign to JSON
    final_result["tribes"].append({"name": tribe_name, "guild_parameters": guild_parameters, "guild_results": guild_results, "endpoint": html.url})


print("====================================")
print("Wyniki koncowe:")

print(json.dumps(final_result))

filename = f"database/{today_date}.json"
listObj = []

with open(filename, 'w') as json_file:
    json.dump(final_result, json_file,
                        indent=4,
                        separators=(',',': '))

print(f"Successfully created {today_date} to the JSON file")
