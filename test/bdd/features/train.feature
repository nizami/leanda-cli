#PREREQUISITES
# - logged in
# - remote SDF file
# - json meta for sdf file
# - yaml meta for sdf file
# do cleanup after Scenario
Feature: Train Leanda recordset


# container
Scenario: Train recordset choosed by full id
   Given I want to train recordset
     And set valid full id
     And set valid folder          
     And set valid metadata file
    When I run the command
    Then I get new folder

Scenario: Train recordset choosed by part id
   Given I want to train recordset
     And set valid part id
     And set valid folder          
     And set valid metadata file
    When I run the command
    Then I get new folder

Scenario: Train recordset choosed by part name
   Given I want to train recordset
     And set valid part name
     And set valid folder         
     And set valid metadata file
    When I run the command
    Then I get new folder

# meta
Scenario Outline: Train recordset with valid meta
   Given I want to train recordset
     And set valid full id
     And set valid <folder>          
     And set valid <metadata> file
    When I run the command
    Then I get <folder>

    Examples: Metadata files
     | metadata                      |  folder           |
     | sample_files/train_valid.json |  train_valid.json |
     | sample_files/train_valid.yaml |  train_valid.yaml |

Scenario Outline: Train recordset with invalid meta
   Given I want to train recordset
     And set valid full id
     And set valid folder          
     And set invalid <metadata> file
    When I run the command
    Then I get error message

    Examples: Metadata files
     | metadata                  |
     | sample_files/invalid.json |
     | sample_files/invalid.yaml |
     | any-file.txt              |


# errors
Scenario: Train recordset choosed by not existed full id
   Given I want to train recordset
     And set valid metadata
     And set valid folder     
     And set not existed full id
    When I run the command
    Then I get error message

Scenario: Train recordset choosed by not existed part id
   Given I want to train recordset
     And set valid metadata   
     And set valid folder          
     And set not existed part id
    When I run the command
    Then I get error message


Scenario: Train recordset choosed by not existed part name
   Given I want to train recordset
     And set valid metadata   
     And set valid folder          
     And set not existed part name
    When I run the command
    Then I get error message

Scenario: Train recordset choosed by not unique part name
   Given I want to train recordset
     And set valid metadata   
     And set valid folder          
     And set not unique part name
    When I run the command
    Then I get error message

Scenario: Train not an SDF based recordset
   Given I want to train recordset
     And set valid metadata   
     And set valid folder          
     And set not an SDF based recordset
    When I run the command
    Then I get error message

Scenario: Store trained models to existed folder
   Given I want to train recordset
     And set valid metadata   
     And set existed folder
    When I run the command
    Then I get error message



# params:
#     -
#         names:
#             - container
#         help: >
#               Remote Leanda SDF file id.
#               Leanda file can be choosed by its
#               full id system wide or by substring in
#               current Leanda folder.
#               Substring compared to filename starting
#               from the beggining or to file id ending.
#     -
#         names:
#             - -m
#             - --meta
#         dest: path
#         required: True
#         help: Model metadata in json or yaml formats
#     -
#         names:
#             - -f
#             - --folder-name
#         dest: name
#         help: Output folder name

# '''
