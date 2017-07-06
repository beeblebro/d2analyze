import dota2api
import json
import dataset

from conf import my_id, my_api_key

api = dota2api.Initialise(my_api_key)


def record_my_data(matches_id, fp):
    """Record only my data from my matches"""
    for match in matches_id:
        match_details = api.get_match_details(match)
        for player in match_details['players']:
            if player['account_id'] == my_id:
                json.dump(player, fp)
                fp.write('\n')


def record_matches_details(matches_id, fp):
    """Record all statistics from my matches"""
    for match in matches_id:
        match_details = api.get_match_details(match)
        json.dump(match_details, fp)
        fp.write('\n')


def get_rows(matches_id):
    """Return dict that represent a row for data base"""
    my_rows = []
    for match in matches_id:
        match_details = api.get_match_details(match)
        match_id = match_details['match_id']
        duration = match_details['duration']
        radiant_win = match_details['radiant_win']

        for player in match_details['players']:
            if player['account_id'] == my_id:
                me = player
                hero = me['hero_name']

                my_slot = me['player_slot']
                if my_slot < 5:
                    my_side = 'Radiant'
                else:
                    my_side = 'Dire'
                if (my_side == 'Radiant' and radiant_win) or (my_side == 'Dire' and not
                radiant_win):
                    result = True
                else:
                    result = False

                kills = me['kills']
                deaths = me['deaths']
                assists = me['assists']
                gpm = me['gold_per_min']
                xpm = me['xp_per_min']
                heal = me['hero_healing']
                cs = me['last_hits']

                my_rows.append({
                    'Match_ID': match_id,
                    'Duration': duration,
                    'Hero': hero,
                    'Side': my_side,
                    'Result': result,
                    'Kills': kills,
                    'Deaths': deaths,
                    'Assists': assists,
                    'GPM': gpm,
                    'XPM': xpm,
                    'Heal': heal,
                    'CS': cs
                })

    return my_rows

if __name__ == '__main__':
    db = dataset.connect('sqlite:///my_stats.db')
    my_history = api.get_match_history(my_id)
    my_matches_id = [match['match_id'] for match in my_history['matches']]
    my_rows = get_rows(my_matches_id)

    table = db['matches']
    for row in my_rows:
        table.insert(row)


