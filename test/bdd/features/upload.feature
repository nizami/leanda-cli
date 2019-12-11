#PREREQUISITES
# - logged in
# - any file
#  to mkmodel
    # - sdf file
    # - json meta for sdf file
    # - yaml meta for sdf file
# do cleanup after Scenario
Feature: Upload Leanda files


Scenario: Upload the file to remote cwd
   Given I want to upload the file
     And set the path to file
    When I run the command
    Then I have a new file in the remote cwd
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size

Scenario: Upload the file to remote cwd with the new filename 
   Given I want to upload the file
     And set the path to file
     And set new filename
    When I run the command
    Then I have a new file in the remote cwd
     And the local file size is equal to the remote file size

Scenario: Upload the set of files with new names to remote cwd
   Given I want to upload a set of files
         | path            | name         |   
         |folder/filename  | newfilename  |
         |folder/filename2 |              |
         |folder/filename3 | newfilename3 |
    When I run the command
    Then I have new files in the remote cwd
     And every the local file size in set is equal to matching remote file size


Scenario: Upload the file to foder in remote cwd defined by beginning of its name 
   Given I want to upload the file
     And choose desired folder in cwd by the beginning of its name
     And set the path to file
    When I run the command
    Then I have a new file in the desired folder
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size


Scenario: Upload the file to foder in remote cwd defined by the ending of its id
   Given I want to upload the file
     And choose desired folder in cwd by the ending of its id
     And set the path to file
    When I run the command
    Then I have a new file in the desired folder
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size


Scenario: Upload the file to any  remote folder defined by its full id
   Given I want to upload the file
     And choose desired folder by its full id
     And set the path to file
    When I run the command
    Then I have a new file in the desired folder
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size


Scenario: Upload the not existed file to remote cwd
   Given I want to upload the file
     And set the path to not existed file
    When I run the command
    Then I get error message

Scenario: Upload the file to not existed remote working directory
   Given I want to upload the file
     And set the path to file
     And choose not existed folder by its full id     
    When I run the command
    Then I get error message



Scenario: Upload the file to not unique identified folder 
   Given I want to upload the file
     And choose not unique identified folder in cwd by the beginning of its name
     And set the path to file
    When I run the command
    Then I get error message

#     names:
#         - container
#     default: .
#     nargs: '?'
# -
#     names:
#         - -p
#         - --path
#     dest: file
#     action: append
#     required: True
#     help: Local file path
# -
#     names:
#         - -n
#         - --name
#     action: append
#     help: Name Leanda file
# -
#     names:
#         - -m
#         - --meta
#     help: Model metadata in json or yaml formats