#PREREQUISITES
# - logged in
# - the file in leanda cwd
# - the other file in leanda cwd with the name mathing the beginnig previous file
Feature: Download an Leanda file

Scenario: Download by the beginning of the filename
   Given I want to download the file
     And know the beginning of the filename in the remote cwd
    When I run the command
    Then I have a new file in the local cwd
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size

Scenario: Download by the ending of the file id
   Given I want to download the file
     And know the ending of the file id in the remote cwd
    When I run the command
    Then I have a new file in the local cwd
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size

Scenario: Download by the full file id
   Given I want to download the file
     And know the full remote file id
     But the file is not in the remote cwd
    When I run the command
    Then I have a new file in the local cwd
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size

Scenario: Download the file and save it with different filename to local cwd
   Given I want to download the file
     And know the beginning of the filename in the remote cwd
     And want to save it with different filename to local cwd
    When I run the command
    Then I have a new file in the local cwd
     And its filename different to remote filename
     And the local file size is equal to the remote file size

Scenario: Download the file and save it to folder other then local cwd
   Given I want to download the file
     And know the beginning of the filename in the remote cwd
     And want to save it to folder other then local cwd
    When I run the command
    Then I have a new file in the folder other then local cwd
     And the local file size is equal to the remote file size

Scenario: Download the file already existed in local cwd
   Given I want to download the file
     And know the beginning of the filename in the remote cwd
     And file with same name already existed in local cwd
    When I run the command
    Then I get an error

Scenario: Force download the file already existed in local cwd
   Given I want to download the file
     And know the beginning of the filename in the remote cwd
     And file with same name already existed in local cwd
     And existed file will be replaced with new one
    When I run the command
    Then I have the file in the local cwd
     And the local filename is equal to the remote filename
     And the local file size is equal to the remote file size

Scenario: Download by the not unique beginning of the filename
   Given I want to download the file
     And I know the beginning of the filename in the remote cwd
     But the beginning of the filename is math with the beginning of the other filename
    When I run the command
    Then I get an error

Scenario: Download by the wrong beginning of the filename
   Given I want to download the file
     And give wrong beginning of the filename
    When I run the command
    Then I get an error

Scenario: Download by the wrong ending of the file id
   Given I want to download the file
     And give wrong ending of the file id
    When I run the command
    Then I get an error

Scenario: Download by the wrong full file id
   Given I want to download the file
     And give wrong full file id
    When I run the command
    Then I get an error

Scenario: Download not a file
   Given I want to download the file
     And give not a file full id
    When I run the command
    Then I get an error

