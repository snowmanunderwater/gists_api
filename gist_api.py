#!/usr/bin/python3

import argparse
import http.client
import json
import re
import shlex
import subprocess
import sys
import urllib
import urllib.parse
import urllib.request
import os.path

with open('TOKEN', 'r') as t:
    TOKEN = t.read()

BASE_URL = 'https://api.github.com'
GIST_URL = 'https://gist.github.com'


# ====== Get a single gist ======
# https://developer.github.com/v3/gists/#get-a-single-gist
def getSingleGist(GIST_ID):
    """Print gist content to STDOUT.

    Args:
        GIST_ID (str): gist_id.

    Examples:
        >>> ./gist_api.py gist 0ba2b2a39f8f66caa5630549239f35a2
        VSCode: Open directory from integrated terminal.

        `code -r .`
    """
    try:
        r = urllib.request.urlopen(f'{BASE_URL}/gists/{GIST_ID}').read()
    except urllib.error.HTTPError:
        print('ERROR: GIST_ID IS BAD')
        return

    cont = json.loads(r.decode('utf-8'))

    gist_id = cont.get('id')
    gist_url = cont.get('html_url')
    gist_files = list(cont.get('files'))
    gist_description = cont.get('description')
    gist_content = list(cont.get('files').values())[0].get('content')

    print(gist_content)


# ====== List a user's gists ======
# https://developer.github.com/v3/gists/#list-a-users-gists
def getAllGists(USERNAME):
    """Print gists information of given user.

    Args:
        USERNAME (str): owner of gists.

    Examples:
        >>> ./gist_api.py list snowmanunderwater
        === 1 of 5 ===
        Name:        Tips.md
        Description: Tips
        URL:         https://gist.github.com/0ba2b2a39f8f66caa5630549239f35a2
        ID:          0ba2b2a39f8f66caa5630549239f35a2
    """
    try:
        r = urllib.request.urlopen(f'{BASE_URL}/users/{USERNAME}/gists').read()
    except urllib.error.HTTPError:
        print('ERROR: USERNAME IS BAD')
        return

    cont = json.loads(r.decode('utf-8'))
    all_gists = len(cont)
    count = 1
    for item in cont:
        name = list(item.get('files').keys())[0]
        gist_id = item.get('id')
        html_url = item.get('html_url')
        raw_url = item.get('files').get(name).get('raw_url')
        gist_description = item.get('description')
        print(f'=== {count} of {all_gists} ===')
        print(
            f'Name:        {name}\nDescription: {gist_description}\nURL:         {html_url}\nID:          {gist_id}'
        )
        count += 1


# ====== Create a gist ======
# https://developer.github.com/v3/gists/#create-a-gist
def createGists(files):
    """Create gist.

    Args:
        files (list): files into gist

    Examples:
        >>> ./gist_api.py create file1
        
    """

    url = 'https://api.github.com/gists'

    files_dict = {}

    for file in files:
        filename = file
        fileContent = open(file, 'r')

        files_dict[filename] = {'content': fileContent.read()}

    json_dict = {'files': files_dict, 'description': 'test', 'public': True}

    # convert json_dict to JSON
    json_data = json.dumps(json_dict)

    # convert str to bytes (ensure encoding is OK)
    post_data = json_data.encode('utf-8')


    # we should also say the JSON content type header
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'token ' + TOKEN
    }

    # now do the request for a url
    req = urllib.request.Request(url, post_data, headers, method='POST')

    # send the request
    res = urllib.request.urlopen(req)
    if res.code == 201:
        print('Gist created!')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('ARG', nargs='*')  # *args
    namespace = parser.parse_args(sys.argv[1:])


    # ====== Get a single gist ======
    # https://developer.github.com/v3/gists/#get-a-single-gist
    if namespace.name == 'gist':
        # namespace.ARG[0] <-- take only one argument
        getSingleGist(namespace.ARG[0])

    # ====== List a user's gists ======
    # https://developer.github.com/v3/gists/#list-a-users-gists
    if namespace.name == 'list':
        # namespace.ARG[0] <-- take only one argument
        getAllGists(namespace.ARG[0])

    # ====== Create a gist ======
    # https://developer.github.com/v3/gists/#create-a-gist
    if namespace.name == 'create':
        # namespace.ARG <-- take all arguments
        # *args - files

        for file in namespace.ARG:
            if not os.path.isfile(file):
                raise Exception(f"{file} IT'S NOT FILE")

        createGists(namespace.ARG)
