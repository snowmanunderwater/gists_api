# gist_api: Github Gists CLI tool



Features
--------

* Single file
* 0 dependencies, vanilla Python 3


API calls
---------

| Command        | API                               | Arguments        |  Implement? |
|----------------|-----------------------------------|------------------|-------------|
| list           | List a specific user's gists      | -u               |  +          |
| lp             | List all public gists             | -s, -pp -pg      |  +          |
| starred        | List starred gists                | -s               |  +          |
| gist           | Get a single gist                 | -id              |  +          |
| srg            | Get a specific revision of a gist | -id, -sha        |  +/-        |
| create         | Create a gist                     | -f, -d, -p       |  +          |
| edit           | Edit a gist                       | -id, -f, -d      |  +/-        |
| lgc            | List gist commits                 | -id              |  +          |
| star           | Star a gist                       | -id              |  +          |
| unstar         | Unstar a gist                     | -id              |  +          |
| check          | Check if a gist is starred        | -id              |  +/-        |
| fork           | Fork a gist                       | -id              |  +          |
| lgf            | List gist forks                   | -id              |  +          |
| delete         | Delete a gist                     | -id              |  +          |


Installation
------------

It's just one file, common.

**BUT** to date, if you want to use calls that required authentication, you must put your GitHub token in file called 'TOKEN'.

I am thinking of improvement.


Examples
--------

- **List all gists of the specified user:**

```
$ python3 gist_api.py list -u snowmanunderwater

=== 1 of 5 ===
Name:        linux_tips.md
Description: Tips
URL:         https://gist.github.com/0ba2b2a39f8f66caa563054
9239f35a2
ID:          0ba2b2a39f8f66caa5630549239f35a2
Comments:    0
=== 2 of 5 ===
Name:        gistfile1.txt
Description: Find missing number in sequences
URL:         https://gist.github.com/923d6669c298f3ffa847b15fa621403b
ID:          923d6669c298f3ffa847b15fa621403b
Comments:    0
=== 3 of 5 ===
Name:        gistfile1.md
Description: Ubuntu 18.04 minimal + i3-gaps
URL:         https://gist.github.com/9674fd25e3174d3beb93c5ac85d23f96
ID:          9674fd25e3174d3beb93c5ac85d23f96
Comments:    0
```

- **Create gist:**

```
$ python3 gist_api.py create -f file1 -d "desc" -p yes

Gist created!
```


- **List public gists from all users:**

```
$ python3 gist_api.py lp -pp 3

=== 1 of 3 ===
id:     80904e1c20b1a5805ceff3f97bd7cbe8
url:    https://gist.github.com/80904e1c20b1a5805ceff3f97bd7cbe8
desc:
files:  ['flairdata_de.txt']
owner:  individual8
comments:  0
=== 2 of 3 ===
id:     ac06a4bd2f032b965f0b40812ebb42cd
url:    https://gist.github.com/ac06a4bd2f032b965f0b40812ebb42cd
desc:   wordpress docker_compose
files:  ['docker-compose.yml']
owner:  nc30
comments:  0
=== 3 of 3 ===
id:     06a04c1122ae1b607f1e6ed69161d254
url:    https://gist.github.com/06a04c1122ae1b607f1e6ed69161d254
desc:   combs
files:  ['combs.rb']
owner:  lbvf50mobile
comments:  0
```


Help
----

```
usage: gist_api [-h] [-id GIST_ID] [-u USERNAME] [-f [FILES [FILES ...]]]
                [-d DESCRIPTION] [-p PUBLIC] [-s SINCE] [-pg PAGE]
                [-pp PER_PAGE] [-sha SHA]
                name

Github Gists CLI

positional arguments:
  name                  Name of method

optional arguments:
  -h, --help            show this help message and exit
  -id GIST_ID, --gist_id GIST_ID
                        Gist ID
  -u USERNAME, --username USERNAME
                        Name of user
  -f [FILES [FILES ...]], --files [FILES [FILES ...]]
                        Path to files
  -d DESCRIPTION, --description DESCRIPTION
                        A descriptive name for this gist.
  -p PUBLIC, --public PUBLIC
                        Gist status(public or private). Default is Public
  -s SINCE, --since SINCE
                        This is a timestamp in ISO 8601 format: YYYY-MM-
                        DDTHH:MM:SSZ. Only gists updated at or after this time
                        are returned.
  -pg PAGE, --page PAGE
                        Paginator: page
  -pp PER_PAGE, --per_page PER_PAGE
                        Paginator: per page
  -sha SHA, --sha SHA   SHA of gist commit
```