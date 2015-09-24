TidyIt Scheduler Script
========================
TidyIt is a script designed to tidy up your video library; house cleaning
one could say. It takes care of directories that once held video content
but now is just either empty, or contains old meta data.

This script is especially useful if you use a third party application such as
Plex or KODI (XBMC) to manage your video library. Most third party applications
that let remove a video from your library will _only_ remove the video itself.
It will not however remove all the content that surrounds it.

Since the primary focus of this script is to remove content from your media
library, I will not be held responsible for any irrecoverable data loss you
experience.  I can confirm the tool works for me, but that doesn't mean it
will work for you. The good news is that the script is filled with safe guards!
Thus you'd have to stray far from the default settings to damage your library.

The script intentionally operates in a _log only_ mode by default unless you 
explicitly specify it to run differently.  I encourage you to run the script
in this _log only_ mode first anyway;  get an idea as to what it wants to do
and the files it wants to handl. If your happy with it's decisions, you can
flip a switch and the script will begin tidying up your library as promised
to you.

The script operates in 3 modes:
* __Preview Only__: This is the default option. It runs the script and just reports to the screen what it would have otherwise done.  It doesn't actually do anthing at all to your library though.  Sometimes this is all you need so that you can handle it's output your own way.  Alternatively this is a great method to run in until you get the options the way you like them.
* __Delete__: This performs the same check the Preview does however anything flagged to be handled is removed.
* __Move__: Similar to __Delete__ however this mode just moves content that should have otherwise been removed into another directory (that you specify).  This allows you to review what is considered junk and decide for yourself if it should be removed.  This method also requires you to be responsible for managing the directory you move content to.

This script was intended to be an [NZBGet](http://nzbget.net) and _Scheduling_
script wrapper for _NZBGet_. However, it also works perfectly well as a
standalone script for others too!


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
| pynzbget                     | 0.2.3   | https://pypi.python.org/pypi/pynzbget/0.2.3                                          |

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
  -s ENTRIES, --safe-entries=ENTRIES
                        If a safe-entry file/dir is located within a path
                        scanned then the path is ignored. Use safe-entry files
                        (or dirs) to intentionally ignore directories of your
                        choice that reside in your video library. You can
                        specify more then one safe-entry by separating them
                        with a comma (,). The default value(s) are
                        '.tidysafe'.
  -t ENTRIES, --always-trash=ENTRIES
                        Identify any file extensions you wish to always trash
                        if matched. By default this is not set.You can specify
                        more then one trash entry by separating each of them
                        with a comma (,).
  -M ENTRIES, --meta-content=ENTRIES
                        Identify any files and/or directories that should be
                        treated as meta content. Meta content is only handled
                        if it's the last thing within a media directory.You
                        can specify more then one meta entry by separating
                        each of them with a comma (,).  By Default the
                        following are already defined: 'Thumbs.db', '@eaDir',
                        '.DS_Store', '.AppleDouble', '__MACOSX'.
  -m SIZE_IN_MB, --video-minsize=SIZE_IN_MB
                        Specify the minimum size a video must be before it's
                        treated as part of your collection. This value is used
                        to diffentiate between video file and samples files.
                        This value is interpreted in MB (Megabytes) and
                        defaults to 150 MB.
  -a AGE_IN_SEC, --min-age=AGE_IN_SEC
                        Specify the minimum age a directory and/or file must
                        be before considering it for processing. This value is
                        interpreted in seconds and defaults to 3600 sec(s).
  -c, --clean           Unless this switch is specified, this script only runs
                        in a log only mode (a dry-run) allowing you to see the
                        actions the script would have otherwise performed.
                        This switch can be combined with the --move-path (-p)
                        switch to move handled instead.
  -p PATH, --move-path=PATH
                        Identifiy the path to place content into instead of
                        removing it.  By specifying a --move-path, the --clean
                        (-c) switch is implied however handled content is
                        moved instead of being removed.
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
python TidyIt.py /usr/share/TVShows /usr/share/Movies
```

If you don't want your content to be removed; you can just have handled content moved
to another directory for your review later on. All directory paths are preserved so it won't
take any rocket science to figure out where removed content came from. It's a little bit of
a more save mode then the --clean (-c) switch.
```bash
# Scan a your librarys and move any content to be handled to the
# TidyIt.Trash in your hoe directory (~ is supported)
python TidyIt.py -m ~/TidyIt.Trash /usr/share/TVShows
```

If the script behaves as you expect it, you can schedule it as a cron
to frequently clean your libraries every day with a command such as:
```bash
# $> crontab -e
0 0 * * * /path/to/TidyIt.py -c /usr/share/TVShows /usr/share/Movies
```
