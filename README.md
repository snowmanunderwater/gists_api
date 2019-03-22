# gist_api: a CLI Github Gists API


Features
--------

* Just one file
* Python 3.6 support
* 0 dependencies, vanilla Python 3
* 7/14 GitHub API calls with parameters


API calls
---------

| API                               | Y\N | Implementation |
|-----------------------------------|-----|----------------|
| List a user's gists               | +   | list           |
| List all public gists             | +   | lp             |
| List starred gists                | +   | starred        |
| Get a single gist                 | +   | gist           |
| Get a specific revision of a gist | +/- | srg            |
| Create a gist                     | +   | create         |
| Edit a gist                       | +   | edit           |
| List gist commits                 | +   | lgc            |
| Star a gist                       | +   | star           |
| Unstar a gist                     | +   | unstar         |
| Check if a gist is starred        | -   |                |
| Fork a gist                       | -   |                |
| List gist forks                   | -   |                |
| Delete a gist                     | +   | delete         |


Installation
------------

It's just one file, common.

**BUT** to date, if you want use calls that required authentication, you must put your GitHub token in file called 'TOKEN'.

I am thinking of improvement.


Examples
--------

List all public gists. Page 1, per page 2.
``` bash
    $ gist_api lp -pg 1 -pp 2
    id:     0c2eaf12e4c50bb97f74afdfc5278001
    url:    https://gist.github.com/0c2eaf12e4c50bb97f74afdfc5278001
    desc:
    files:  ['Docker-CheatSheet.md']
    owner:  funkyremi
    ===================
    id:     ba57917f931db4da39a2209093717010
    url:    https://gist.github.com/ba57917f931db4da39a2209093717010
    desc:
    files:  ['.gitconfig']
    owner:  vloginov
```