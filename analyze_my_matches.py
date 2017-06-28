import json
import matplotlib.pyplot as plt
import numpy as np
import pygal
from matplotlib.ticker import FuncFormatter

from conf import my_id


def get_my_heroes(fp):
    """Get my heroes my statistics file"""
    for line in fp:
        my_stats = json.loads(line)
        yield my_stats['hero_name']


def get_durations(fp):
    """Get matches durations from matches file"""
    for line in fp:
        match = json.loads(line)
        # print(match.keys())
        yield int(np.round(match['duration'] / 60))


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


if __name__ == "__main__":
    my_stats_file = open("my_stats.jsonl", 'r')
    my_matches_file = open("my_matches_file.jsonl", 'r')

    my_heroes = get_my_heroes(my_stats_file)
    durations = list(get_durations(my_matches_file))

    durations = np.array(durations)

    # plot_most_played_heroes(my_heroes)

    print(np.mean(durations))

    chart = pygal.Bar()
    chart.add('Match durations', durations)
    chart.render_to_file('plots/match_durations.svg')

    # hist = np.histogram(durations, bins='auto')

    plt.hist(durations, bins=20, facecolor='green')
    plt.xlabel('Durations')
    plt.ylabel('Count')
    plt.title('Durations of last 100 games')
    plt.grid(True)
    plt.show()
