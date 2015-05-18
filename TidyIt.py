#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# TidyIt post-processing script for NZBGet
#
# Copyright (C) 2015 Chris Caron <lead2gold@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with subliminal.  If not, see <http://www.gnu.org/licenses/>.
#


##############################################################################
### NZBGET SCHEDULER SCRIPT                                                ###

# Tidy It.
#
# The script searches your media libraries and performs house keeping on it.
#
# It's quite simple really, a lot of people use other tools to work with their
# content such as XBMC, KODI, etc which can remove shows you don't like, etc.
# But what they don't do is clean up other lingering subtitles, nfo's and other
# things that may have also been associated with the deleted file.
#
# Info about this TidyIt NZB Script:
# Author: Chris Caron (lead2gold@gmail.com).
# Date: Tue, May 15th, 2015.
# License: GPLv3 (http://www.gnu.org/licenses/gpl.html).
# Script Version: 0.0.1
#
# A script that can tidy up your library by removing stale content
# left over from removing video files from third party applications.
# The script looks after cleaning off any directory containing dangling
# information about a video file, but no video itself.
#
# NOTE: This script requires Python to be installed on your system.
#
# NOTE: I take absolutely no responsibility for any data loss sustained to
#       your media library from any mis-configuration you make.  The script
#       works well as long as you take caution when changing settings from
#       their default values.

##############################################################################
### OPTIONS                                                                ###

#  TidyIt Mode (Enabled, Disabled).
#
# Identify the TidyIt Mode you want to run in:
#  Enabled    - This enables the full capacity of this script. Actions are
#               still always logged eve with this mode set.
#  Disabled   - Log all planned tidy actions but do not actually do perform
#               them. This is the absolute safest mode to survey things with
#               first.
#
# This script's primary function is to remove content.
# After you configure it the way you want, you can use the logging to
# determine if it is doing what you expect it to. Only then should you
# enable it.  I take absolutely no responsibility for any loss of data
# sustained.
#
# NOTE: that you should ALWAYS operate in 'Disabled' mode first to confirm
#       that the script doesn't cause irreversable damage to your media library.
#
#Mode=Disabled

# Video Libraries to Scan
#
# Specify any number of directories this script can (recursively) check
# delimited by a comma and or space. ie: /home/nuxref/mystuff, /path/no3, etc
# For windows users, you can specify: C:\My Downloads, \\My\Network\Path, etc
#
#VideoPaths=

# Video Extra File Extensions.
#
# Identify the extra files you keep around with your video files. The script
# will scan for these files explicitly and remove them if a video file
# bearing the same name is not found.  For this reason you do not want to
# specify video extensions here.
#
# You can use a 'question mark' (?) to identify single placeholders for
# printable characters (this does not include white space). This list is not
# case-sensitive. You can also use a 'asterix' (*) to identify the regular
# expression (.*) or zero or many.  Keep in mind that *.nfo is the same as
# writing .nfo below.  the * is automatically implied at the front. Use a
# comma (,) and/or space to separate more then one entry.
# Example=.nfo,.??.srt,.srt,.sub,.txt,.sub,.idx,.-thumb.jpg,.tbn,.nzb,.xml
#
#VideoExtras=.nfo,.??.srt,.srt,.sub,.txt,.sub,.idx,.-thumb.jpg,.tbn,.nzb,.xml

# Minimum Video Size.
#
# Identify the minimum size (in MB) a video file must be before it's
# treated as part of your collection (and not a sample or extra).
# If you want every video file to be considered equal; simply set
# this value to zero (0).
#
#VideoMinSize=150

# File extensions for video files.
#
# Only files with these extensions are considered a video. Extensions must
# be separated with commas.
# Example=.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso
#
#VideoExtensions=.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso

# Tidy Safe Entries.
#
# No doubt there will be a situation where you will point the tidy script
# to a series of directories to which you want to intentionally avoid
# removing.  Use a comma to identify any content that immediately makes
# a directory safe from removal if found. You can specify directory or
# filenames. Simply use a comma and/or space to delimite multiple safe
# entries.
#
#SafeEntries=.notidy

