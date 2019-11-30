# OSDR-Cli

OSDR Command Line Interface (CLI) is intended for installation on users computers and will serve as another "client" for OSDR platform.

## Quickstart

You will need Python 2.7 to get started, so be sure to have an up-to-date Python 2.x installation.
Osdr-cli and its dependencies support Python 3. You could start using Python 3, but there are a few things to be aware of.
You need to use Python 3.6 or higher. Older versions are not supported.  You’ll probably want to use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
You should define environment variables (or default values will be used):
```
WEB_API_URL = 'https://api.dev.dataledger.io/osdr/v1/api'
IDENTITY_SERVER_URL = 'https://id.your-company.com/auth/realms/OSDR'
```

```terminal
git clone https://github.com/<this-repository>/osdr-cli.git
cd osdr-cli
pip install -r requirements.txt
python osdr.py --help
```

If you don't have pip installed try

```terminal
python -m pip install -r requirements.txt
```


## Commands Summary

|Command| Usage|
| ----- | ---------- |
|`osdr.py` [`login`](#login)| Allows to login and store the update sesion information for an OSDR user.|
|`osdr.py` [`whoami`](#whoami)| Check athorization and explore session data.|
|`osdr.py` [`logout`](#logout)| Do logout. Session data is removed.|
|`osdr.py` [`pwd`](#pwd)| Identify current OSDR working directory.|
|`osdr.py` [`cd`](#cd)| Change OSDR's current working directory.|
|`osdr.py` [`ls`](#ls)| Browse remote OSDR folder. |
|`osdr.py` [`rm`](#rm)| Allows to remove file or folder. |
|`osdr.py` [`upload`](#upload)| Allows uploading a local file into the BLOB (raw file) store.|
|`osdr.py` [`download`](#download)| Allows to download an OSDR file.|
|`osdr.py` [`livesync`](#livesync)| Two-way synchronization of local folder with the OSDR user's folder. |
|`osdr.py` [`items`](#items)| Allows to list all items from OSDR using queries. |
|`osdr.py` [`models`](#models)| Allows to list models from OSDR using queries. |
|`osdr.py` [`recordsets`](#recordsets)| Allows to list recordsets from OSDR using queries. |
|`osdr.py` [`train`](#train)| Allows to run Machine Learning command train. |
|`osdr.py` [`predict`](#predict)| Allows to run Machine Learning command predict. |
|`osdr.py` [`categories`](#categories)| Allows to initialize category tree with basic structure. |


## login

Allows to login and reset sesion information for an OSDR user.

### Parameters for `login`

```terminal
-u, --username   your osdr username.
-p, --password   your osdr password
-v, --verbosity  set verbosity level.
```

Examples:

```terminal
$ osdr.py login -u<user-name> -p<password>
$ osdr.py login --verbosity -u<user-name> -p<password>
$ osdr.py login -v -u<user-name> -p<password>
$ osdr.py login -vv -u<user-name> -p<password>
$ osdr.py login -u<user-name> -p
Password:
```

## whoami

Check athorization and explore session data.

### Parameters for `whoami`

```terminal
-v, --verbosity  set verbosity level.
```

Examples:

```terminal
osdr.py whoami --verbosity
osdr.py whoami -vv
osdr.py whoami -vvv
```

## logout

Do logout. Session data is removed.

### Parameters for `logout`

No parameters

Examples:

```terminal
osdr.py logout
```

## pwd

Identify current OSDR working directory.

### Parameters for `pwd`

```terminal
-v, --verbosity  set verbosity level.
```

Examples:

```terminal
osdr.py pwd
osdr.py pwd --verbosity
osdr.py pwd -vv
osdr.py pwd -vvv
```

## ls

Browse remote OSDR folder.

### Parameters for `ls`

```terminal
container - Remote OSDR user's folder or none for current working folder.
            OSDR user's folder can be choosed by its full id system wide
            or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
-s, --size - Report page length (default value 10)
-p, --page - Report page number (default value 1)
```

Examples:

```terminal
osdr.py ls c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
osdr.py ls 2e01
osdr.py ls -p10
osdr.py ls -s20 -2
```

## cd

Change OSDR's current working directory.

### Parameters for `cd`

```terminal
container - Remote OSDR user's folder, none for home  folder or '..' for
            parent folder. OSDR user's folder can be choosed by its full id
            system wide or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
```

Examples:

```terminal
$ osdr.py ls
File
    33.mol               Records(  1) Processed  c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
    combined lysomotroph Records( 55) Processed  00160000-ac12-0242-c20e-08d56e29a481

$ osdr.py cd 33
$ osdr.py cd a481
$ osdr.py cd
$ osdr.py cd ..
$ osdr.py cd c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
```

## rm

Allows to remove file or folder

### Parameters for `rm`

```terminal
container - Remote OSDR user's folder. OSDR user's folder can be choosed by
            its full id  system wide or by substring for subfolders in current
            folder. Substring compared to folder name starting from the beggining
            or to folder id ending.
```

Examples:

```terminal
osdr.py rm a481
osdr.py rm abc
osdr.py rm c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
```

## upload

Allows uploading a local file into the BLOB (raw file) store.

### Parameters for `upload`

```terminal
container - Remote OSDR user's folder, none for working folder.
            OSDR user's folder can be choosed by its full id system wide
            or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
-p, --path - path to local file
-n, --name - name for file
-m, --meta - path to model description in json or yaml formats
-v, --verbosity  set verbosity level.
```

Examples:

```terminal
osdr.py upload -p path-to-file
osdr.py upload -p path-to-file1 -p path-to-file2 -p path-to-file3
osdr.py upload -p path-to-file -n new-name to file 'filename'
osdr.py upload -p path-to-file -m path-to-model.json
osdr.py upload -p path-to-file -m path-to-model.yaml
```

## download

Allows downloading a remote file to local host.

### Parameters for `download`

```terminal
container - Remote OSDR user's folder, none for working folder.
            OSDR user's folder can be choosed by its full id system wide
            or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
-o, --output - Path to file or directory to save.
-f, --force - Force overwrite if file exists.
```

Examples:

```terminal
osdr.py upload abc -o path-to-file
osdr.py upload a481 -f -o path-to-file1
osdr.py upload c1cc0000-5d8b-0015-e9e3-08d56a8a2e01 -o path-to-file
```

## livesync

Two-way synchronization of local folder with the OSDR user's folder. Comparision between folders based on file names. For more precise comparision see -ul and -ur keys.

```terminal
 -l, --local-folder - Path to local folder or none for current working directory
 -r, --remote-folder - Remote OSDR user's folder or none for current working folder.
                       OSDR user's folder can be choosed by its full id system wide
                       or by substring for subfolders in current folder. Substring
                       compared to folder name starting from the begining or to
                       folder id ending.
 -ul, --update-local - Compare by name and OSDR file's version
 -ur, --update-remote - Compare by name and last modification time.

```

Examples:

```terminal
osdr.py livesync -l abc -r c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
osdr.py livesync -l /path/to/folder -f -r 2e01 -ul
osdr.py livesync -ur
```

## items
Allows to list all items from OSDR using queries.

```terminal
  -q, --query - Filter models by subquery
  -n, --name  - Filter models by substring
  -s, --short-notation
              - Path to yaml file with list of short notations
                Example - p.radius:MachineLearningModelInfo.Fingerprints.Radius
  -v,--verbosity = 0 
              - Set verbosity level. 
                -v - display query string,
                -vv - display records,
   -f, --format = (json|yaml)
              - Set model verbosity output format
```

Examples:

```terminal
osdr.py items 
osdr.py items -v
osdr.py items -vv
osdr.py items -n png
osdr.py items -q "SubType eq 'Model' and MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
osdr.py items -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
osdr.py items -q "SubType eq 'Model' and MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml
```



## models
Allows to list models from OSDR using queries. Same as `items`, but add preset filter `SubType eq 'Model'`

Examples:

```terminal
osdr.py models 
osdr.py models -v
osdr.py models -vv
osdr.py items -n ada
osdr.py models -q "MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
osdr.py models -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
osdr.py models -q "MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml

```



## recordsets
Allows to list recordsets from OSDR using queries. Same as `items`, but add preset filter `SubType eq 'Records'`

Examples:

```terminal
osdr.py recordsets 
osdr.py recordsets -v
osdr.py recordsets -vv
osdr.py recordsets -n combined
osdr.py recordsets -q "MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
osdr.py recordsets -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
osdr.py recordsets -q "MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml

```



## train
Allows to run Machine Learning command train.

```terminal
  container - Remote OSDR user's folder, none for working folder.
              OSDR user's folder can be choosed by its full id system wide
              or by substring for subfolders in current folder.
              Substring compared to folder name starting from the beggining
              or to folder id ending.
  -m, --meta - Model metadata in json or yaml formats
  -f, --folder-name - Output folder name

```

Examples:

```terminal
osdr.py train 00130000-ac12-0242-0f11-08d58dbc7b8b  -f test1.model -m sample_files/train_sdf_model.yaml 
osdr.py train 08d58dbc7b8b  -f test2.model -m sample_files/train_sdf_model.yaml 
osdr.py train b data_solubility.sdf -f test3.model -m sample_files/train_sdf_model.yaml 
osdr.py train data_solubility.sdf -f test4.model -m sample_files/train_sdf_model.yaml 
osdr.py train data_solu -f test5.model -m sample_files/train_sdf_model.yaml 
```



## predict
Allows to run Machine Learning command predict.

```terminal
 -f - --folder-name - Output folder name
 -m - --model - OSDR model's file id.
 -r - --recordset - OSDR recordsets's file id.
```

Examples:

```terminal
osdr.py predict -f folder.predict -m 7ceef61a-cf7d-41d9-a1f0-19874a2b31e9 -r 000e0000-ac12-0242-36bb-08d585329c5a

```

## categories
Allows to initialize category tree with basic structure.

Examples:

```terminal
osdr.py categories

```
