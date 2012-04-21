#!/usr/bin/python
#
# Internet Pulse Scraper
# by Tony Perriello (tony.perriello@gmail.com)
#

import sys
import urllib
import re
import datetime

def display_latencies(matches, min_lat, max_lat):
   print '--------------------------------------------'
   if min_lat == 0:
     sys.stdout.write('Normal')
   elif min_lat == 90:
     sys.stdout.write('Warning')
   elif min_lat == 180:
     sys.stdout.write('Critical')
   elif (min_lat == 0) & (max_lat == 9999):
     sys.stdout.write('All')
   
   print ' latencies as of', datetime.datetime.now()

   for match in matches:
     if (int(match[2]) > min_lat) & (int(match[2]) < max_lat):
       print 'Origin: ', match[0], '\nDestination: ', match[1], '\nLatency: ', match[2], '\n\n'
   print '--------------------------------------------'
   
def print_usage():
  print 'usage: internetpulse.py [LATENCY TYPE]'
  print '-h: Healthy latencies (< 90 ms)\n-w: Warning latencies (< 180 ms)\n-c: Critical latencies (> 180 ms)\n-a: All latencies'

def check_args():
  # Set the min and max latencies to look for based on the arguments.   
    if len(sys.argv) == 1:
      print_usage()
      exit(1)
    elif sys.argv[1] == '-h':
      min_lat = 0
      max_lat = 90
    elif sys.argv[1] == '-w':
      min_lat = 90
      max_lat = 180
    elif sys.argv[1] == '-c':
      min_lat = 180
      max_lat = 9999
    elif sys.argv[1] == '-a':
      min_lat = 0
      max_lat = 9999
    else:
      print 'invalid argument.\n'
      print_usage()
      exit(1)

    return min_lat, max_lat

def main():
    # Validate args and set min/max lat range based on arg
    min_lat, max_lat = check_args()

    # Get the main internetpulse page
    ufile = urllib.urlopen('http://www.internetpulse.com')
    page = ufile.read()

    # Parse the html for the Origin/Destination/Latency pattern 
    matches = re.findall('Origin=(\S+)&amp;Destination=(\S+)&amp;.+>(\d+)</a>', page)

    # Show the appropriate latencies based on the args
    display_latencies(matches, min_lat, max_lat)

if __name__ == '__main__':
    main()
