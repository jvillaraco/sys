#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
verifyIPsendMail.py
This program verifies external home IP and sends IP if it has changed.

@author: Joan G. Villaraco


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

Execution: python usermodMultiple01.py group usersList.txt
Requirements: - Path to whereis binary
              - Txt file with users
"""
import sys
import argparse
import subprocess
import shlex
import os

DEBUG = True
COMMAND = 'usermod'
COMMAND_ARG = ' -a -G <userGroup> <user>'
WHEREIS = '/usr/bin/whereis'


def main():
    # Verifica parametres
    param = verifyParameters(sys.argv)
    if DEBUG:
        # print param.grup
        print param.fitxerTemp        
    copyMailFile(param.fitxerTemp)
    # Execute line to write IP in mailFile
    # Compare both files
    # if files are different sendmail otherwise do nothing
    sIP = loadIP(param.fitxerTemp)
    print sIP
#    commandArgWithGroup = COMMAND_ARG.replace("<userGroup>", param.grup)
#    commandPath = whereIsCommand(COMMAND.split()[0])
#    if DEBUG:
#        print commandPath + commandArgWithGroup
#    execCommands(commandPath + commandArgWithGroup, lUsers)


def copyMailFile(mailFile, debug=DEBUG):
    cpCommand = whereIsCommand('cp')
    command = [cpCommand, param.fitxerTemp,
               os.path.dirname(param.fitxerTemp) + 'mailAnt.txt']
    print command
    execCommand(command)


def prepareCommand(command, lUsers, debug=DEBUG):
    for user in lUsers:
        userCommand = command.replace('<user>', user)
        lUserCommand = userCommand.split()
        if debug:
            print userCommand
            print lUserCommand
        (ret, out, error) = execCommand(lUserCommand, False)
        if ret != 0:
            # Cut the last char of the error that is a LF or CR
            print "Error %s: %s" % (ret, error.rstrip(error[-1:]))
            print "Comanda de l'error: %s" % userCommand
            # print error.rstrip(error[-1:])
        else:
            print "Perfecte %s: %s" % (ret, out)


def execCommand(command, debug=DEBUG):
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    error = process.stderr.read()
    out = process.stdout.read()
    process.stderr.close()
    process.stdout.close()
    if debug:
        print("Salida de errores:\n")
        print error
        # error = error.decode(sys.getdefaultencoding())
        # print(error)
        print("Salida del comando:\n")
        print out
        # out = out.decode(sys.getdefaultencoding())
        # print(out.split()[1])
        # print ret
        # print "pepe: %s" % ret.split()
        print "Error? %s" % process.wait()
    return (process.wait(), out, error)


def whereIsCommand(command, debug=DEBUG):
    process = subprocess.Popen(['whereis', command],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    error = process.stderr.read()
    out = process.stdout.read()
    process.stderr.close()
    process.stdout.close()
    if debug:
        print("Salida de errores:\n")
        print error
        error = error.decode(sys.getdefaultencoding())
        print(error)
        print("Salida del comando:\n")
        print out
        out = out.decode(sys.getdefaultencoding())
        print(out.split()[1])
        # print ret
        # print "pepe: %s" % ret.split()
    return out.split()[1]


def loadIP(filePath, debug=DEBUG):
    ipFile = open(filePath, 'r')
    ipLine = ipFile.readline()
    ipFile.close()
    # print userLines
    if debug:
        print ipLine
    return ipLine.lstrip()


def verifyParameters(parametres, debug=DEBUG):
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    # parser.add_argument("grup", help="Grup on s'afegeix la llista")
    parser.add_argument("fitxerTemp", help="Cami al fitxer de la darrera IP")
    args = parser.parse_args()
    if args.verbose:
        print "verbosity turned on"
    return args


if __name__ == '__main__':
    main()
