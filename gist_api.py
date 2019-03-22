#!/usr/bin/python3

import argparse
import json
import os.path
import urllib
import urllib.parse
import urllib.request

# TODO: think of what to do with TOKEN
with open('TOKEN', 'r') as f:
    TOKEN = f.read()

BASE_URL = 'https://api.github.com'


def str2bool(v):
    """
    Function to convert posible bool values to Python bools.
    """
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


# ====== Get a single gist ======
# https://developer.github.com/v3/gists/#get-a-single-gist
def getSingleGist(GIST_ID):
    """Print gist content to STDOUT.

    Args:
        GIST_ID (str): gist_id.

    Examples:
        >>> ./gist_api.py gist 0ba2b2a39f8f66caa5630542239f35a2
        VSCode: Open directory from integrated terminal.

        `code -r .`
    """

    # TODO: Add option selection

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

    print('gist_id: ', gist_id)
    print('gist_url: ', gist_url)
    print('gist_files: ', gist_files)
    print('gist_description: ', gist_description)
    print('gist_content: ', gist_content)
    print('===================')


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

    # TODO: Add option selection

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
        gist_description = item.get('description')
        comments = item.get('comments')

        print(f'=== {count} of {all_gists} ===')
        print(f'Name:        {name}')
        print(f'Description: {gist_description}')
        print(f'URL:         {html_url}')
        print(f'ID:          {gist_id}')
        print(f'Comments:    {comments}')
        count += 1


# ====== Create a gist ======
# https://developer.github.com/v3/gists/#create-a-gist
def createGist(files, desc, public):
    """Create gist.

    Args:
        files (list): files into gist
        desc (str): gist description
        public (bool): True for public, False for private

    Examples:
        >>> ./gist_api.py create -f file1 file2 -d 'Lalala' -b no
    """

    url = 'https://api.github.com/gists'

    files_dict = {}

    # FIXME: Possible problems in file parsing
    for file in files:
        filename = file.split('/')[-1]
        fileContent = open(file, 'r').read()
        files_dict[filename] = {'content': fileContent}

    json_dict = {
        'files': files_dict,
        'description': desc,
        'public': str2bool(public)
    }

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
    req = urllib.request.Request(
        url, data=post_data, headers=headers, method='POST')

    # send the request
    res = urllib.request.urlopen(req)

    if res.code == 201:
        print('Gist created!')


# ====== Edit a gist ======
# https://developer.github.com/v3/gists/#edit-a-gist
def editGist(id, desc, files):
    url = f'https://api.github.com/gists/{id}'

    files_dict = {}

    # FIXME: Possible problems in file parsing
    for file in files:
        filename = file.split('/')[-1]
        fileContent = open(file, 'r').read()
        files_dict[filename] = {'content': fileContent, 'filename': filename}

    json_dict = {
        'description': desc,
        'files': files_dict,
    }

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
    req = urllib.request.Request(
        url, data=post_data, headers=headers, method='PATCH')

    # send the request
    res = urllib.request.urlopen(req)

    if res.code == 200:
        print('Gist edited!')


# ====== Delete a gist ======
# https://developer.github.com/v3/gists/#delete-a-gist
def deleteGist(GIST_ID):
    url = f'{BASE_URL}/gists/{GIST_ID}'

    headers = {'Authorization': 'token ' + TOKEN}

    req = urllib.request.Request(url, headers=headers, method='DELETE')

    try:
        res = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print('ERROR: GIST_ID IS BAD')
        return

    if res.code == 204:
        print('Gist deleted!')


# ====== List all public gists ======
# https://developer.github.com/v3/gists/#list-all-public-gists
def listPublicGists(since, page, per_page):

    # TODO: Implement since
    # TODO: Add option selection

    r = urllib.request.urlopen(
        f'{BASE_URL}/gists/public?page={page}&per_page={per_page}').read()
    gists = json.loads(r.decode('utf-8'))

    for gist in gists:
        gist_id = gist.get('id')
        gist_url = gist.get('html_url')
        gist_description = gist.get('description')
        gist_files = list(gist.get('files'))
        gist_owner = gist.get('owner').get('login')
        gist_comments = gist.get('comments')

        print('id:    ', gist_id)
        print('url:   ', gist_url)
        print('desc:  ', gist_description)
        print('files: ', gist_files)
        print('owner: ', gist_owner)
        print('comments: ', gist_comments)
        print('===================')


