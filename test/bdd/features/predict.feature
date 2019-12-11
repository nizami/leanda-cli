#PREREQUISITES
# - logged in
Feature: Predict recordset with model


Scenario: Predict recordset with model
   Given I want to predict recordset
     And set folder name
     And set model full id
     And set recordset full id
    When I run the command
    Then I get success message

Scenario: Predict recordset with existed folder
   Given I want to predict recordset
     And set existing folder name
     And set model full id
     And set recordset full id
    When I run the command
    Then I get error message

Scenario: Predict recordset with not existed model
   Given I want to predict recordset
     And set folder name
     And set not existed model full id
     And set recordset full id
    When I run the command
    Then I get error message

Scenario: Predict recordset with not a model full id
   Given I want to predict recordset
     And set folder name
     And set model full id
     And set not recordset full id
    When I run the command
    Then I get error message


Scenario: Predict recordset with not existed recordset
   Given I want to predict recordset
     And set folder name   
     And set model full id
     And set not existed recordset full id
    When I run the command
    Then I get error message

Scenario: Predict recordset with not recordset full id
   Given I want to predict recordset
     And set folder name   
     And set model full id
     And set not recordset full id
    When I run the command
    Then I get error message




# names:
#     - -f
#     - --folder-name
# dest: folder
# required: True
# help: Output folder name
# -
# names:
#     - -m
#     - --model
# required: True
# help: Leanda model's file id.
# -
# names:
#     - -r
#     - --recordset
# required: True
# help: Leanda recordsets's file id.
# '''