# My Systems File Encoding (UTF-8, UTF-16, ISO-8859-1, ISO-8859-2).
#
# All systems have their own encoding; here is a loose guide you can use
# to determine what encoding you are (if you're not sure):
# - UTF-8: This is the encoding used by most Linux/Unix filesystems. just
#          check the global variable $LANG to see if that's what you are.
# - UTF-16: This is the encoding usually used by OS/X systems and NTFS.
# - ISO-8859-1: Also referred to as Latin-1; Microsoft Windows used this
#               encoding for years (in the past), and still do in some
#               cases. It supports the English, Spanish, and French language
#               character sets.
# - ISO-8859-2: Also referred to as Latin-2; It supports Czech, German,
#               Hungarian, Polish, Romanian, Croatian, Slovak, and
#               Slovene character sets.
#
# If you wish to add another encoding; just email me and i'll add it.
# All files that are downloaded will be written to your filesystem using
# the same encoding your operating system uses.  Since there is no way
# to detect this (yet), by specifying it here, you can make it possible
# to handle files with the extended character sets.
#
#SystemEncoding=UTF-8

# Enable debug logging (yes, no).
#
# If you experience a problem, you can bet I'll have a much easier time solving
# it for you if your logs include debugging.  This can be made possible by
# flipping this flag here.
#
#Debug=no

### NZBGET SCHEDULER SCRIPT                                                ###
##############################################################################

import re
from os.path import join
from os import listdir
from os.path import basename
from os.path import abspath
from os.path import dirname
from os.path import isdir
from os import unlink
from shutil import rmtree
from stat import ST_MTIME
# This is required if the below environment variables
# are not included in your environment already
import sys
sys.path.insert(0, join(dirname(__file__), 'TidyIt'))

# stat is used to test if the .srt file was fetched okay or not
from os import stat

# Script dependencies identified below
from datetime import timedelta
from datetime import datetime

# pynzbget Script Wrappers
from nzbget import SKIP_DIRECTORIES
from nzbget import SchedulerScript
from nzbget import EXIT_CODE
from nzbget import SCRIPT_MODE

# Meta Information
MEDIAMETA_FILES_RE = (
    re.compile('^(backdrop|banner|fanart|folder|poster|season-specials-poster)\.jpe?g', re.IGNORECASE),
    re.compile('^season[0-9]+(-(banner|poster))?\.(tbn|jpe?g)', re.IGNORECASE),
    re.compile('^tvshow.nfo', re.IGNORECASE),
    re.compile('^series.xml', re.IGNORECASE)
)

# Meta Directory(ies)
# Sometimes the matching meta information is actually within a subdirectory
# If mismatched data is found in directories identified here, they're match
# is searched against content in the parent directory too just to be safe
# before assuming the content should be removed
METADIRS = ( 'metadata', )

# A Tuple that contains all of the directories and/files that are always
# ignored reguardless and can be safely be removed if found within a directory
OS_METADATA_ENTRY = (
    'Thumbs.db',
) + SKIP_DIRECTORIES

# A list of compiled regular expressions identifying files to not parse ever
IGNORE_FILELIST_RE = (
    # Samples
    re.compile('^.*[-.]sample(\.[^.]*)?$', re.IGNORECASE),
    re.compile('^sample-.*$', re.IGNORECASE),
)

class TIDYIT_MODE(object):
    ENABLED = "Enabled"
    DISABLED = "Disabled"

# TidyIt Modes
TIDYIT_MODES = (
    TIDYIT_MODE.ENABLED,
    TIDYIT_MODE.DISABLED,
)
# Default in a Read-Only Mode; It's the safest way!
TIDYIT_MODE_DEFAULT = TIDYIT_MODE.DISABLED

# Some Default Environment Variables (used with CLI)
DEFAULT_VIDEO_EXTENSIONS = \
        '.mkv,.avi,.divx,.xvid,.mov,.wmv,.mp4,.mpg,.mpeg,.vob,.iso'

# Some Default Environment Variables (used with CLI)
DEFAULT_VIDEO_EXTRAS = \
        '.nfo,.??.srt,.srt,.sub,.txt,.sub,.idx,.-thumb.jpg,.tbn,.nzb,.xml,.diz'

# Some Default TidySafe Variables (used with CLI)
DEFAULT_TIDYSAFE_ENTRIES = \
        '.tidysafe'

class TidyCode(object):
    """ Codes returned by tidy_library() function that provide instructions
    as to what to do next
    """
    REMOVE = 0
    IGNORE = -1

# A collection of all the tidy_library() return codes
TIDY_CODES = (TidyCode.REMOVE, TidyCode.IGNORE)

# The number of seconds a matched directory/file has to have aged before it
# is processed further.  This prevents the script from removing content
# that may being processed 'now'.  All content must be older than this
# to be considered. This value is represented in seconds.
DEFAULT_MATCH_MINAGE = 120

