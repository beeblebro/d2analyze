import operator
import json
import matplotlib.pyplot as plt
import numpy as np
import pygal


def get_my_heroes(fp):
    """Get my heroes my statistics file"""
    for line in fp:
        my_stats = json.loads(line)
        yield my_stats['hero_name']


def get_durations(fp):
    """Get matches durations [min] from matches file"""
    durs = []
    for line in fp:
        match = json.loads(line)
        durs.append(match['duration'] / 60)
    fp.seek(0, 0)
    return durs


def get_fb_time(fp):
    """Get first blood times [min]"""
    fb_t = []
    for line in fp:
        match = json.loads(line)
        fb_t.append(match['first_blood_time'] / 60)
    fp.seek(0, 0)
    return fb_t


def print_summary(my_stats_file, my_matches_file):
    my_heroes = get_my_heroes(my_stats_file)
    hist = {}
    for hero in my_heroes:
        hist[hero] = hist.get(hero, 0) + 1
    sorted_by_freq = sorted(hist.items(), key=operator.itemgetter(1), reverse=True)
    top_five = sorted_by_freq[:5]

    durations = np.array(list(get_durations(my_matches_file)))
    aver_duration = round(np.mean(durations))
    max_duration = round(max(durations))
    min_duration = round(min(durations))
    fb_times = np.array(get_fb_time(my_matches_file))
    aver_fb_time = round(np.mean(fb_times))

    print("Last 100 games summary:\n")
    print("Five most playable heroes:")
    for hero, freq in top_five:
        print('\t' + str(hero) + ' ' + str(freq))
    print()
    print('average match duration: ' + str(aver_duration))
    print('the longest: ' + str(max_duration) + '; the shortest: ' + str(min_duration))
    print('average first blood time: ' + str(aver_fb_time))


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
    my_stats_file = open("my_stats.jsonl", 'r')
    my_matches_file = open("my_matches_file.jsonl", 'r')
    print_summary(my_stats_file, my_matches_file)
