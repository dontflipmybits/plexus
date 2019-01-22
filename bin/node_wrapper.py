#!/opt/splunk/bin/python
from subprocess import call
import sys, os

splunk_node_path = os.path.join(sys.path[0], "..", "..", "..", "..", "bin", "node")
script_to_run = os.path.join(sys.path[0], "file_scraper.js")

call([splunk_node_path, script_to_run])