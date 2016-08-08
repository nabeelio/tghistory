#
from setuptools import setup


requires = (
    'addict==0.4.0',
    'arrow==0.8.0',
    'html5lib==0.9999999',
    'jinja2==2.8',
    'pelican==3.6.3',
    'pytest==2.9.2',
    'pytg==0.4.10',
    'pyyaml==3.11',
    'requests==2.10.0',
    'typogrify==2.0.7',
)


setup(name='tghistory',
      author='Nabeel Shahzad',
      version='0.0.1',
      url='https://github.com/nabeelio/soccerbot',
      install_requires=requires,
      entry_points={
          'console_scripts': [
              'tghistory = tghistory.__init__:main',
          ]
      }
      )
