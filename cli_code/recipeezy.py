#!/usr/bin/env python3
import sys
import db_fcns

argc = len(sys.argv)
options = {'--help': db_fcns.help,
           '--add-entry': db_fcns.add_entry,
           '--get-all': db_fcns.get_all,
           '--get-entry': db_fcns.get_entry,
           '--remove-entry': db_fcns.rm_entry,
           '--downvote': db_fcns.downvote,
           '--upvote': db_fcns.upvote,
           '--add-tag': db_fcns.addtag}
if argc < 2:
    print("Usage: recipeezy <option> [<args>]")
    sys.exit()
try:
    funchandle = options[sys.argv[1]]
except KeyError as e:
    print(f"Error: {e} not an option. Type --help for available options.")
    sys.exit()
if sys.argv[1] in ['--help', '--get-all']:
    funchandle()
elif sys.argv[1] in ['--add-tag']:
    funchandle(sys.argv[2], sys.argv[3])
else:
    funchandle(sys.argv[2])