# The number of MegaBytes the detected video must be (with respect
# to it's filesize). If it is less than this value, then it is
# presumed to be a sample.
DEFAULT_VIDEO_MIN_SIZE_MB = 150

# System Encodings
DEFAULT_ENCODINGS = (
    # Most Linux Systems
    'UTF-8',
    # NTFS/OS-X
    'UTF-16',
    # Most French/English/Spanish Windows Systems
    'ISO-8859-1',
    # Czech, German, Hungarian, Polish, Romanian,
    # Croatian, Slovak, Slovene.
    'ISO-8859-2',
)

# Filesystem Encoding
DEFAULT_SYSTEM_ENCODING = 'UTF-8'

class TidyItScript(SchedulerScript):
    """A Media Library Tidying tool written for NZBGet
    """
    def _re_str(self, re_str):
        """
        Support custom RE provided by this script where * becomes .*
        and ? becomes .
        """
        return re.sub('?', '.', re.sub('*', '.*', re_str))

    def _remove(self, path, recursive=False):
        """
        A Simple wrapper to removing content in addition to logging it.
        """

        if not isdir(path):
            # File Removal
            if self.mode == TIDYIT_MODE.ENABLED:
                try:
                    unlink(path)
                    self.logger.info('Removed FILE: %s' % path)
                except:
                    self.logger.error('Could not removed FILE: %s' % path)
                    return False
            else:
                self.logger.info('PREVIEW ONLY: Remove FILE: %s' % path)
        else:
            # Directory Removal
            if self.mode == TIDYIT_MODE.ENABLED:
                try:
                    rmtree(path)
                    self.logger.info('Removed DIRECTORY: %s' % path)
                except:
                    self.logger.error('Could not removed DIRECTORY: %s' % path)
                    return False
            else:
                self.logger.info('PREVIEW ONLY: Remove DIRECTORY: %s' % path)
        return True

    def tidy_library(self, path, extensions, extras, minsize, *args, **kwargs):
        """
          - Recursively scan a library path and returns the number of files
            found in a directory.

          But the path library will be skewed if changes are determiend to happen.
          - If a directory contains another directory within it; it will never
            be removed.
              - If a meta directory exists, it will not be considered as part
                of this rule.
            The directory passed into the function (for the first time
            will 'never' be removed reguardless of scanned outcome

        """
        if not isdir(path):
            # Not a directory? then return a value that will prevent
            # the file/block from being removed (non-zero)
            return TidyCode.IGNORE

        # Internal Tracking of Directory Depth
        # A depth of 0 is a 'safe' directory that will
        # never be removed
        current_depth = kwargs.get('__current_depth', 1)
        if current_depth == 1:
            self.logger.info('Scanning %s' % path)

        # Change to absolute path
        path = abspath(path)

        ref_time = datetime.now() - timedelta(seconds=DEFAULT_MATCH_MINAGE)
        # Check absolute path date (because we don't want to
        # process anything in it if it was touched recently)
        if current_depth > 1:
            try:
                mtime = datetime.fromtimestamp(stat(path)[ST_MTIME])
                if mtime >= ref_time:
                    # We're done; directory is to new
                    self.logger.debug('Skipping %s; modified less than %ds ago.' % (
                        path,
                        DEFAULT_MATCH_MINAGE,
                    ))
                    return TidyCode.IGNORE

            except OSError:
                # The directory suddently became inaccessible
                self.logger.warning(
                    'Directory %s became inaccessible.' % path,
                )
                # Since the directory is missing, return 0 letting
                # recursively called situations go ahead and handle
                # this directory
                if current_depth > 1:
                    return TidyCode.REMOVE
                return TidyCode.IGNORE

            except ValueError:
                # datetime could not parse the time correctly
                # Newly created directories won't have this problem
                # we can move along
                pass

        # First check for the goods; we may not have to do
        # further processing otherwise
        _valid_paths = self.get_files(
            path,
            suffix_filter=extensions,
            min_depth=1, max_depth=1,
            fullstats=True,
            skip_directories=False,
        )

        # Apply Filters To Detect actual valid video files
        _valid_paths = dict([ (k, v) for (k, v) in _valid_paths.items() if \
                  v['filesize'] >= minsize]).keys()

        # Apply Ignore list
        valid_paths = list()
        while(len(_valid_paths)):
            _path = _valid_paths.pop()
            if True in [ v.match(path) is not None \
                        for v in IGNORE_FILELIST_RE ]:
                self.logger.debug('Skipping - Ignored file: %s' % basename(_path))
                continue
            valid_paths.append(_path)
        del _valid_paths

        if len(valid_paths):
            # at least one valid file was found in this directory
            # but it doesn't rule out the fact the possibility of
            # movie files existing in further sub directories.
            # so we flag this as a safe dir and keep processing

            # The easiest way to mark a directory safe is to just
            # toggle the current_depth to one (1).
            current_depth = 1

            # Get Directory entries
            dirents = [ d for d in listdir(path) \
                          if d not in ('..', '.') and isdir(d) ]
        else:
            # Get All Entries
            dirents = [ d for d in listdir(path) \
                        if d not in ('..', '.') ]

        tidylist = []
        cannonfodder = []
        while len(dirents):

            # Pop directory entry
            dirent = dirents.pop()

            # Build absolute path with it
            fullpath = join(path, dirent)

            # Check for TidySafe Content
            if dirent in self.tidysafe_entries:
                # it was found; change the current depth
                # to 1 to enforce a tidy safe environment
                current_depth = 1
                self.logger.debug('Ignoring %s; found %s' % (path, dirent))
                continue

            # METADATA is only cannon-fodder if it's determined
            # the directory should be removed
            if dirent in OS_METADATA_ENTRY:
                # We can go ahead and remove this
                if not len(valid_paths) and current_depth > 1:
                    cannonfodder.append(fullpath)
                continue

            if isdir(fullpath):
                if dirent in METADIRS and len(valid_paths):
                    # We skip this directory 'only if' we matched
                    # a video file
                    valid_paths.append(fullpath)
                    continue

                # Recursively continue scanning
                code = self.tidy_library(
                    path=fullpath,
                    extensions=extensions,
                    extras=extras,
                    minsize=minsize,
                    # Internal
                    __current_depth=current_depth+1,
                )

                if code == TidyCode.IGNORE:
                    # Add this directory back to the
                    # valid paths to prevent it from being
                    # removed later
                    valid_paths.append(fullpath)

                elif code == TidyCode.REMOVE:
                    tidylist.append(fullpath)
                continue

            # If we make it to the end, we scanned a file
            # that does not meet filtering criterias
            self.logger.debug('TidyFilters skipped from %s' % fullpath)
            break

        for entry in cannonfodder:
            self._remove(entry, recursive=True)

        for entry in tidylist:
            self._remove(entry, recursive=True)

        if len(dirents) + len(valid_paths):
            # We have a media directory worth keeping
            return TidyCode.IGNORE

        if current_depth > 1:
            return TidyCode.REMOVE

        return TidyCode.IGNORE


    def tidy(self):
        """All of the core cleanup magic happens here.
        """

        if not self.validate(keys=(
            'Mode',
            'VideoPaths',
            'VideoMinSize',
            'VideoExtensions',
            'SafeEntries',
            'VideoExtras',
            'SystemEncoding')):

            return False


        # Fix mode to object (self.*)
        self.mode = self.get('Mode', TIDYIT_MODE_DEFAULT)
        self.tidysafe_entries = self.parse_list(self.get('SafeEntries', DEFAULT_TIDYSAFE_ENTRIES))

        # Remaining Environment Variables
        video_extension = self.get('VideoExtensions', DEFAULT_VIDEO_EXTENSIONS)
        video_extras = self.get('VideoExtras', DEFAULT_VIDEO_EXTENSIONS)
        video_minsize = int(self.get('VideoMinSize', DEFAULT_VIDEO_MIN_SIZE_MB)) * 1048576
        encoding = self.get('SystemEncoding', DEFAULT_SYSTEM_ENCODING)
        paths = self.parse_path_list(self.get('VideoPaths'))

        for path in paths:
            self.tidy_library(
                path,
                extensions=video_extension,
                extras=video_extras,
                minsize=video_minsize,
            )

        # Nothing fetched, nothing gained or lost
        return None

    def scheduler_main(self, *args, **kwargs):
        """Scheduler
        """

        return self.tidy()

    def main(self, *args, **kwargs):
        """CLI
        """
        return self.tidy()


