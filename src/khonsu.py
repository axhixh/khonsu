#!/usr/bin/env python

import csv
from collections import defaultdict

def load_places(filename):
    loc_map = {}
    with open(filename, 'rb') as csvfile:
        placereader = csv.reader(csvfile)
        placereader.next()
        for row in placereader:
            duration = int(row[4])
            location = (float(row[5]), float(row[6])) #lat,long
            total_duration = loc_map.get(location, 0) + duration
            loc_map[location] = total_duration
        return loc_map

def calc_intensity(locations):
    """ Calculate intensity per location"""
    max_duration = float(max(locations.values()))
    result = {}
    for key, value in locations.items():
        result[key] = value/max_duration
    return result

def histogram_equalization(locations):
    """ equalize the location intensity so the heatmap is spread out"""
    histo = histogram(locations.values())
    equalized = {}
    for key, value in locations.items():
        equalized[key] = histo[value]
    return equalized

def histogram(values):
    """ cumulative histogram of the values """
    histo = defaultdict(int)
    for x in values:
        histo[x] += 1
    keys = histo.keys()
    keys.sort()
    result = {}
    current_total = 0
    for key in keys:
        result[key] = histo[key] + current_total
        current_total = result[key]
    total = float(result[keys[-1]])
    # scale histogram 0 - 1
    for key, value in result.items():
        result[key] = value / total
    return result

def save_places(locations, filename):
    entries = []
    for key, value in locations.items():
        entries.append("[%.6f, %.6f, %.8f]" % (key[0], key[1], value))
    with open(filename, 'w') as out:
        out.write("var locations = [")
        out.write(",\n".join(entries))
        out.write("];")

def main():
    print 'Loading places data'
    locations = load_places('../data/places_2014.csv')
    print 'Calculating heat map'
    intensity_map = histogram_equalization(calc_intensity(locations))
    print 'Saving places'
    save_places(intensity_map, '../public/places.js')
    print 'Done'


if __name__ == '__main__':
    main()
