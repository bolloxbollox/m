#!/usr/bin/python3
# -*- Mode: Python -*- 

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

# A book IS a physical product !
physicalProducts = [ "book", "video" ]
virtualProducts = [ "membership" ]

############################################################################
def parseArgs():        # Parse the input
############################################################################
   parser = argparse.ArgumentParser( 
      description="Business Rules Engine",
      formatter_class=argparse.RawTextHelpFormatter,
      epilog="Problem 2 (python ver %s)" % platform.python_version() )

   parser.add_argument("-p", "--productType",
      default="unknown",
      choices = physicalProducts + virtualProducts,
      help='Specify the product')

   parser.add_argument("-t", "--title",
      default = None,
      help="If book or video, this sets the title")

   parser.add_argument("-a", "--action",
      default = None,
      choices=[ "new", "upgrade" ],
      help="If membership, specify if new member or an upgrade")

   parser.add_argument("-v", "--verbosity",
      action="count",
      default=0,
      help="increase output verbosity")

   cfgVal = parser.parse_args()
   return cfgVal

############################################################################
class order:
############################################################################
   action = None
   productType = None
   title = None

   magicTitle = "Learning to Ski"
   productTypes = physicalProducts + virtualProducts

   #########################################################################
   def __init__(self, log, productType = None, title = None, action = None ):
   #########################################################################
      self.log = log
      if   productType in physicalProducts: 
         self.title    = title
      elif productType in virtualProducts:
         self.action   = action
      else:
         print("ERROR: unknown product type %s" % productType  )
         sys.exit(1)

      self.productType = productType

   #########################################################################
   def validate(self): 
   #########################################################################
      s = "valid"
      if   self.productType in physicalProducts and self.title == None:
         s = "%s needs a title" % self.productType
      if   self.productType in virtualProducts and self.action == None:
         s = "%s needs an action" % self.productType
      return s

   #########################################################################
   def __str__(self):
   #########################################################################
      s  = "Type: %s, " % self.productType
      if self.title is not None:
         s += "Title: %s, " % self.title
      if self.action is not None:
         s += "Action: %s, " % self.action
      s += "Status: %s" % self.validate()
      return s

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

   o = order( log, productType = cfgVal.productType, action = cfgVal.action, title = cfgVal.title )
   log.info(o)

############################################################################

if __name__ == "__main__":
   #  parseArgs()
   main()

sys.exit(0)
