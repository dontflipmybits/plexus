const fs = require("fs");
var json = JSON.parse(fs.readFileSync(__dirname + "\\config.json")); //format is {"monitored_directories": ["directory_path1","directory_path2"]}
var monitored_directories = json.monitored_directories;

function dirCrawler(directory) {
    fs.readdir(directory, function(err, child) {
        if (err) console.log("Error in dirCrawler", err);
        else {
            for (i = 0; i < child.length; i++) {
                var filePath = directory + "\\" + child[i];
                filePath.replace(/\/\//g, "/");
                var stats = fs.statSync(filePath);
                if (stats.isDirectory()) {
                    dirCrawler(filePath);
                } else
                    fileLogger(directory, child[i]);
            }
        }
    });
}

function fileLogger(directory, file) {
    var data = {};
    data.timestamp = Date.now();
    data.drive = directory.slice(0, 1);
    data.folder = directory;
    data.filePath = directory + "\\" + file;
    data.filePath.replace(/\/\//g, "/");
    data.file = file;
    var stats = fs.statSync(data.filePath);
    data.size = stats.size;
    data.created = stats.ctimeMs;
    data.accessed = stats.atimeMs;
    data.modified = stats.mtimeMs;
    console.log(JSON.stringify(data) + "\n");
}



for (var i in monitored_directories)
    dirCrawler(monitored_directories[i]);