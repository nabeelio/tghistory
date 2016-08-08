#

AUTHOR = ''
SITENAME = 'telegram logs'
SITEURL = 'index.html'

# options are taken/set from there as well
THEME = '../pelican-themes/Flex'
CUSTOM_CSS = 'main.css'

PATH = 'tmp/'

# general settings
MAIN_MENU = False
TYPOGRIFY = True
TIMEZONE = 'US/Central'
USE_FOLDER_AS_CATEGORY = True
DELETE_OUTPUT_DIRECTORY = True

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True

FORMATTED_FIELDS = [
    'summary'
]

STATIC_PATHS = [
    'static/'  # relative to tmp/
]

LINKS = [
    ('users', 'categories.html')
]

# default theme: https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3
# this theme allows you to chose a sub-theme
# http://bootswatch.com
# THEME = '../pelican-themes/pelican-bootstrap3'
# BOOTSTRAP_THEME = 'flatly'

# use the fluid layout
# BOOTSTRAP_FLUID = True
# SHOW_ARTICLE_AUTHOR = False
# SHOW_ARTICLE_CATEGORY = False

