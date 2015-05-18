TidyIt Scheduler Script
========================
Point TidyIt to your video library and the script then looks after eliminating
any empty directories. It also eliminates directories that simply no longer
host video files. This script is especially useful when you use a third party
application such as Plex or KODI (XBMC) to manage your library. Most third
party applications that you tell to remove a video from your library leaves
the directory that contained it and any meta information as well.  This script
simply automatically cleans this up for you.

Since this script has one primary function (to delete lingering content), it
was intended to be pointed at a video library.  I will not be held responsible
for any irrecoverable data loss you experience through the use of this script.
The script intentionally operates in a  _log only_ mode with no parameters
other then the directory(ies) to scan.  I encourage you to run the script
as such and monitor what it itends to remove.  If your satisfied with the
results, then rerun the script using its clean mode.

This script was intended to be an [NZBGet](http://nzbget.net) and _scheduling_
script wrapper for _TidyIt_. However, it also works perfectly fine as a
standalone script for others too.


Installation Instructions
=========================
1. Ensure you have at least Python v2.6 or higher installed onto your system.
2. Simply place the __TidyIt.py__ and __TidyIt__ directory together.
   * __NZBGet users__: you will want to place these inside of your _nzbget/scripts_ directory. Please ensure you are running _(at least)_ NZBGet v11.0 or higher. You can acquire the latest version of of it from [here](http://nzbget.net/download).

The Non-NZBGet users can also use this script via a cron (or simply call it
from the command line) to automatically poll directories for the latest
subtitles for the video content within it. See the __Command Line__ section
below for more instructions on how to do this.

**Note:** The _TidyIt_ directory provides all of the nessisary dependencies
in order for this script to work correctly. The directory is only required
if you do not have the packages already available to your global
environment. These dependant packages are all identified under the
_Dependencies_ section below.

Dependencies
============
The following dependencies are already provided for you within the
_TidyIt_ directory and no further effort is required by you. However, it
should be known that TidyIt.py depends on the following packages:

| Name                         | Version | Source                                                                               |
| ---------------------------- |:------- |:------------------------------------------------------------------------------------ |
| pynzbget                     | 0.2.2   | https://pypi.python.org/pypi/pynzbget/0.2.2                                          |

Command Line
============
TidyIt.py has a built in command line interface that can be easily tied
to a cron entry or can be easilly called from the command line to automate
the fetching of subtitles.

Here are the switches available to you:
```
Usage: TidyIt.py [options] [scandir1 [scandir2 [...]]]

Options:
  -h, --help            show this help message and exit
  -n ENCODING, --encoding=ENCODING
                        The system encoding to use (utf-8, ISO-8859-1, etc).
                        The default value is 'UTF-8'.
  -m SIZE_IN_MB, --video-minsize=SIZE_IN_MB
                        Specify the minimum size a video must be before it's
                        treated as part of your collection. This value is used
                        to diffentiate between video file and samples files.
                        This value is interpreted in MB (Megabytes) and
                        defaults to 150 MB.
  -c, --clean           Unless this switch is specified, this script only runs
                        in a log only mode (a dry-run) allowing you to see the
                        actions the script would have otherwise performed.
  -L FILE, --logfile=FILE
                        Send output to the specified logfile instead of
                        stdout.
  -D, --debug           Debug Mode
```

Here is simple example:
```bash
# Scan a your library (print only mode)
python TidyIt.py /usr/share/TVShows
# Happy with the results?  Okay then run the script with the --clean (-c) switch:

python TidyIt.py -c /usr/share/TVShows
```

You can scan multiple directories with the following command:
```bash
# Scan a your librarys (print only mode)
python TidyIt.py /usr/share/TVShows, /usr/share/Movies
```

If the script behaves as you expect it, you can schedule it as a cron
to frequently clean your libraries every day with a command such as:
```bash
# $> crontab -e
0 0 * * * /path/to/TidyIt.py -c /usr/share/TVShows, /usr/share/Movies
```