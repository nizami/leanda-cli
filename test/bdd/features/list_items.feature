Feature: List Leanda wide items, recorsets and models

Scenario: List all items
   Given I want to list items
    When I run the command
    Then I get items list 

Scenario: List items filtered by valid name
   Given I want to list items
     And set valid name substring
    When I run the command
    Then I get items list meet the constraints

Scenario: List items filtered by valid natural notation query 
   Given I want to list items
     And set <natural> notation query 
    When I run the command
    Then I get items list meet the constraints

    Examples: Natural notation
    | natural                                                               |
    | subType eq 'Tabular'                                                  |
    | MachineLearningModelInfo.ClassName eq 'Soluble'                       |
    | subType eq 'Model' and MachineLearningModelInfo.ClassName eq 'Soluble'|

Scenario: List items filtered by valid natural notation query and by valid name 
   Given I want to list items
     And set valid name substring
     And set <natural> notation query      
    When I run the command
    Then I get items list meet the constraints

    Examples: Natural notation
    | natural                                                   |
    | subType eq 'Image'                                        |
    | MachineLearningModelInfo.ClassName eq 'Soluble'           |
    | subType eq 'Model' and MachineLearningModelInfo.KFold eq 2|

Scenario: List items filtered by valid short notation query
   Given I want to list items
     And set path to yaml file with short notations dictionary
     And set <short> notation query      
    When I run the command
    Then I get items list meet the constraints

    Examples: Short notation
    | short                   |
    | stype=Model, fp.size=256|
    | stype=Image             |
    | stype=Model, kfold=2    |



Scenario: List items filtered by valid short notation query and by valid name 
   Given I want to list items
     And set path to yaml file with short notations dictionary
     And set valid name substring
     And set <short> notation query      
    When I run the command
    Then I get items list meet the constraints

    Examples: Short notation
    | short                   |
    | stype=Model, fp.size=256|
    | stype=Tabular           |
    | stype=Model, kfold=2    |


# errors
Scenario: List items filtered by valid short notation query but without short notaion dictionary
   Given I want to list items
     And set <short> notation query      
    When I run the command
    Then I get error

    Examples: Short notation
    | short                   |
    | stype=Model, fp.size=256|
    | stype=Tabular           |
    | stype=Model, kfold=2    |


Scenario: List items filtered by not existed name
   Given I want to list items
     And set substring for existed name
    When I run the command
    Then I get an empty list

Scenario: List items filtered by not existed parameter value
   Given I want to list items
     And set natural query with not existed parameter value
    When I run the command
    Then I get an empty list

Scenario: List items filtered by not existed field
   Given I want to list items
     And set short query with not existed field
    When I run the command
    Then I get error message


Scenario: List items filtered by badly formed  natural query
   Given I want to list items
     And set badly formed  natural query
    When I run the command
    Then I get error message

Scenario: List items filtered by badly formed  short notation query
   Given I want to list items
     And set path to yaml file with short notations dictionary   
     And set badly formed  shoert notation query
    When I run the command
    Then I get error message

Scenario: List recordsets filtered by name
   Given I want to list recordsets
     And set valid name substring
    When I run the command
    Then I get recordsets list meet the constraints

Scenario: List models filtered by name
   Given I want to list models
     And set valid name substring
    When I run the command
    Then I get models list meet the constraints






# class ListItems(HandlerBase):
# class ListModels(ListItems):
# class ListRecordsets(ListItems):
#     """
#     Allows to list contents of Leanda using queries.
#     """
#     url = 'https://api.dataledger.io/osdr/v1/api/me'
#     info = '''
#             name: items
#             help: Allows to list contents of Leanda using queries.
#             params:
#                 -
#                     names:
#                         - -q
#                         - --query
#                     help: Filter models by subquery

#                 -
#                     names:
#                         - -n
#                         - --name
#                     help: Filter models by substring

#                 -
#                     names:
#                         - -s
#                         - --short-notation
#                     help: |
#                         Path to yaml file with list of short notations
#                         Example - p.radius:
#                             MachineLearningModelInfo.Fingerprints.Radius
#                 -
#                     names:
#                         - -v
#                         - --verbosity
#                     default: 0
#                     action: count
#                     help: >
#                         Set verbosity level. 
#                         -v - display query string,
#                         -vv - display records,
#                 -
#                     names:
#                         - -f
#                         - --format
#                     choices:
#                         - json
#                         - yaml
#                     default:
#                     help: Set model verbosity output format

