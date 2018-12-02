# -*- coding: utf-8 -*-
"""Convert the Yelp Dataset Challenge dataset from json format to csv.
For more information on the Yelp Dataset Challenge please visit http://yelp.com/dataset_challenge
"""
import argparse
import collections
import csv
import simplejson as json
import unicodedata


columns_filter = ["business_id", "categories"]
categories = []

def read_and_write_file(json_file_path, csv_file_path, column_names):
    """Read in the json dataset file and write it out to a csv file, given the column names."""
    with open(csv_file_path, 'wb+') as fout:
        csv_file = csv.writer(fout)
        csv_file.writerow(list(column_names))
        with open(json_file_path) as fin:
            for line in fin:
                line_contents = json.loads(line)
                csv_file.writerow( get_row(line_contents, column_names) )

def set_categories(json_file_path, csv_file_path):
    """Read in the json dataset file and write it out to a csv file, given the column names."""
    
    with open(json_file_path) as fin:
        for line in fin:
            line_contents = json.loads(line)
            get_row(line_contents, columns_filter)
    
    cat = list(set(categories))
    columns = ['business_id'] + cat
    print(len(cat))

    i = 0
    for c in cat:
        print( str(i) + " - " + c)
        i += 1

    with open(csv_file_path, 'wb+') as fout:
        csv_file = csv.writer(fout)
        csv_file.writerow(columns)
        with open(json_file_path) as fin:
            for line in fin:
                line_contents = json.loads(line)
                csv_file.writerow( god_is_more_qntc(line_contents, cat) )


def get_superset_of_column_names_from_file(json_file_path):
    """Read in the json dataset file and return the superset of column names."""
    column_names = set()
    with open(json_file_path) as fin:
        for line in fin:
            line_contents = json.loads(line)
            column_names.update(
                    set(get_column_names(line_contents).keys())
                    )
    return column_names

def get_column_names(line_contents, parent_key=''):
    """Return a list of flattened key names given a dict.
    Example:
        line_contents = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        will return: ['a.b', 'a.c']
    These will be the column names for the eventual csv file.
    """
    column_names = []
    for k, v in line_contents.iteritems():
        column_name = "{0}.{1}".format(parent_key, k) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            column_names.extend(
                    get_column_names(v, column_name).items()
                    )
        else:
            column_names.append((column_name, v))
    return dict(column_names)

def get_nested_value(d, key):
    """Return a dictionary item given a dictionary `d` and a flattened key from `get_column_names`.
    
    Example:
        d = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        key = 'a.b'
        will return: 2
    
    """
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    return get_nested_value(sub_dict, sub_key)

def get_row(line_contents, column_names):
    """Return a csv compatible row given column names and a dict."""
    row = []
    for column_name in column_names:
        # categories += s.split(',')
        line_value = get_nested_value(
                        line_contents,
                        column_name,
                        )
        if line_value:
            if(column_name == 'categories'):
                categories.extend( line_value.split(',') )

        if isinstance(line_value, unicode):
            row.append('{0}'.format(line_value.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row

def god_is_more_qntc(line_contents, cats):
    """Return a csv compatible row given column names and a dict."""
    row = []

    bus_id = get_nested_value(
                    line_contents,
                    'business_id',
                    )

    bus_cats = get_nested_value(
                    line_contents,
                    'categories',
                    )

    line_value = ''
    line_value = line_value + bus_id + ", "

    if isinstance(bus_id, unicode):
        row.append('{0}'.format(bus_id.encode('utf-8')))
    elif line_value is not None:
        row.append('{0}'.format(bus_id))
    else:
        row.append('')
    
    # string = unicodedata.normalize('NFKD', line_value).encode('ascii','ignore')

    # print(line_value)
    # print(string)

    business_cat = []
    if bus_cats:
        business_cat = bus_cats.split(',')
    else:
        print("category not found")

    for great_category in cats:
        v = "0"
        for cat in business_cat:
            if great_category == cat:
                v = "1"
        if isinstance(v, unicode):
            row.append('{0}'.format(v.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(v))
        else:
            row.append('')

    return row

if __name__ == '__main__':
    """Convert a yelp dataset file from json to csv."""

    parser = argparse.ArgumentParser(
            description='Convert Yelp Dataset Challenge data from JSON format to CSV.',
            )

    parser.add_argument(
            'json_file',
            type=str,
            help='The json file to convert.',
            )

    args = parser.parse_args()

    json_file = args.json_file
    csv_file = '{0}.csv'.format(json_file.split('.json')[0])

    set_categories(json_file, csv_file)
