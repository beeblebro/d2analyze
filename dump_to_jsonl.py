import dota2api
import json

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


def update_jsonl_files():
    my_history = api.get_match_history(my_id)
    my_matches_id = [match['match_id'] for match in my_history['matches']]
    my_stats_file = open("my_stats.jsonl", 'w')
    my_matches_file = open("my_matches_file.jsonl", 'w')

    record_my_data(my_matches_id, my_stats_file)
    record_matches_details(my_matches_id, my_matches_file)

    my_stats_file.close()
    my_matches_file.close()


if __name__ == '__main__':
    my_history = api.get_match_history(my_id)
    my_matches_id = [match['match_id'] for match in my_history['matches']]
    my_stats_file = open("my_stats.jsonl", 'w')
    my_matches_file = open("my_matches_file.jsonl", 'w')

    record_my_data(my_matches_id, my_stats_file)
    record_matches_details(my_matches_id, my_matches_file)

    my_stats_file.close()
    my_matches_file.close()