# ====== List starred gists ======
# https://developer.github.com/v3/gists/#list-starred-gists
def listStarredGists(since):

    # TODO: Implement since
    # TODO: Add option selection

    url = f'{BASE_URL}/gists/starred'
    headers = {'Authorization': 'token ' + TOKEN}
    req = urllib.request.Request(url, headers=headers, method='GET')
    res = urllib.request.urlopen(req).read()

    gists = json.loads(res.decode('utf-8'))
    for gist in gists:
        gist_id = gist.get('id')
        gist_url = gist.get('html_url')
        gist_description = gist.get('description')
        gist_files = list(gist.get('files'))
        gist_comments = gist.get('comments')

        print('id:       ', gist_id)
        print('url:      ', gist_url)
        print('desc:     ', gist_description)
        print('files:    ', gist_files)
        print('comments: ', gist_comments)
        print('===================')


# ====== Get a specific revision of a gist ======
# https://developer.github.com/v3/gists/#get-a-specific-revision-of-a-gist
def specificRevisionOfAGist(GIST_ID, SHA):

    # FIXME: SHA don't work, at to date work like list gist

    try:
        r = urllib.request.urlopen(f'{BASE_URL}/gists/{GIST_ID}').read()
    except urllib.error.HTTPError:
        print('ERROR: GIST_ID OR SHA IS BAD')
        return

    cont = json.loads(r.decode('utf-8'))

    print(cont)


# ====== List gist commits ======
# https://developer.github.com/v3/gists/#list-gist-commits
def listGistCommits(GIST_ID):

    # TODO: Implement since
    # TODO: Add option selection

    url = f'{BASE_URL}/gists/{GIST_ID}/commits'
    req = urllib.request.Request(url, method='GET')

    try:
        res = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError:
        print('ERROR: GIST_ID IS BAD')
        return

    commits = json.loads(res.decode('utf-8'))
    for commit in commits:
        commit_url = commit.get('url')
        commit_version = commit.get('version')
        commit_user = commit.get('user').get('login')
        commit_change_deletions = commit.get('change_status').get('deletions')
        commit_change_additions = commit.get('change_status').get('additions')
        commit_change_total = commit.get('change_status').get('total')
        committed_at = commit.get('committed_at')

        print('commit_url              : ', commit_url)
        print('commit_version          : ', commit_version)
        print('commit_user             : ', commit_user)
        print('commit_change_deletions : ', commit_change_deletions)
        print('commit_change_additions : ', commit_change_additions)
        print('commit_change_total     : ', commit_change_total)
        print('committed_at            : ', committed_at)
        print('===================')


# ====== Star a gist ======
# https://developer.github.com/v3/gists/#star-a-gist
def starGist(GIST_ID):
    url = f'{BASE_URL}/gists/{GIST_ID}/star'
    headers = {'Authorization': 'token ' + TOKEN, 'Content-Length': 0}
    req = urllib.request.Request(url, headers=headers, method='PUT')

    try:
        res = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print('ERROR: GIST_ID IS BAD')
        return

    if res.code == 204:
        print('Starred!')


# ====== Unstar a gist ======
# https://developer.github.com/v3/gists/#unstar-a-gist
def unstarGist(GIST_ID):
    url = f'{BASE_URL}/gists/{GIST_ID}/star'
    headers = {
        'Authorization': 'token ' + TOKEN,
    }
    req = urllib.request.Request(url, headers=headers, method='DELETE')

    try:
        res = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print('ERROR: GIST_ID IS BAD')
        return

    if res.code == 204:
        print('Unstarred!')


# ====== Check if a gist is starred ======
# https://developer.github.com/v3/gists/#check-if-a-gist-is-starred
def checkGistStarred(GIST_ID):
    url = f'{BASE_URL}/gists/{GIST_ID}/star'
    headers = {
        # 'Content-Type': 'application/json',
        # 'Accept': 'application/json',
        'Content-Length': 0,
        'Authorization': 'token ' + TOKEN
    }
    req = urllib.request.Request(url, headers=headers, method='GET')

    # FIXME: this call return 404 if gist unstarred, if GIST_ID is bad it also return 404, !think about it
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print('Unstarred (or ID is bad, check it)')
        return
    else:
        print('Starred!')


# ====== Fork a gist ======
# https://developer.github.com/v3/gists/#fork-a-gist
def forkGist(GIST_ID):
    url = f'{BASE_URL}/gists/{GIST_ID}/forks'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'token ' + TOKEN
    }
    req = urllib.request.Request(url, headers=headers, method='POST')

    # FIXME: this call return 404 if gist unstarred, if GIST_ID is bad it also return 404, !think about it
    try:
        res = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print('Gist ID is BAD')
        return

    if res.code == 201:
        print('Gist forked')


