#!/usr/bin/python3
#                             -*- Mode: Python -*- 
#  Last Modified On: Thu Apr 22 15:35:00 2021
# 

import sys, platform
import logging
import datetime, locale
import socket
import argparse

logging.basicConfig(
   format="%(asctime)s %(levelname).3s [# %(lineno)3d] -- %(message)s",
   level=logging.INFO
)

global log
log = logging.getLogger("self")

############################################################################
def parseArgs():        # Parse the input
############################################################################
   parser = argparse.ArgumentParser( 
      description="Python template",
      formatter_class=argparse.RawTextHelpFormatter,
      epilog="Only use if you know what you're doing (python ver %s)" % platform.python_version() )

   parser.add_argument("-v", "--verbosity",
      action="count",
      default=0,
      help="increase output verbosity")

   cfgVal = parser.parse_args()
   return cfgVal




############################################################################
def main():              # Start the show
############################################################################
   cfgVal = parseArgs()
   log = logging.getLogger("self")

   log.setLevel( 60 - ( min(cfgVal.verbosity, 5)  * 10))
   if cfgVal.verbosity > 5 :
      log.error("Max verbosity level is 5, passing %d v's is silly" % cfgVal.verbosity  )

   log.debug("verbosity  = %d (=> %s)" % (cfgVal.verbosity, logging.getLevelName(log.level)))

   #log.set_threshold(5 - cfgVal.verbosity )
   for l in [ "debug", "info", "warning", "error", "critical" ]:
      (getattr(log,l))( "Log Level %s" % l)

############################################################################

if __name__ == "__main__":
   #  parseArgs()
   main()

sys.exit(0)
