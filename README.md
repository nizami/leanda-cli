# Leanda-Cli

Leanda Command Line Interface (CLI) is intended for installation on users computers and will serve as another "client" for Leanda platform.

## Quickstart

You will need Python 2.7 to get started, so be sure to have an up-to-date Python 2.x installation.
Osdr-cli and its dependencies support Python 3. You could start using Python 3, but there are a few things to be aware of.
You need to use Python 3.6 or higher. Older versions are not supported.  You’ll probably want to use [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
You should define environment variables (or default values will be used):

```bash
WEB_API_URL = 'https://api.dev.dataledger.io/osdr/v1/api'
IDENTITY_SERVER_URL = 'https://id.your-company.com/auth/realms/Leanda'
```

```terminal
git clone https://github.com/<this-repository>/leanda-cli.git
cd leanda-cli
pip install -r requirements.txt
python leanda.py --help
```

If you don't have pip installed try

```terminal
python -m pip install -r requirements.txt
```

## Commands Summary

|Command| Usage|
| ----- | ---------- |
|`leanda.py` [`login`](#login)| Allows to login and store the update session information for an Leanda user.|
|`leanda.py` [`whoami`](#whoami)| Check authorization and explore session data.|
|`leanda.py` [`logout`](#logout)| Do logout. Session data is removed.|
|`leanda.py` [`pwd`](#pwd)| Identify current Leanda working directory.|
|`leanda.py` [`cd`](#cd)| Change Leanda's current working directory.|
|`leanda.py` [`ls`](#ls)| Browse remote Leanda folder. |
|`leanda.py` [`rm`](#rm)| Allows to remove file or folder. |
|`leanda.py` [`upload`](#upload)| Allows uploading a local file into the BLOB (raw file) store.|
|`leanda.py` [`download`](#download)| Allows to download an Leanda file.|
|`leanda.py` [`livesync`](#livesync)| Two-way synchronization of local folder with the Leanda user's folder. |
|`leanda.py` [`items`](#items)| Allows to list all items from Leanda using queries. |
|`leanda.py` [`models`](#models)| Allows to list models from Leanda using queries. |
|`leanda.py` [`recordsets`](#recordsets)| Allows to list recordsets from Leanda using queries. |
|`leanda.py` [`train`](#train)| Allows to run Machine Learning command train. |
|`leanda.py` [`predict`](#predict)| Allows to run Machine Learning command predict. |
|`leanda.py` [`categories`](#categories)| Allows to initialize category tree with basic structure. |

## login

Allows to login and reset session information for an Leanda user.

### Parameters for `login`

```terminal
-u, --username   your leanda username.
-p, --password   your leanda password
-v, --verbosity  set verbosity level.
```

Examples:

```terminal
$ leanda.py login -u<user-name> -p<password>
$ leanda.py login --verbosity -u<user-name> -p<password>
$ leanda.py login -v -u<user-name> -p<password>
$ leanda.py login -vv -u<user-name> -p<password>
$ leanda.py login -u<user-name> -p
Password:
```

## whoami

Check authorization and explore session data.

### Parameters for `whoami`

```terminal
-v, --verbosity  set verbosity level.
```

Examples:

```terminal
leanda.py whoami --verbosity
leanda.py whoami -vv
leanda.py whoami -vvv
```

## logout

Do logout. Session data is removed.

### Parameters for `logout`

No parameters

Examples:

```terminal
leanda.py logout
```

## pwd

Identify current Leanda working directory.

### Parameters for `pwd`

```terminal
-v, --verbosity  set verbosity level.
```

Examples:

```terminal
leanda.py pwd
leanda.py pwd --verbosity
leanda.py pwd -vv
leanda.py pwd -vvv
```

## ls

Browse remote Leanda folder.

### Parameters for `ls`

```terminal
container - Remote Leanda user's folder or none for current working folder.
            Leanda user's folder can be choosed by its full id system wide
            or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
-s, --size - Report page length (default value 10)
-p, --page - Report page number (default value 1)
```

Examples:

```terminal
leanda.py ls c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
leanda.py ls 2e01
leanda.py ls -p10
leanda.py ls -s20 -2
```

## cd

Change Leanda's current working directory.

### Parameters for `cd`

```terminal
container - Remote Leanda user's folder, none for home  folder or '..' for
            parent folder. Leanda user's folder can be choosed by its full id
            system wide or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
```

Examples:

```terminal
$ leanda.py ls
File
    33.mol               Records(  1) Processed  c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
    combined lysomotroph Records( 55) Processed  00160000-ac12-0242-c20e-08d56e29a481

$ leanda.py cd 33
$ leanda.py cd a481
$ leanda.py cd
$ leanda.py cd ..
$ leanda.py cd c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
```

## rm

Allows to remove file or folder

### Parameters for `rm`

```terminal
container - Remote Leanda user's folder. Leanda user's folder can be choosed by
            its full id  system wide or by substring for subfolders in current
            folder. Substring compared to folder name starting from the beggining
            or to folder id ending.
```

Examples:

```terminal
leanda.py rm a481
leanda.py rm abc
leanda.py rm c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
```

## upload

Allows uploading a local file into the BLOB (raw file) store.

### Parameters for `upload`

```terminal
container - Remote Leanda user's folder, none for working folder.
            Leanda user's folder can be choosed by its full id system wide
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
leanda.py upload -p path-to-file
leanda.py upload -p path-to-file1 -p path-to-file2 -p path-to-file3
leanda.py upload -p path-to-file -n new-name to file 'filename'
leanda.py upload -p path-to-file -m path-to-model.json
leanda.py upload -p path-to-file -m path-to-model.yaml
```

## download

Allows downloading a remote file to local host.

### Parameters for `download`

```terminal
container - Remote Leanda user's folder, none for working folder.
            Leanda user's folder can be choosed by its full id system wide
            or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
-o, --output - Path to file or directory to save.
-f, --force - Force overwrite if file exists.
```

Examples:

```terminal
leanda.py upload abc -o path-to-file
leanda.py upload a481 -f -o path-to-file1
leanda.py upload c1cc0000-5d8b-0015-e9e3-08d56a8a2e01 -o path-to-file
```

## livesync

Two-way synchronization of local folder with the Leanda user's folder. Comparision between folders based on file names. For more precise comparision see -ul and -ur keys.

```terminal
 -l, --local-folder - Path to local folder or none for current working directory
 -r, --remote-folder - Remote Leanda user's folder or none for current working folder.
                       Leanda user's folder can be choosed by its full id system wide
                       or by substring for subfolders in current folder. Substring
                       compared to folder name starting from the begining or to
                       folder id ending.
 -ul, --update-local - Compare by name and Leanda file's version
 -ur, --update-remote - Compare by name and last modification time.

```

Examples:

```terminal
leanda.py livesync -l abc -r c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
leanda.py livesync -l /path/to/folder -f -r 2e01 -ul
leanda.py livesync -ur
```

## items

Allows to list all items from Leanda using queries.

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
leanda.py items 
leanda.py items -v
leanda.py items -vv
leanda.py items -n png
leanda.py items -q "SubType eq 'Model' and MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
leanda.py items -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
leanda.py items -q "SubType eq 'Model' and MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml
```

## models

Allows to list models from Leanda using queries. Same as `items`, but add preset filter `SubType eq 'Model'`

Examples:

```terminal
leanda.py models 
leanda.py models -v
leanda.py models -vv
leanda.py items -n ada
leanda.py models -q "MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
leanda.py models -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
leanda.py models -q "MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml

```

## recordsets

Allows to list recordsets from Leanda using queries. Same as `items`, but add preset filter `SubType eq 'Records'`

Examples:

```terminal
leanda.py recordsets 
leanda.py recordsets -v
leanda.py recordsets -vv
leanda.py recordsets -n combined
leanda.py recordsets -q "MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
leanda.py recordsets -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
leanda.py recordsets -q "MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml

```

## train

Allows to run Machine Learning command train.

```terminal
  container - Remote Leanda user's folder, none for working folder.
              Leanda user's folder can be choosed by its full id system wide
              or by substring for subfolders in current folder.
              Substring compared to folder name starting from the beggining
              or to folder id ending.
  -m, --meta - Model metadata in json or yaml formats
  -f, --folder-name - Output folder name

```

Examples:

```terminal
leanda.py train 00130000-ac12-0242-0f11-08d58dbc7b8b  -f test1.model -m sample_files/train_sdf_model.yaml 
leanda.py train 08d58dbc7b8b  -f test2.model -m sample_files/train_sdf_model.yaml 
leanda.py train b data_solubility.sdf -f test3.model -m sample_files/train_sdf_model.yaml 
leanda.py train data_solubility.sdf -f test4.model -m sample_files/train_sdf_model.yaml 
leanda.py train data_solu -f test5.model -m sample_files/train_sdf_model.yaml 
```

## predict

Allows to run Machine Learning command predict.

```terminal
 -f - --folder-name - Output folder name
 -m - --model - Leanda model's file id.
 -r - --recordset - Leanda recordsets's file id.
```

Examples:

```terminal
leanda.py predict -f folder.predict -m 7ceef61a-cf7d-41d9-a1f0-19874a2b31e9 -r 000e0000-ac12-0242-36bb-08d585329c5a

```

## categories

Allows to initialize category tree with basic structure.

Examples:

```terminal
leanda.py categories

```
