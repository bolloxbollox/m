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
      choices=[ "activation", "upgrade" ],
      help="If membership, specify if membership activation or an upgrade")

   parser.add_argument("-u", "--unit",
      action="store_true",
      default=False,
      help="A (very small) bit of unit test")

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
   def handle(self):
   #########################################################################
      # In "real" life this should call other systems instead of printing
      # probably using other classes (member, packingSlip, ...)
      if self.productType in physicalProducts: 
         print("Generate a commission payment to the agent")
         print("Instantiate packing slip for shipping")
         print("   add %s \"%s\" to packing slip" % ( self.productType, self.title ))
      if self.productType == "video" and self.title == self.magicTitle : 
         print("   add video \"First Aid\" to packing slip")
      if self.productType == "book" : 
         print("   duplicate the packing slip for the royalty department")

      if self.productType == "membership" : 
         if self.action == "activation":
            print("Create new membership and activate it")
         elif self.action == "upgrade":
            print("Find the membership in database or similar and upgrade it")
         print("   e-mail the owner and inform them of the membership %s" % self.action )

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
def test():
############################################################################
   print("Testing")
   o1 = order( log, productType = "book", title = "Bla bla" )
   assert "valid" == o1.validate()

   o2 = order( log, productType = "book", action = "Bla bla" )
   assert "valid" != o2.validate()

   print("Done testing")

############################################################################
def main():              # Start the show
############################################################################
   cfgVal = parseArgs()
   log = logging.getLogger("self")

   log.setLevel( 60 - ( min(cfgVal.verbosity, 5)  * 10))
   if cfgVal.verbosity > 5 :
      log.error("Max verbosity level is 5, passing %d v's is silly" % cfgVal.verbosity  )

   log.debug("verbosity  = %d (=> %s)" % (cfgVal.verbosity, logging.getLevelName(log.level)))
   if cfgVal.unit:
      test()
      sys.exit(0)

   #log.set_threshold(5 - cfgVal.verbosity )
   for l in [ "debug", "info", "warning", "error", "critical" ]:
      (getattr(log,l))( "Log Level %s" % l)

   o = order( log, productType = cfgVal.productType, action = cfgVal.action, title = cfgVal.title )
   rs = o.validate()
   if rs != "valid":
      print("Error: %s" % rs)
      sys.exit(1)
   o.handle()

############################################################################

if __name__ == "__main__":
   main()

sys.exit(0)