# telegram history exporter

generates a static, searchable, per-user static site of your telegram chat history


## install

```
git clone --recursive git@github.com:nabeelio/tghistory.git tghistory
cd tghistory
make install
cd ..
git clone https://github.com/getpelican/pelican-themes
```

next edit:
* config.yml - point to the correct paths for pelican, and the telegram-cli
* pelicanconf.py - any custom pelican confs, like themes


## run

```
env/bin/python tghistory.py [--contact <username>]
```
