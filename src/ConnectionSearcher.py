#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path
import json
import sys
import glob
import plistlib
from workflow import Workflow3, ICON_WARNING, MATCH_SUBSTRING

def read_connections():

    configPath = os.environ["HOME"] + "/Library/Application Support/com.tinyapp.TablePlus/Data/Connections.plist"
    if not os.path.exists(configPath):
        configPath = os.environ["HOME"] + "/Library/Application Support/com.tinyapp.TablePlus-setapp/Data/Connections.plist"

    pl = plistlib.readPlist(configPath)
    connections = []
    i = 0
    while i < len(pl):
        connections.append({
                    'id': pl[i]['ID'],
                    'name': pl[i]['ConnectionName'],
                    'host': pl[i]['DatabaseHost']
                })
        i += 1
    return connections



def filter_key_for_connection(connection):
    return connection['name'] + ' ' + str(connection['id'])


def sort_key_for_connection(connection):
    return connection['name']

def main(wf):
    query = wf.args[0]
    connections = wf.cached_data('connections', read_connections, max_age=30)
    
    if query and connections:
        connections = wf.filter(query, connections, filter_key_for_connection, match_on=MATCH_SUBSTRING)
    
    connections.sort(key=sort_key_for_connection)
    for connection in connections:
        wf.add_item(title=connection['name'],
                    subtitle=connection['host'],
                    arg='tableplus://?id='+connection['id'],
                    valid=True)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
