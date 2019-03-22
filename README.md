# gist_api: a CLI Github Gists API


Features
--------

* Just one file
* Python 3.6 support
* 0 dependencies, vanilla Python 3


API calls
---------

| API                               | Implement? | Command        |
|-----------------------------------|------------|----------------|
| List a user's gists               | +          | list           |
| List all public gists             | +          | lp             |
| List starred gists                | +          | starred        |
| Get a single gist                 | +          | gist           |
| Get a specific revision of a gist | +/-        | srg            |
| Create a gist                     | +          | create         |
| Edit a gist                       | +          | edit           |
| List gist commits                 | +          | lgc            |
| Star a gist                       | +          | star           |
| Unstar a gist                     | +          | unstar         |
| Check if a gist is starred        | +/-        | check          |
| Fork a gist                       | +          | fork           |
| List gist forks                   | +/-        | lgf            |
| Delete a gist                     | +          | delete         |


Installation
------------

It's just one file, common.

**BUT** to date, if you want use calls that required authentication, you must put your GitHub token in file called 'TOKEN'.

I am thinking of improvement.


Examples
--------

* List all public gists.

![list](https://github.com/snowmanunderwater/gists_api/blob/master/screenshots/list.png)

* Create gist.

![create](https://github.com/snowmanunderwater/gists_api/blob/master/screenshots/create.png)

* List public gists.

![list](https://github.com/snowmanunderwater/gists_api/blob/master/screenshots/list_public.png)




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