# ====== List gist forks ======
# https://developer.github.com/v3/gists/#list-gist-forks
def listGistForks(GIST_ID):

    # TODO: page, per_page

    url = f'{BASE_URL}/gists/{GIST_ID}/forks'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'token ' + TOKEN
    }

    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        res = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError:
        print('Gist ID is BAD')
        return

    forks = json.loads(res.decode('utf-8'))
    for fork in forks:
        fork_user = fork.get('user').get('login')
        fork_url = fork.get('url')
        fork_id = fork.get('id')
        fork_created_at = fork.get('created_at')
        fork_updated_at = fork.get('updated_at')

        print('fork_user      : ', fork_user)
        print('fork_url       : ', fork_url)
        print('fork_id        : ', fork_id)
        print('fork_created_at: ', fork_created_at)
        print('fork_updated_at: ', fork_updated_at)
        print('===================')


if __name__ == '__main__':

    # TODO: refactor argparse

    parser = argparse.ArgumentParser(description='Github Gists CLI')
    parser.add_argument('name', type=str, help='Name of method')
    parser.add_argument('-id', '--gist_id', type=str, help='Gist ID')
    parser.add_argument('-u', '--username', type=str, help='Name of user')
    parser.add_argument('-f', '--files', nargs='*', help='Path to files')
    parser.add_argument(
        '-d',
        '--description',
        type=str,
        default='',
        help='A descriptive name for this gist.')
    parser.add_argument(
        '-p',
        '--public',
        type=str,
        default='yes',
        help='Gist status(public or private). Default is Public')
    parser.add_argument(
        '-s',
        '--since',
        type=str,
        help=
        'This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ. Only gists updated at or after this time are returned.'
    )
    parser.add_argument(
        '-pg', '--page', type=int, default='1', help='Paginator: page')
    parser.add_argument(
        '-pp', '--per_page', type=int, default='3', help='Paginator: per page')
    parser.add_argument(
        '-sha', '--sha', type=str, default='', help='SHA of gist commit')

    args = parser.parse_args()

    # ====== Get a single gist ======
    # https://developer.github.com/v3/gists/#get-a-single-gist
    if args.name == 'gist':
        getSingleGist(args.gist_id)

    # ====== List a user's gists ======
    # https://developer.github.com/v3/gists/#list-a-users-gists
    if args.name == 'list':
        getAllGists(args.username)

    # ====== Create a gist ======
    # https://developer.github.com/v3/gists/#create-a-gist
    if args.name == 'create':
        for file in args.files:
            if not os.path.isfile(file):
                raise Exception(f"{file} IS NOT A FILE")
        createGist(args.files, args.description, args.public)

    # ====== Edit a gist ======
    # https://developer.github.com/v3/gists/#edit-a-gist
    if args.name == 'edit':
        for file in args.files:
            if not os.path.isfile(file):
                raise Exception(f"{file} IS NOT A FILE")
        editGist(args.gist_id, args.description, args.files)

    # ====== Delete a gist ======
    # https://developer.github.com/v3/gists/#delete-a-gist
    if args.name == 'delete':
        deleteGist(args.gist_id)

    # ====== List all public gists ======
    # https://developer.github.com/v3/gists/#list-all-public-gists
    if args.name == 'lp':
        listPublicGists(args.since, args.page, args.per_page)

    # ====== List starred gists ======
    # https://developer.github.com/v3/gists/#list-starred-gists
    if args.name == 'starred':
        listStarredGists(args.since)

    # ====== Get a specific revision of a gist ======
    # https://developer.github.com/v3/gists/#get-a-specific-revision-of-a-gist
    if args.name == 'srg':
        specificRevisionOfAGist(args.gist_id, args.sha)

    # ====== List gist commits ======
    # https://developer.github.com/v3/gists/#list-gist-commits
    if args.name == 'lgc':
        listGistCommits(args.gist_id)

    # ====== Star a gist ======
    # https://developer.github.com/v3/gists/#star-a-gist
    if args.name == 'star':
        starGist(args.gist_id)

    # ====== Unstar a gist ======
    # https://developer.github.com/v3/gists/#unstar-a-gist
    if args.name == 'unstar':
        unstarGist(args.gist_id)

    # ====== Check if a gist is starred ======
    # https://developer.github.com/v3/gists/#check-if-a-gist-is-starred
    if args.name == 'check':
        checkGistStarred(args.gist_id)

    # ====== Fork a gist ======
    # https://developer.github.com/v3/gists/#fork-a-gist
    if args.name == 'fork':
        forkGist(args.gist_id)

    # ====== List gist forks ======
    # https://developer.github.com/v3/gists/#list-gist-forks
    if args.name == 'lgf':
        listGistCommits(args.gist_id)

    # FIXME: when create gist or star allready starred gist, this prints
    else:
        print(
            f"""gist_api: {args.name} is not a gist_api command. See 'gist_api --help'."""
        )
