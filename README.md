# Leanda-CLI

Leanda Command Line Interface (CLI) is intended for installation on users computers and will serve as another "client" for Leanda platform.

## Quickstart

Install leanda-cli via pip:

```bash
pip install leanda
```

Run help command:

```bash
leanda --help
```

For the next commands you need to set the next environment variables or will set for dev env if ommited:

`LEANDA_WEB_CORE_API_URL`

`LEANDA_WEB_BLOB_API_URL`

`LEANDA_IDENTITY_SERVER_URL`

Login to Leanda:

```bash
leanda login -u my_name -p my_password

```

Get categories list:

```bash
leanda categories
```

Run livesync command:

```bash
leanda livesync -l ./leanda-sync-folder
```

`./leanda-sync-folder` is a local folder path.

## Commands Summary

| Command                              | Usage                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| `leanda` [`login`](#login)           | Allows to login and store the update session information for an Leanda user. |
| `leanda` [`whoami`](#whoami)         | Check authorization and explore session data.                                |
| `leanda` [`logout`](#logout)         | Do logout. Session data is removed.                                          |
| `leanda` [`pwd`](#pwd)               | Identify current Leanda working directory.                                   |
| `leanda` [`cd`](#cd)                 | Change Leanda's current working directory.                                   |
| `leanda` [`ls`](#ls)                 | Browse remote Leanda folder.                                                 |
| `leanda` [`rm`](#rm)                 | Allows to remove file or folder.                                             |
| `leanda` [`upload`](#upload)         | Allows uploading a local file into the BLOB (raw file) store.                |
| `leanda` [`download`](#download)     | Allows to download an Leanda file.                                           |
| `leanda` [`livesync`](#livesync)     | Two-way synchronization of local folder with the Leanda user's folder.       |
| `leanda` [`items`](#items)           | Allows to list all items from Leanda using queries.                          |
| `leanda` [`models`](#models)         | Allows to list models from Leanda using queries.                             |
| `leanda` [`recordsets`](#recordsets) | Allows to list recordsets from Leanda using queries.                         |
| `leanda` [`train`](#train)           | Allows to run Machine Learning command train.                                |
| `leanda` [`predict`](#predict)       | Allows to run Machine Learning command predict.                              |
| `leanda` [`categories`](#categories) | Allows to initialize category tree with basic structure.                     |

## login

Allows to login and reset session information for an Leanda user.

### Parameters for `login`

```bash
-u, --username   your leanda username.
-p, --password   your leanda password
-v, --verbosity  set verbosity level.
```

Examples:

```bash
leanda login -u<user-name> -p<password>
leanda login --verbosity -u<user-name> -p<password>
leanda login -v -u<user-name> -p<password>
leanda login -vv -u<user-name> -p<password>
leanda login -u<user-name> -p
Password:
```

## whoami

Check authorization and explore session data.

### Parameters for `whoami`

```bash
-v, --verbosity  set verbosity level.
```

Examples:

```bash
leanda whoami --verbosity
leanda whoami -vv
leanda whoami -vvv
```

## logout

Do logout. Session data is removed.

### Parameters for `logout`

No parameters

Examples:

```bash
leanda logout
```

## pwd

Identify current Leanda working directory.

### Parameters for `pwd`

```bash
-v, --verbosity  set verbosity level.
```

Examples:

```bash
leanda pwd
leanda pwd --verbosity
leanda pwd -vv
leanda pwd -vvv
```

## ls

Browse remote Leanda folder.

### Parameters for `ls`

```bash
container - Remote Leanda user's folder or none for current working folder.
            Leanda user's folder can be choosed by its full id system wide
            or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
-s, --size - Report page length (default value 10)
-p, --page - Report page number (default value 1)
```

Examples:

```bash
leanda ls c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
leanda ls 2e01
leanda ls -p10
leanda ls -s20 -2
```

## cd

Change Leanda's current working directory.

### Parameters for `cd`

```bash
container - Remote Leanda user's folder, none for home  folder or '..' for
            parent folder. Leanda user's folder can be choosed by its full id
            system wide or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
```

Examples:

```bash
leanda ls
File
    33.mol               Records(  1) Processed  c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
    combined lysomotroph Records( 55) Processed  00160000-ac12-0242-c20e-08d56e29a481

leanda cd 33
leanda cd a481
leanda cd
leanda cd ..
leanda cd c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
```

## rm

Allows to remove file or folder

### Parameters for `rm`

```bash
container - Remote Leanda user's folder. Leanda user's folder can be choosed by
            its full id  system wide or by substring for subfolders in current
            folder. Substring compared to folder name starting from the beggining
            or to folder id ending.
```

Examples:

```bash
leanda rm a481
leanda rm abc
leanda rm c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
```

## upload

Allows uploading a local file into the BLOB (raw file) store.

### Parameters for `upload`

```bash
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

```bash
leanda upload -p path-to-file
leanda upload -p path-to-file1 -p path-to-file2 -p path-to-file3
leanda upload -p path-to-file -n new-name to file 'filename'
leanda upload -p path-to-file -m path-to-model.json
leanda upload -p path-to-file -m path-to-model.yaml
```

## download

Allows downloading a remote file to local host.

### Parameters for `download`

```bash
container - Remote Leanda user's folder, none for working folder.
            Leanda user's folder can be choosed by its full id system wide
            or by substring for subfolders in current folder.
            Substring compared to folder name starting from the beggining
            or to folder id ending.
-o, --output - Path to file or directory to save.
-f, --force - Force overwrite if file exists.
```

Examples:

```bash
leanda upload abc -o path-to-file
leanda upload a481 -f -o path-to-file1
leanda upload c1cc0000-5d8b-0015-e9e3-08d56a8a2e01 -o path-to-file
```

## livesync

Two-way synchronization of local folder with the Leanda user's folder. Comparision between folders based on file names. For more precise comparision see -ul and -ur keys.

```bash
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

```bash
leanda livesync -l abc -r c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
leanda livesync -l /path/to/folder -f -r 2e01 -ul
leanda livesync -ur
```

## items

Allows to list all items from Leanda using queries.

```bash
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

```bash
leanda items
leanda items -v
leanda items -vv
leanda items -n png
leanda items -q "SubType eq 'Model' and MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
leanda items -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
leanda items -q "SubType eq 'Model' and MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml
```

## models

Allows to list models from Leanda using queries. Same as `items`, but add preset filter `SubType eq 'Model'`

Examples:

```bash
leanda models
leanda models -v
leanda models -vv
leanda items -n ada
leanda models -q "MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
leanda models -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
leanda models -q "MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml

```

## recordsets

Allows to list recordsets from Leanda using queries. Same as `items`, but add preset filter `SubType eq 'Records'`

Examples:

```bash
leanda recordsets
leanda recordsets -v
leanda recordsets -vv
leanda recordsets -n combined
leanda recordsets -q "MachineLearningModelInfo.Method eq 'Naive Bayes'"  -vv -f json
leanda recordsets -q "type=Model,prop.chem=MOST_ABUNDANT_MASS,prop.fields=logs"  -s sample_files/short_notations.yaml
leanda recordsets -q "MachineLearningModelInfo.Fingerprints.Size gt 200"  -vv -f yaml

```

## train

Allows to run Machine Learning command train.

```bash
  container - Remote Leanda user's folder, none for working folder.
              Leanda user's folder can be choosed by its full id system wide
              or by substring for subfolders in current folder.
              Substring compared to folder name starting from the beggining
              or to folder id ending.
  -m, --meta - Model metadata in json or yaml formats
  -f, --folder-name - Output folder name

```

Examples:

```bash
leanda train 00130000-ac12-0242-0f11-08d58dbc7b8b  -f test1.model -m sample_files/train_sdf_model.yaml
leanda train 08d58dbc7b8b  -f test2.model -m sample_files/train_sdf_model.yaml
leanda train b data_solubility.sdf -f test3.model -m sample_files/train_sdf_model.yaml
leanda train data_solubility.sdf -f test4.model -m sample_files/train_sdf_model.yaml
leanda train data_solu -f test5.model -m sample_files/train_sdf_model.yaml
```

## predict

Allows to run Machine Learning command predict.

```bash
 -f - --folder-name - Output folder name
 -m - --model - Leanda model's file id.
 -r - --recordset - Leanda recordsets's file id.
```

Examples:

```bash
leanda predict -f folder.predict -m 7ceef61a-cf7d-41d9-a1f0-19874a2b31e9 -r 000e0000-ac12-0242-36bb-08d585329c5a

```

## categories

Allows to initialize category tree with basic structure.

```bash
  -rm, --remove - Remove all categories
  -i, --init    - Initialize categories from categories.json file data
```

Examples:

```bash
leanda categories #get list of categories
leanda categories -rm
leanda categories -i

```

## Development

### Install virtualenv

```bash
pip install virtualenv --user
```

### Create virtual environment

```bash
virtualenv venv
```

### Activate virtualenv

```bash
# on Mac OS X or Linux
. venv/bin/activate

# on Windows
venv\scripts\activate
```

### Install package

```bash
pip install --editable .
```
