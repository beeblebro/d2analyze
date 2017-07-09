import operator
import json
import matplotlib.pyplot as plt
import numpy as np
import pygal

from dump_to_jsonl import update_jsonl_files

from conf import my_id


def get_my_heroes(my_stats_fp):
    """Get my heroes from my statistics file"""
    heroes = []
    for line in my_stats_fp:
        my_stats = json.loads(line)
        heroes.append(my_stats['hero_name'])
    my_stats_fp.seek(0, 0)
    return heroes


def get_gpm(my_stats_fp):
    """Get Gold Per Minute"""
    gpm = []
    for line in my_stats_fp:
        my_stats = json.loads(line)
        gpm.append(my_stats['gold_per_min'])
    my_stats_fp.seek(0, 0)
    return gpm


def get_xpm(my_stats_fp):
    """Get eXperience Per Minute"""
    xpm = []
    for line in my_stats_fp:
        my_stats = json.loads(line)
        xpm.append(my_stats['xp_per_min'])
    my_stats_fp.seek(0, 0)
    return xpm


def get_kda(my_stats_fp):
    """Get KDA ratio = (kills - assists) / max(deaths, 1)"""
    kda = []
    for line in my_stats_fp:
        my_stats = json.loads(line)
        kda.append((my_stats['kills'] + my_stats['assists']) / max(my_stats['deaths'], 1))
    my_stats_fp.seek(0, 0)
    return kda


def get_win_rate(my_matches_fp):
    """Calculate win rate"""
    result = []
    for line in my_matches_fp:
        my_match = json.loads(line)
        radiant_win = my_match['radiant_win']

        for player in my_match['players']:
            if player['account_id'] == my_id:
                me = player
                my_slot = me['player_slot']
                if my_slot < 5:
                    my_side = 'Radiant'
                else:
                    my_side = 'Dire'

                if (my_side == 'Radiant' and radiant_win) or (my_side == 'Dire' and not
                radiant_win):
                    res = 1
                else:
                    res = 0

                result.append(res)
    my_matches_fp.seek(0, 0)
    return sum(result)


def get_durations(my_stats_fp):
    """Get matches durations [min] from matches file"""
    durs = []
    for line in my_stats_fp:
        match = json.loads(line)
        durs.append(match['duration'] / 60)
    my_stats_fp.seek(0, 0)
    return durs


def get_fb_time(my_matches_fp):
    """Get first blood times [min]"""
    fb_t = []
    for line in my_matches_fp:
        match = json.loads(line)
        fb_t.append(match['first_blood_time'] / 60)
    my_matches_fp.seek(0, 0)
    return fb_t


def print_summary(my_stats_fp, my_matches_fp):
    """Print some statistic summary"""
    my_heroes = get_my_heroes(my_stats_fp)
    hist = {}
    for hero in my_heroes:
        hist[hero] = hist.get(hero, 0) + 1
    sorted_by_freq = sorted(hist.items(), key=operator.itemgetter(1), reverse=True)
    top_five = sorted_by_freq[:5]

    durations = np.array(get_durations(my_matches_fp))
    aver_duration = np.round(np.mean(durations), 1)
    max_duration = np.round(max(durations), 1)
    min_duration = np.round(min(durations), 1)
    fb_times = np.array(get_fb_time(my_matches_fp))
    aver_fb_time = np.round(np.mean(fb_times), 1)

    aver_gpm = np.round(np.mean(np.array(get_gpm(my_stats_fp))), 1)
    aver_xpm = np.round(np.mean(np.array(get_xpm(my_stats_fp))), 1)
    aver_kda = np.round(np.mean(np.array(get_kda(my_stats_fp))), 1)

    win_rate = get_win_rate(my_matches_fp)

    print("Last 100 games summary:\n")
    print("win rate: " + str(win_rate) + "%")
    print("Five most playable heroes:")
    for hero, freq in top_five:
        print('\t' + str(hero) + ' ' + str(freq))
    print()
    print('average match duration: ' + str(aver_duration))
    print('the longest: ' + str(max_duration) + '; the shortest: ' + str(min_duration))
    print('average first blood time: ' + str(aver_fb_time))
    print('average GPM: ' + str(aver_gpm))
    print('average XPM: ' + str(aver_xpm))
    print('average KDA: ' + str(aver_kda))

    my_matches_fp.seek(0, 0)
    my_stats_fp.seek(0, 0)


def plot_most_played_heroes(heroes):
    """Plot most played heroes"""
    hist = {}
    for hero in heroes:
        hist[hero] = hist.get(hero, 0) + 1

    chart = pygal.HorizontalBar()
    chart.title = 'Most played heroes (at least 3 times)'
    for hero, times in hist.items():
        if times >= 3:
            chart.add(hero, times)

    chart.render_to_file('plots/most_played_heroes.svg')


def plot_durations(durations):
    plt.hist(durations, bins=20, facecolor='green')
    plt.xlabel('Durations')
    plt.ylabel('Count')
    plt.title('Durations of last 100 games')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # update_jsonl_files()
    my_stats_file = open("my_stats.jsonl", 'r')
    my_matches_file = open("my_matches_file.jsonl", 'r')
    print_summary(my_stats_file, my_matches_file)
