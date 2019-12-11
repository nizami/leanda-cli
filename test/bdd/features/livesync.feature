Feature: Sync Leanda and local folder

Scenario: Sync current folders
   Given I want to sync folders
    When I run the command
    Then I get folders synced

Scenario: Sync current folder and remote identifyed by full id
   Given I want to sync folders
     And set remote folder full id
    When I run the command
    Then I get folders synced

Scenario: Sync current folder and remote identifyed by part id
   Given I want to sync folders
     And set remote folder part id
    When I run the command
    Then I get folders synced

Scenario: Sync current folder and remote identifyed by name
   Given I want to sync folders
     And set remote folder name
    When I run the command
    Then I get folders synced

Scenario: Sync not existed local folder and remote identifyed by full id
   Given I want to sync folders
     And set not existed local folder path
     And set remote folder full id     
    When I run the command
    Then I get folders synced

Scenario: Sync existed local folder and remote identifyed by part id
   Given I want to sync folders
     And set existed local folder path
     And set remote folder part id     
    When I run the command
    Then I get folders synced

Scenario: Sync existed local folder and remote identifyed by part id. Some of local files already exist
   Given I want to sync folders
     And set existed local folder path
     And set remote folder part id     
     And some of local files already exist
    When I run the command
    Then I get folders synced
     But files with same names scipped

Scenario: Sync existed local folder and remote identifyed by part id. Some of local and remote files already exist
   Given I want to sync folders
     And set existed local folder path
     And set remote folder part id     
     And some of local files already exist
    When I run the command
    Then I get folders synced
     But files with same names scipped

Scenario: Sync existed local folder and remote identifyed by part id. Some of remote files already exist
   Given I want to sync folders
     And set existed local folder path
     And set remote folder part id     
     And some of local files already exist
    When I run the command
    Then I get folders synced
     But files with same names scipped


Scenario: Force sync existed local folder and remote identifyed by part id. Some of local files already exist
   Given I want to sync folders
     And set existed local folder path
     And set remote folder part id     
     And some of local files already exist
    When I run the command
    Then I get folders synced
     But files with same names scipped


Scenario: Force sync existed local folder and remote identifyed by part id. Some of local and remote files already exist
   Given I want to sync folders
     And set existed local folder path
     And set remote folder part id     
     And some of local files already exist
     And set force replace local files
    When I run the command
    Then I get folders synced
     And files with same names in local folder replaced


Scenario: Force sync existed local folder and remote identifyed by part id. Some of remote files already exist
   Given I want to sync folders
     And set existed local folder path
     And set remote folder part id     
     And some of local files already exist
     And set force replace remote files
    When I run the command
    Then I get folders synced
     And files with same names in remote folder replaced


Scenario: Sync current folder and not existed remote identifyed by full id
   Given I want to sync folders
     And set remote folder identifyed by full id which not exists
    When I run the command
    Then I get error

Scenario: Sync current folder and not existed remote identifyed by part id
   Given I want to sync folders
     And set remote folder identifyed by part id which not exists
    When I run the command
    Then I get error

Scenario: Sync current folder and not existed remote identifyed by part name
   Given I want to sync folders
     And set remote folder identifyed by part name which not exists
    When I run the command
    Then I get error


Scenario: Sync current folder and remote ambiguously identifyed by part name
   Given I want to sync folders
     And set remote folder ambiguously identifyed by part name
    When I run the command
    Then I get error

Scenario: Sync current folder and remote ambiguously identifyed by part id
   Given I want to sync folders
     And set remote folder ambiguously identifyed by part id
    When I run the command
    Then I get error


Scenario: Sync current folder and remote item(but not folder) identifyed by full id
   Given I want to sync folders
     And set remote not folder identifyed by full id
    When I run the command
    Then I get error

# RECORDSETS          
# name: livesync
#   help: >
#       Two-way synchronization of local folder
#       with the Leanda user's folder. Comparision between
#       folders based on file names. For more precise
#       comparision see -ul and -ur keys.
#   params:
#       -
#           names:
#               - -l
#               - --local-folder
#           default: .
#           dest: folder
#           help: >
#                Path to local folder or
#                none for working directory
#       -
#           names:
#               - -r
#               - --remote-folder
#           dest: container
#           default: .
#           help: >
#                 Remote Leanda user's folder
#                 or none for current working folder.
#                 Leanda user's folder can be choosed by its
#                 full id system wide or by substring for
#                 subfolders in current folder.
#                 Substring compared to folder name starting
#                 from the beggining or to folder id ending.
#       -
#           names:
#               - -ul
#               - --update-local
#           action: store_true
#           help: Compare by name and Leanda file's version
#       -
#           names:
#               - -ur
#               - --update-remote
#           action: store_true
#           help: Compare by name and last modification time.