# Leanda-CLI

Leanda Command Line Interface (CLI) is intended for installation on users computers and will serve as another "client" for Leanda platform.

## Quickstart

Install leanda-cli via pip:

```bash
pip install leanda
```

Run help command for installation test:

```bash
leanda --help
```

For the next commands you need to set the next environment variables or it will set as default dev env if ommited:

`LEANDA_WEB_CORE_API_URL`

`LEANDA_WEB_BLOB_API_URL`

`LEANDA_WEB_SOCKET_URL`

`LEANDA_IDENTITY_SERVER_URL`

`LEANDA_FILE_UPLOAD_LIMIT`

`LEANDA_FILE_DOWNLOAD_LIMIT`

Login to Leanda:

```bash
leanda login -u my_name -p my_password

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
| `leanda` [`upload`](#upload)         | Upload local direcory or file list to remote folder.                         |
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
```

Examples:

```bash
leanda login -u<user-name> -p<password>
```

## whoami

Check authorization and explore user data.

Examples:

```bash
leanda whoami
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

Examples:

```bash
leanda rm c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
```

## upload

Upload local direcory or file list to remote folder.

Examples:

```bash
leanda upload -r c1cc0000-5d8b-0015-e9e3-08d56a8a2e01 -l local_folder
leanda upload -l local_folder
```

## download

Download remote folder or file list to local directory.

Examples:

```bash
leanda download -r c1cc0000-5d8b-0015-e9e3-08d56a8a2e01 -l local_folder
leanda download -l local_folder
```

## livesync

Sync local direcory with remote folder.

Examples:

```bash
leanda livesync -l abc -r c1cc0000-5d8b-0015-e9e3-08d56a8a2e01
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

### Install as package

```bash
pip install --editable .
```

### Use as terminal tool

```bash
leanda --help
```
