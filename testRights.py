#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
testRights.py

 This program verifies writable directories with the user who executes in
a scope with a non-limited number of exclusions.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Version: 160531
@author: Joan G. Villaraco

Requirements:
- Be sure there is no file named like FILENAME in the search scope
- Alls params in absolute path

Execution:
- python testRights.py <searchPathScope> [excludedDir1 ... [excludedDirN]]

Results:
    Directori amb escriptura: %s /tmp
    Directori amb escriptura: %s /dev/shm
    Directori amb escriptura: %s /dev/mqueue
    Directori amb escriptura: %s /proc/247/cwd
    Directori amb escriptura: %s /proc/247/task/247/cwd
    Directori amb escriptura: %s /proc/253/cwd
    Directori amb escriptura: %s /proc/253/task/253/cwd
    Directori amb escriptura: %s /run/lock
    Directori amb escriptura: %s /var/lock
    Directori amb escriptura: %s /var/tmp
"""

import os
import sys
from os.path import join, getsize


FILENAME = "pepepepepepepepepe.txt"
DEBUG = False


def testDir(path):
    try:
        f = open(path + '/' + FILENAME, "w")
    except IOError as err:
        if DEBUG:
            # print ("OS Error: {0}".format(err))
            print "OS Error: %s", err
    except:
        print ("Unexpected error:", sys.exc_info()[0])
    else:
        print "Writable directory: %s", path
        f.close()
        os.remove(path + '/' + FILENAME)


def isPathInExcDirs(path, excDirs):
    foundInExcDirs = False
    for excDir in excDirs:
        if DEBUG:
            print "(isPath)path: %s, excDir: %s, \
                    path.startswith(excDir): %s", (
                path, excDir, path.startswith(excDir))
        if path.startswith(excDir):
            foundInExcDirs = True
            break
    return(foundInExcDirs)


def walkDirs(dir, excDirs):
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            path = join(root, dir)
            if isPathInExcDirs(path, excDirs):
                pass
            else:
                testDir(path)


def main():
    if len(sys.argv) == 1:
        print "Usage: %s Path [excudedPath]..." % sys.argv[0]
        sys.exit(-1)
    if DEBUG:
        print len(sys.argv)
    dirsFile = sys.argv[1]
    del sys.argv[0:2]
    if DEBUG:
        print sys.argv
    walkDirs(dirsFile, sys.argv)


if __name__ == '__main__':
    main()
