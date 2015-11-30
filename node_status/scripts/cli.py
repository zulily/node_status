# Copyright (C) 2015 zulily, llc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""node_status
knife status-like, but significantly faster with various output
formats.  Uses partial search.
"""
from __future__ import print_function

import argparse
import chef
import datetime
import time
import sys

from termcolor import colored

# Node attributes used for partial search
SEARCH_ATTRIBUTES = {'name': ['name'],
                     'ohai_time': ['ohai_time'],
                     'platform':  ['platform'],
                     'platform_version':  ['platform_version'],
                     'fqdn': ['fqdn'],
                     'ipaddress': ['ipaddress'],
                     'chef_client_version': ['chef_packages', 'chef',
                                             'version'],
                     'ruby_version': ['languages', 'ruby', 'version'],}

# Default number of minutes back for the last successful
# chef client run window, for the node to be considered healthy
HEALTHY_MINUTES = 120


def main():
    """
    Do some stuff.
    """
    arguments = parse_arguments().parse_args()
    name_filters = ['*'] if not arguments.name_filters else \
                   arguments.name_filters
    api = chef.autoconfigure()
    response = nodes_status(api, name_filters,
                            healthy_only=arguments.healthy_only,
                            healthy_minutes=arguments.healthy_minutes)
    if arguments.output_format == 'knife_status':
        print_status(response, arguments.sort,
                     healthy_minutes=arguments.healthy_minutes)
    elif arguments.output_format == 'fqdn_list':
        print_fqdn_list(response, arguments.sort)
    elif arguments.output_format == 'version_list':
        print_version_list(response, arguments.sort)


def print_version_list(response, sort):
    """Output a list of FQDN + chef client version

    Given the response from the chef server following a partial search, output
    a simple list of FQDNs + the chef client version.
    """
    reverse_sort = True if sort == 'asc' else False
    sort_attribute = 'ohai_time'

    if sort == 'fqdn':
        sort_attribute = 'fqdn'
    elif sort == 'chef_client_version':
        sort_attribute = 'chef_client_version'
    elif sort == 'ruby_version':
        sort_attribute = 'ruby_version'

    for node in sorted(response['rows'], key=lambda node: \
                       node['data'][sort_attribute], reverse=reverse_sort):
        print("{0} {1} {2}".format(node['data']['fqdn'], \
                                   node['data']['chef_client_version'],
                                   node['data']['ruby_version']))


def print_fqdn_list(response, sort):
    """Output a list of FQDNs

    Given the response from the chef server following a partial search, output
    a simple list of FQDNs.
    """
    reverse_sort = True if sort == 'asc' else False
    sort_attribute = 'fqdn' if sort == 'fqdn' else 'ohai_time'

    for node in sorted(response['rows'], key=lambda node: \
                       node['data'][sort_attribute], reverse=reverse_sort):
        print("{0}".format(node['data']['fqdn']))


def print_status(response, sort, healthy_minutes):
    """Output results just like 'knife status' would

    Given the response from the chef server following a partial search, output
    similar to the knife status command.
    """
    reverse_sort = True if sort == 'asc' else False
    sort_attribute = 'fqdn' if sort == 'fqdn' else 'ohai_time'
    now = int(time.time())
    for node in sorted(response['rows'], key=lambda node: \
                       node['data'][sort_attribute], reverse=reverse_sort):
        try:
            time_diff = now - int(node['data']['ohai_time'])
        except:
            # For some reason, we have seen a few nodes of type None,
            # skipping these
            continue
        hours = int(time_diff / 60 / 60)
        minutes = int(time_diff / 60)
        is_healthy = True if healthy_minutes >= minutes else False
        last_run = datetime.timedelta(seconds=time_diff)
        if last_run.days > 1:
            last_run_formatted = '{0} days ago'.format(last_run.days)
        elif last_run.days == 1:
            last_run_formatted = '1 day ago'
        elif hours > 1:
            last_run_formatted = '{0} hours ago'.format(hours)
        elif hours == 1:
            last_run_formatted = '1 hour ago'
        elif minutes != 1:
            last_run_formatted = '{0} minutes ago'.format(minutes)
        elif minutes == 1:
            last_run_formatted = '1 minute ago'
        else:
            last_run_formatted = 'unknown'

        last_run_formatted = colored(last_run_formatted, 'green') if \
                             is_healthy else \
                             colored(last_run_formatted, 'yellow')
        print("{0}, {1}, {2}, {3}, {4} {5}.".\
              format(last_run_formatted,
                     node['data']['name'], node['data']['fqdn'],
                     node['data']['ipaddress'], node['data']['platform'],
                     node['data']['platform_version']))


def nodes_status(api, name_filters, healthy_only, healthy_minutes):
    """Perform the search to determine status of matching nodes

    Perform a partial search against the chef server, limited to any name
    filters.  If healthy_only is True, only return nodes updated in last
    healthy_minutes minutes.
    """
    query = 'name:{0}'.format('+OR+name:'.join(name_filters))
    response = api.api_request('POST', '/search/node?q={0}'.format(query),
                               data=SEARCH_ATTRIBUTES)

    if healthy_only:
        rows = list()
        for node in response['rows']:
            try:
                if int(time.time()) - int(node['data']['ohai_time']) <= \
                healthy_minutes * 60:
                    rows.append(node)
            except:
                # For some reason, we have seen a few nodes of type None,
                # skipping these
                continue
        response['rows'] = rows

    return response


def parse_arguments():
    """Collect command-line arguments."""
    parser = argparse.ArgumentParser(prog='node_status',
                                     description="A 'knife status' " + \
                                     "alternative.")
    parser.add_argument('--name-filter', '-F', action='append',
                        dest='name_filters', metavar='CHEF_SEARCH_FILTER',
                        help='A node name search filter, with * and ? ' + \
                        'allowed, defaulting to *.  For example, ' + \
                        '*dev* or *pr?d*.  Can be used multiple times ' + \
                        'with results being cumulative')
    parser.add_argument('--healthy-only', '-H', action='store_true',
                        dest='healthy_only', default=False,
                        help='Only report on "healthy" nodes, with ' + \
                        'client runs completed in < "healthy minutes"')
    parser.add_argument('--healthy-minutes', '-m', action='store',
                        dest='healthy_minutes', default=HEALTHY_MINUTES,
                        type=int,
                        help='Set the number of minutes back for the last ' + \
                        'successful chef run, for a node to be considered ' + \
                        'healthy. Defaults to {0} minutes'.\
                        format(HEALTHY_MINUTES))
    parser.add_argument('--output-format', '-f',
                        choices=['knife_status', 'fqdn_list', 'version_list'],
                        dest='output_format', default='knife_status',
                        help='Output format to display.  Defaults to ' + \
                        'knife_status')
    parser.add_argument('--sort', '-S', choices=['asc', 'desc', 'fqdn',
                                                 'chef_client_version',
                                                 'ruby_version'],
                        dest='sort', default='desc',
                        help='Last client run sort order.  Defaults to desc')

    return parser


if __name__ == '__main__':
    sys.exit(main())
