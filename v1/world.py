#!/usr/bin/env python

from bson.objectid import ObjectId
from datetime import datetime, timedelta
from optparse import OptionParser

import assets
import game_assets
import html
import session
from utils import mdb, get_percentage, ymd, admin_session
from models import Quarries, Nemeses, mutually_exclusive_principles



#
#   Canned Queries with normal results
#

def multiplayer_settlements(return_type=False, threshold=1):
    """ Returns settlements with players greater than 'threshold'. """

    totals = {}
    all_survivors = mdb.survivors.find()
    for s in all_survivors:
        if s["settlement"] not in totals.keys():
            totals[s["settlement"]] = set([s["created_by"]])
        else:
            totals[s["settlement"]].add(s["created_by"])

    multiplayer = {}
    for s in totals.keys():
        players = len(totals[s])
        if players > threshold:
            multiplayer[s] = players

    if return_type == "total_settlements":
        return len(multiplayer.keys())
    elif return_type == "raw":
        return totals

    return multiplayer


def current_hunt(return_type=False):
    """ Uses settlements with a 'current_quarry' attribute to determine who is
    currently hunting monsters. """
    try:
        settlement = mdb.settlements.find({"name": {"$nin": ["Test", "Unknown"]}, "current_quarry": {"$exists": True}, "hunt_started": {"$gte": datetime.now() - timedelta(minutes=180)}}).sort("hunt_started", -1)[0]
    except:
        return "No settlements are currently hunting monsters."

    # bail if we've got no settlements with 'current_quarry' flags
    if settlement is None:
        return "No settlements are currently hunting monsters."

    # otherwise, let's do this thing:
    hunters = mdb.survivors.find({"settlement": settlement["_id"], "in_hunting_party": {"$exists": True}}).sort("name")
    if hunters.count() == 0:
        return "No settlements are currently hunting monsters."
    elif hunters.count() == 1:
        hunter = mdb.survivors.find_one({"settlement": settlement["_id"], "in_hunting_party": {"$exists": True}})
        return "%s of <b>%s</b> is currently out hunting! Quarry: %s" % (hunter["name"], settlement["name"], settlement["current_quarry"])
    elif hunters.count() >= 2:
        hunter_names = []
        for h in hunters:
            hunter_names.append(h["name"])
        hunter_string = ", ".join(hunter_names[:-1])
        hunter_string += " and %s of <b>%s</b>" % (hunter_names[-1], settlement["name"])
        hunter_string += " are currently out hunting! Quarry: %s" % (settlement["current_quarry"])
        return hunter_string
    else:
        return "An error occurred while gathering information about the latest monster hunt."


def latest_kill(return_type=False):
    """ Returns the latest defeated monster from mdb.killboard. """
    l = mdb.killboard.find_one({"settlement_name": {"$nin": ["Test", "Unknown"]}}, sort=[("created_on", -1)])
    if l is None:
        return None

    if return_type == "admin_panel":
        output = "%s: %s (%s)" % (l["created_on"].strftime(ymd), l["name"], l["settlement_name"])
    else:   # all other return_type values
        output = "<li><b>%s</b></li>" % l["name"]
        ly = l["kill_ly"].split("_")[1]
        output += "<li>Defeated by the survivors of <b>%s</b> in LY %s on %s at %s (CT).</li>" % (l["settlement_name"], ly, l["created_on"].strftime(ymd), l["created_on"].strftime("%H:%M:%S"))

    return output


def survivor_html(s, item=False):
    """ Helper function that returns survivor HTML for dashboard/panel use. """
    output = ""

    if item == "avatar":
        if "avatar" in s.keys():
            output = html.dashboard.avatar_image.safe_substitute(name=s["name"], avatar_id=s["avatar"])
    elif item == "epithets":
        if "epithets" in s.keys() and s["epithets"] != []:
            epithets = ", ".join(s["epithets"])
            output = "<li><i>%s</i></li>" % epithets

    return output


def latest_settlement(return_type="html"):
    """ Returns the most recently created settlement with a real name and
    survivors."""
    latest_settlement = mdb.settlements.find_one(
        {
            "population": {"$gt": 0},
            "name": {"$nin": ["Unknown", "Test", "test"]},
        },
        sort=[("created_on", -1)],
    )

    player_set = set()
    survivors = mdb.survivors.find({"settlement": latest_settlement["_id"]})
    for s in survivors:
        player_set.add(s["email"])
    Settlement = assets.Settlement(settlement_id=latest_settlement["_id"], session_object=admin_session, update_mins=False)

    if return_type == "html":
        output = "<p>Latest Settlement:</p><ul><li><b>%s</b></li>" % latest_settlement["name"]
        output += "<li>&nbsp; <i>%s</i></li>" % Settlement.get_campaign()
        output += "<li>Expansions: %s</li>" % Settlement.get_expansions("comma-delimited")
        output += "<li>Players: %s</li>" % len(player_set)
        output += "<li>Created on: %s</li>" % latest_settlement["created_on"].strftime(ymd)
        output += "<li>Population: %s</li>" % latest_settlement["population"]
        output += "</ul>"
        return output

    return latest_settlement


