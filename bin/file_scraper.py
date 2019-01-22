# coding: utf8
import argparse, json, time, os

"""
sample output:
{"timestamp":1544139712113,
    "drive":"E",
    "folder":"E:\\Movies\\A",
    "filePath":"E:\\Movies\\A\\A Movie Name (2019) x265 AC3 6ch 2160p, 3840x2160, 4 500 Kbps.mkv",
    "file":"A Movie Name (2019) x265 AC3 6ch 2160p, 3840x2160, 4 500 Kbps.mkv",
    "size":5151515151,
    "created":1511111111111.1234,
    "accessed":1511111111112.1234,
    "modified":1511111111113.1234
}
"""

default_dirs = [] #Add any directories you want scanned by default, then comment out the next two lines.
default_config_file = open(os.path.join(os.getcwd(),"config.json"), "r").read() #See the config.json file to change the directories to be monitored.
default_dirs = json.loads(default_config_file)["monitored_directories"]

#parse arguments
#arguments include directories to be parsed, save location
parser = argparse.ArgumentParser(description='Parse files')
parser.add_argument('-r', '-d', '--read', '--dir', action='append', dest='directories', default=default_dirs, help='Specify a directory to read from.  For multiple directories, use the switch multiple times. (default current working directory)')
parser.add_argument('-w', '--write', dest='savedir', help='Specify a directory to write to. (default current working directory)')

args = parser.parse_args()
if len(args.directories)==0:
    args.directories = [os.getcwd()]

for top in args.directories:
    #recursively pull file list
    for root,dirs,files in os.walk(top): #Roots is the root dir.  dirs and files are what the root contains.  Dirs will be referenced as roots as the function recurses.
        if files: #only parse if files exist
            for file in files:
                try:
                    #initialize data blob
                    blob = {}
                    #build data blob
                    blob['timestamp'] = int(round(time.time() * 1000)) #Python does time in seconds with a decimal up to nano seconds.  time*1000 gets us milliseconds.
                    blob['drive'] = os.path.splitdrive(os.path.join(root,file))[0]
                    blob['folder'] = root
                    blob['filePath'] = os.path.join(root,file) #os.path.join accounts for slashes and stuff
                    blob['file'] = file
                    blob['size'] = os.path.getsize(os.path.join(root,file))
                    blob['created'] = os.stat(os.path.join(root,file)).st_ctime*1000
                    blob['accessed'] = os.stat(os.path.join(root,file)).st_atime*1000
                    blob['modified'] = os.stat(os.path.join(root,file)).st_mtime*1000
                    print(json.dumps(blob, ensure_ascii=False, encoding="utf-8") + "\n")

                except Exception as e:
                    blob['error'] = e
                    try:
                        print(json.dumps(blob['error'], ensure_ascii=False, encoding="utf-8") + "\n")

                    except:
                        print(e)