# Call your script as follows:
if __name__ == "__main__":
    from sys import exit
    from optparse import OptionParser

    # Support running from the command line
    usage = "Usage: %prog [options] [scandir1 [scandir2 [...]]]"
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-n",
        "--encoding",
        dest="encoding",
        help="The system encoding to use (utf-8, ISO-8859-1, etc)." + \
             " The default value is '%s'" % DEFAULT_SYSTEM_ENCODING + ".",
        metavar="ENCODING",
    )
    parser.add_option(
        "-s",
        "--safe-entries",
        dest="safeentries",
        help="If a safe-entry file/dir is located within a path scanned " +\
             "then the path is ignored. Use safe-entry files (or dirs) " +\
             "to intentionally ignore directories of your choice that " +\
             "reside in your video library. You can specify more then one " +\
             "safe-entry by separating them with a comma (,). " +\
             "The default value(s) are '%s'" % (DEFAULT_TIDYSAFE_ENTRIES) +\
             ".",
        metavar="ENTRIES",
    )
    parser.add_option(
        "-m",
        "--video-minsize",
        dest="video_minsize",
        help="Specify the minimum size a video must be before it's " +\
        "treated as part of your collection. This value is used to " +\
        "diffentiate between video file and samples files.  This value " +\
        "is interpreted in MB (Megabytes) and defaults to %d MB." % \
        DEFAULT_VIDEO_MIN_SIZE_MB,
        metavar="SIZE_IN_MB",
    )
    parser.add_option(
        "-c",
        "--clean",
        dest="clean",
        action="store_true",
        help="Unless this switch is specified, this script only runs in a " +\
        "log only mode (a dry-run) allowing you to see the actions the " +\
        "script would have otherwise performed.",
    )
    parser.add_option(
        "-L",
        "--logfile",
        dest="logfile",
        help="Send output to the specified logfile instead of stdout.",
        metavar="FILE",
    )
    parser.add_option(
        "-D",
        "--debug",
        action="store_true",
        dest="debug",
        help="Debug Mode",
    )
    options, _args = parser.parse_args()

    logger = options.logfile
    if not logger:
        # True = stdout
        logger = True
    debug = options.debug

    script_mode = None
    videopaths = ''
    if len(_args):
        # Support command line arguments too
        videopaths = ','.join(_args)

    # We always enter this part of the code, so we have to be
    # careful to only set() values that have been set by an
    # external switch. Otherwise we use defaults or what might
    # already be resident in memory (environment variables).
    _encoding = options.encoding
    _video_minsize = options.video_minsize
    _clean = options.clean
    _safeentries = options.safeentries

    if _clean:
        # By specifying a clean switch, we know for sure the user is
        # running this as a standalone script,

        # Setting Script Mode to NONE forces main() to execute
        # which is where the code for the cli() is defined
        script_mode = SCRIPT_MODE.NONE

    if videopaths:
        # By specifying a videopath, we know for sure the user is
        # running this as a standalone script,

        # Setting Script Mode to NONE forces main() to execute
        # which is where the code for the cli() is defined
        script_mode = SCRIPT_MODE.NONE

    script = TidyItScript(
        logger=logger,
        debug=debug,
        script_mode=script_mode,
    )

    if _clean:
        script.set('Mode', TIDYIT_MODE.ENABLED)

    if _video_minsize:
        try:
            _video_minsize = str(abs(int(_video_minsize)))
            script.set('VideoMinSize', _video_minsize)
        except (ValueError, TypeError):
            script.logger.error(
                'An invalid `video_minsize` (%s) was specified.' % (_video_minsize)
            )
            exit(EXIT_CODE.FAILURE)

    if _safeentries:
        script.set('SafeEntries', _safeentries)

    if _encoding:
        script.set('SystemEncoding', _encoding)

    if videopaths:
        if not _encoding:
            # Force defaults if not set
            script.set('SystemEncoding', DEFAULT_SYSTEM_ENCODING)

        if not _clean:
            script.set('Mode', TIDYIT_MODE_DEFAULT)

        if not _video_minsize:
            script.set('VideoMinSize', DEFAULT_VIDEO_MIN_SIZE_MB)

        if not _safeentries:
            script.set('SafeEntries', DEFAULT_TIDYSAFE_ENTRIES)

        # Force generic Video Extensions
        script.set('VideoExtensions', DEFAULT_VIDEO_EXTENSIONS)

        # Force generic Video Extras
        script.set('VideoExtras', DEFAULT_VIDEO_EXTRAS)

        # Finally set the directory the user specified for scanning
        script.set('VideoPaths', videopaths)

    if not script.script_mode and not script.get('VideoPaths'):
        # Provide some CLI help when VideoPaths has been
        # detected as not being identified
        parser.print_help()
        exit(1)

    # call run() and exit() using it's returned value
    exit(script.run())