def latest_survivor(return_type="html"):
    """ Returns the most recently created survivor with a real name. """
    latest_survivor = mdb.survivors.find_one(
        {
            "dead": {"$exists": False},
            "name": {"$nin": ["Test", "Anonymous", "test"]},
        },
        sort=[("created_on", -1)],
    )

    if return_type == "html":
        output = '<p>Newest survivor: %s<br/><ul>' % survivor_html(latest_survivor, item="avatar")
        settlement = mdb.settlements.find_one({"_id": latest_survivor["settlement"]})
        output += "<li><b>%s</b> of <b>%s</b></li>" % (latest_survivor["name"], settlement["name"])
        output += survivor_html(latest_survivor, item="epithets")
        if "mother" in latest_survivor.keys() or "father" in latest_survivor.keys():
            output += "<li>Born in LY %s</li>" % latest_survivor["born_in_ly"]
        else:
            output += "<li>Joined the settlement in LY %s</li>" % latest_survivor["born_in_ly"]
        output += "</ul></p>"
        return output

    return latest_survivor


def latest_fatality(return_type="html"):
    """ Returns the latest fatality from mdb.the_dead. """
    latest_fatality = mdb.the_dead.find_one(
        {
            "complete": {"$exists": True},
            "name": {"$nin": ["Anonymous","Test"]},
            "cause_of_death": {"$ne": "Forsaken."},
        },
        sort=[("created_on", -1)],
        )

    if return_type == "html":
        output = '<p>Latest fatality: %s<br/><ul>' % survivor_html(latest_fatality, item="avatar")
        output += '<li><b>%s</b> of <b>%s</b></li>' % (latest_fatality["name"], latest_fatality["settlement_name"])
        output += survivor_html(latest_fatality, item="epithets")
        output += '<li>Cause of death: %s<br/>&ensp; Died in LY %s, XP: %s</li>' % (latest_fatality["cause_of_death"], latest_fatality["lantern_year"], latest_fatality["hunt_xp"]) 
        output += '<li>Courage: %s, Understanding: %s</li>' % (latest_fatality["Courage"], latest_fatality["Insanity"])
        output += '</ul></p>'
        return output

    return latest_fatality


def kill_board(return_type=None, admin=False):
    """ Creates a dictionary showing kills by monster type. """
    kill_list = []
    all_settlements = mdb.settlements.find()
    for settlement in all_settlements:
        for m in settlement["defeated_monsters"]:
            kill_list.append(m)

    monsters = {"Other": {"sort_order": 99, "tokens": ["OTHER"], }}
    others = []
    for model in [Quarries, Nemeses]:
        monsters.update(model.game_assets)
    for m in monsters:
        monsters[m]["kills"] = 0
        monsters[m]["name"] = m

    for kill in kill_list:
        categorized = False
        k_tokenized = kill.upper().split()
        for monster in monsters.keys():
            if kill.upper() in monsters[monster]["tokens"]:
                categorized = True
                monsters[monster]["kills"] += 1
            if not categorized:
                for k_token in k_tokenized:
                    if k_token in monsters[monster]["tokens"]:
                        categorized = True
                        monsters[monster]["kills"] += 1
        if not categorized:
            others.append(kill)
            monsters["Other"]["kills"] += 1

    sorted_monsters = {}
    for m in monsters:
        sorted_monsters[monsters[m]["sort_order"]] = monsters[m]

    if return_type == "html_table_rows":
        output = ""
        for numerical_key in sorted(sorted_monsters.keys()):
            monst_dict = sorted_monsters[numerical_key]
            monst_html = html.dashboard.kill_board_row.safe_substitute(monster = monst_dict["name"], kills = monst_dict["kills"])
            output += monst_html
        if admin:
            output += html.dashboard.kill_board_foot.safe_substitute(other_list = ", ".join(sorted(others)))
        return output

    return sorted_monsters


def top_principles(return_type=None):
    """ Determines which principles are most popular. """

    popularity_contest = {}
    for principle in mutually_exclusive_principles.keys():
        tup = mutually_exclusive_principles[principle]
        sample_set = mdb.settlements.find({"principles": {"$in": tup} }).count()
        popularity_contest[principle] = {"sample_size": sample_set, "options": tup}
        for option in tup:
            total = mdb.settlements.find({"principles": {"$in": [option]}}).count()
            popularity_contest[principle][option] = {
                "total": total,
                "percentage": int(get_percentage(total, sample_set)),
            }

    if return_type == "html_ul":
        output = "<ul>\n"
        for k in popularity_contest.keys():
            output += "<li>%s Principle:\n\t<ul>\n" % k
            for principle in popularity_contest[k]["options"]:
                output += "<li>%s%% - %s</li>\n" % (popularity_contest[k][principle]["percentage"], principle) 
            output += "\t</ul>\n</li>"
        output += '</ul>\n\n'
        return output

    return popularity_contest


