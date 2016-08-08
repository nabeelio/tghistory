# telegram history exporter

generates a static, per-user static site of your telegram chat history.
uses pelican to generate the site itself.

## install

```
git clone --recursive git@github.com:nabeelio/tghistory.git tghistory
git clone --recursive https://github.com/getpelican/pelican-themes
cd tghistory
make install
```

next edit:
* config.yml - point to the correct paths for pelican, and the telegram-cli
* pelicanconf.py - any custom pelican confs, like themes


## run

```
./generate.sh  # OR
env/bin/python tghistory.py [--contact <username>]
```

## innards

* telegram-cli is used to find contact
* read the history of each contact
* generate the rst file(s), per-day, in a sub-folder for a client
* run pelican, calling it on that temp directory, into the output folder
* ???
* don't profit off of this
