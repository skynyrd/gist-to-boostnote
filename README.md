# gist-to-boostnote

Script to create [Boostnote](https://github.com/BoostIO/Boostnote)s from anyone's public gists.

### Description

Although [Gist Service](https://gist.github.com) is a great cloud platform for your notes/snippets, you can't organize them properly as it doesn't have such required features like smart search and tagging. I switched from Gist to Boostnote, which promotes these features by default. However, I didn't want to copy and paste all the gists, chose writing a small script for those who have similar considerations instead.

### Requirements

* Python > 3.5
* MacOS or Linux

### Usage

1. Backup your `Boostnote` folder just in case. (containing `notes` and `boostnote.js`)
1. Create a folder in BoostNote app, script will create notes into it.
1. Clone the repo
1. `cd gist-to-boostnote`
1. `pip3 install -r requirements.txt`
1. `export PYTHONPATH=./`
1. python3 src/gist-to-boostnote.py /YOUR/BOOSTNOTE/FOLDER/PATH GITHUB_USER_NAME BOOSTNOTE_FOLDER_NAME
    1. e.g. `python3 src/gist-to-boostnote.py /Users/skynyrd/Boostnote skynyrd GistFolder`

### Missing stuff

* Tests
* Docker support
