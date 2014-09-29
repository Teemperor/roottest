#!/usr/bin/env python
""" Clever (with filters) compare command using difflib.py providing diffs in four formats:
  
  * ndiff:    lists every line and highlights interline changes.
  * context:  highlights clusters of changes in a before/after format.
  * unified:  highlights clusters of changes in an inline format.
  * html:     generates side by side comparison with change highlights.
  
  """
import sys, os, time, difflib, optparse, re
#---------------------------------------------------------------------------------------------------------------------------
#---Filter and substitutions------------------------------------------------------------------------------------------------

def filter(lines):
  outlines = []
  for line in lines:
    #---Processing line from interpreter (root.exe)------------------------------
    if re.match(r'^Processing ', line):
      continue
    #---ACLiC info---------------------------------------------------------------
    if re.match(r'^Info in <\w+::ACLiC>: creating shared library', line):
      continue
    #---Compilation error--------------------------------------------------------
    elif re.search(r': error:', line):
      nline = re.sub(r'\S+/', '', line)
      nline = re.sub(r':[0-9][0-9]:', ':--:', nline)
    #---Wrapper input line-------------------------------------------------------
    elif re.match(r'^In file included from input_line', line):
      continue
    else:
      nline = line
    #---Remove Addresses in cling/cint-------------------------------------------
    nline = re.sub(r'[ ]@0x[a-fA-F0-9]+', '', nline)
    #---Remove versioning in std-------------------------------------------------
    nline = re.sub(r'std::__[0-9]::', 'std::', nline)
    #---Remove white spaces------------------------------------------------------
    nline = re.sub(r'[ ]', '', nline)
    outlines.append(nline)
  return outlines

#-----------------------------------------------------------------------------------------------------------------------------
def main():
  usage = "usage: %prog [options] fromfile tofile"
  parser = optparse.OptionParser(usage)
  parser.add_option("-c", action="store_true", default=False, help='Produce a context format diff (default)')
  parser.add_option("-u", action="store_true", default=True, help='Produce a unified format diff')
  parser.add_option("-m", action="store_true", default=False, help='Produce HTML side by side diff (can use -c and -l in conjunction)')
  parser.add_option("-n", action="store_true", default=False, help='Produce a ndiff format diff')
  parser.add_option("-l", "--lines", type="int", default=3, help='Set number of context lines (default 3)')
  (options, args) = parser.parse_args()
  
  if len(args) == 0:
    parser.print_help()
    sys.exit(1)
  if len(args) != 2:
    parser.error("need to specify both a fromfile and tofile")
  
  n = options.lines
  fromfile, tofile = args
  
  fromdate = time.ctime(os.stat(fromfile).st_mtime)
  todate = time.ctime(os.stat(tofile).st_mtime)
  fromlines = open(fromfile, 'U').readlines()
  tolines = open(tofile, 'U').readlines()

  fromlines = filter(fromlines)
  tolines = filter(tolines)

  if options.u:
    diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)
  elif options.n:
    diff = difflib.ndiff(fromlines, tolines)
  elif options.m:
    diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile,context=options.c,numlines=n)
  else:
    diff = difflib.context_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)
  
  difflines = [line for line in diff]
  sys.stdout.writelines(difflines)

  if difflines : sys.exit(1)
  else         : sys.exit(0)

if __name__ == '__main__':
  main()
