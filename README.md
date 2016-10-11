# S3 Backup App
The app works with Amazon S3 using versioned buckets to backup and restore files.

##Features
* Unix and windows versions.
* Any file type supported.
* Easy to restore files.
* Infrequent Access, Reduced Redundancy and Standard storage classes supported.
* Low overhead

##Usage
The app is designed to work with a Amazon S3 bucket that has versioning enabled. 
A none versioned bucket can be used if you wish to only store the latest version but the `--timestamp` argument will not work.

###Config File
The app uses a json config file named `config.json` by default it is in:
* On windows `%appdata%\amazon-backup\`
* On Unix `~/.local/share/amazon-backup/`
The file can be named anything and placed anywhere however and passed in via the `--config` argument

**Be aware** the config file is required for restoring files and should be backed up as well. 
The app can backup its own config files by adding its location like any other folder.

A basic config file structure is this:

```
{
    "folders": [
        {
            "name": "Folder",
            "path": "C:\\Users\\Username\folder to be backedup",
            "ignore": [
                "C:\\Users\\Username\folder to be backedup\\ignore this",
                "C:\\Users\\Username\folder to be backedup\\ignore that"
            ],
            "bucket_name": "backup bucket",
            "bucket_path": "subfolder1/",
            "aws_credentials":{
                "api_key" : "****************",
                "secret_key" : "***************"
            }
        },
        {
            "name": "Folder 2",
            "path": "C:\\Users\\Username\folder to also be backedup",
            "ignore": [
                "C:\\Users\\Username\folder to also be backedup\\ignore this",
                "C:\\Users\\Username\folder to also be backedup\\ignore that"
            ],
            "bucket_name": "backup bucket",
            "bucket_path": "subfolder2/",
            "aws_credentials":{
                "api_key" : "****************",
                "secret_key" : "***************"
            }
        }
    ]
}
```

`"folders"` contains a list of all the folders to be backed up.

Each folder is a dict containing:
* `"name"` Is your name for the folder to be backed up it should be a one line string.
* `"path"` Is the absoute path to the folder you wish to backup.
* `"ignore"` Is a list of absoute path's you wish to be ignored when the backup takes place.
* `"bucket_name"` Is the name of the S3 bucket you wish to backup to.
* `"bucket_path"` Is the "folder" that you wish files on S3 to be placed in (this is just prepended to the key on s3 and does not need to contain slashes)
* `"aws_credentials"` should either contain both the  `"api_key"` and `"secret_key"` to acces the bucket or not be set at all.
Any credentials in `"aws_credentials"` will always be used to access S3 over any other credentials passed. Note not every folder needs to use the same credentials.

###Arguments
A path to a config file can be passed via the `--config` argument

Two log are created `all.log` and `error.log` and similarly their location
can be set via `--errorlog` and `-alllog`.

By passing `-v` or `--verbose` the app will pass all messages to the console.
Alternatively `-a` or `--quiet` will make it pass nothing these arguments do not affect the log files which will always be written.

`--apikey` and `--secretkey` can be used to pass your AWS api credentials if none are passed aws configure credentials will be used and if specific creditals are set in the config file for folders they will always be used. If you are running for EC2 IAM roles can be used. 

### Backing Up
The above optional arguments relate to all commands and should be passed first then the command `upload` ie `-v --config "path to config file" upload -o`.

By default files are only uploaded to S3 is they are newer than the ones on S3. 
If you pass `-o` or `--overwrite` all files will be uploaded regardless of age.

### Restoring
Like with the `upload` command argumenrs like `-v` should be passed first then pass `restore "/path/to/file/or/folder"`, this will restore that file or folder to the latest version in S3.

`-c` or `--clean` can be passed to remove all files and folders in path passed path. This is currently only supported if you do not have ignored folders in the config for that folder.

`--timestamp` along with a unix timestamp can be passed to restore files back to that time and date. 

##Road Map
* Glacier support
* Custom Lifecycle rules
* File Compression
* File Encryption

##Pull Requests
PR's are welcome espcially to add more unit and integration tests but for features please open an issue and check it with us first.