def expansion_popularity_contest(return_type=None):
    """ Creates a dict of expansion use across all settlements. """
    exp_dict = {}
    for expansion in game_assets.expansions.keys():
        exp_dict[expansion] = mdb.settlements.find({"expansions": {"$in": [expansion]}}).count()
    output = ""
    for k in sorted(exp_dict.keys()):
        v = exp_dict[k]
        output += "<li>%s: %s</li>" % (k, v)
    return output



#
#   Averages and min/max queries for settlements and survivors
#

def get_minmax(attrib="population"):
    """ Gets the highest/lowest value for an attrib in all settlements. """
    data_points = []
    sample_set = mdb.settlements.find({"population": {"$gt": 4}, "death_count": {"$gt": 0}})
    for sample in sample_set:
        data_points.append(int(sample[attrib]))
    return min(data_points), max(data_points)


def user_average(return_type=False):
    """ Returns averages re: users. """

    user_counts = {}
    for user in mdb.users.find():
        settlement_count = mdb.settlements.find({"created_by": user["_id"]}).count()
        survivor_count = mdb.survivors.find({"created_by": user["_id"]}).count()
#       gridfs queries need version 2.7+ of the gridfs pymongo driver
#        avatar_count = gridfs.GridFS(mdb).find({"created_by": user["_id"]}).count()
        avatar_count = mdb.survivors.find({"created_by": user["_id"], "avatar": {"$exists": True}}).count()
        user_counts[user["_id"]] = {"settlements": settlement_count, "survivors": survivor_count, "avatars": avatar_count}

    averages = {"settlements": 0, "survivors": 0, "avatars": 0}
    for asset in averages.keys():
        data_points = []
        for user in user_counts.keys():
            data_points.append(user_counts[user][asset])
        result = reduce(lambda x, y: x + y, data_points) / float(len(data_points))
        averages[asset] = round(result,2)

    if return_type:
        return averages[return_type]

    return averages


def get_average(collection="settlements", attrib="population", precision=2, return_type=int):
    """ Gets averages for either settlements or survivors. Re-state my
        assumptions:

            1.) make sure you're setlecting an attrib that's numeric. If you
                specify a non-numeric attribute, we're going to calculate the
                len() of the attribute and use that. Which...can get weird.
            2.) documents that don't have your target attrib are ignored
            3.) rounding to a precision of 2 is the default
            4.) we're querying settlements with population higher than 4 or a
                    LY greater than 2 and at least one dead survivor
            5.) we're only querying survivors who aren't dead

    """

    # first, set our query based on the collection we're interrogating
    query = {attrib: {"$exists": True}}
    if collection == "settlements":
        query.update({"$or": [{"population": {"$gt": 4}}, {"lantern_year": {"$gt": 2}}], "death_count": {"$gt": 0}})
    elif collection == "survivors":
        query.update({"dead": {"$exists": False}})
    else:
        raise Exception("Unsupported collection type! '%s' cannot be queries!" % collection)

    # now, start crunching
    data_points = []
    sample_set = mdb[collection].find(query)
    for sample in sample_set:
        try:
            data_points.append(return_type(sample[attrib]))
        except:
            data_points.append(return_type(len(sample[attrib])))
    result = reduce(lambda x, y: x + y, data_points) / len(data_points)
    if return_type == int:
        return result
    elif return_type == float:
        return round(result, precision)





if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", dest="user_avg", help="Returns averages re: users. Try: 'survivors', 'settlements', 'avatars'", metavar="survivors", default=False)
    parser.add_option("-a", dest="average", help="Returns an average for the specified value", metavar="population", default=False)
    parser.add_option("-m", dest="minmax", help="Returns min/max numbers the specified value", metavar="death_count", default=False)
    parser.add_option("-M", dest="multiplayer", help="Dump the multiplayer settlement count.", default=False, action="store_true")
    parser.add_option("-k", dest="kill_board", help="Run the kill_board func and print its contents.", default=False, action="store_true")
    parser.add_option("-p", dest="top_principles", help="Run the top_principles func and print its contents.", default=False, action="store_true")
    (options, args) = parser.parse_args()

    start = datetime.now()

    if options.user_avg:
        print user_average(options.user_avg)
    if options.multiplayer:
        print multiplayer_settlements()
    if options.kill_board:
        print kill_board()
    if options.top_principles:
        print top_principles()
    if options.average:
        print get_average(options.average)
    if options.minmax:
        print get_minmax(options.minmax)

    stop = datetime.now()
    duration = stop - start
    print("Requested operations completed:\n Seconds: %s\n Microseconds: %s\n" % (duration.seconds, duration.microseconds))
