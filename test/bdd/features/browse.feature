Feature: Browse Leanda 

Scenario: Get current working Leanda folder
   Given I want to get current working Leanda folder
    When I run the command
    Then I get full Leanda path current working folder

# params:
#     -
#         names:
#             - -v
#             - --verbosity
#         default: 0
#         action: count
#         help: Set verbosity level

Scenario: Change current working Leanda folder to home folder
   Given I want change current working Leanda folder
    When I run the command
    Then I am in my home remote folder

Scenario: Change current working Leanda folder to parent folder
   Given I want change current working Leanda folder
     And set path '..'
    When I run the command
    Then I am in parent remote folder

Scenario: Change current working Leanda folder to parent folder whilst in home folder
   Given I want change current working Leanda folder
     And set path '..'
     And I am in parent remote folder
    When I run the command
    Then I get an error


Scenario: Change current working Leanda folder to folder identified by full id
   Given I want change current working Leanda folder
     And set full id
    When I run the command
    Then I am in other remote folder



Scenario: Change current working Leanda folder to folder identified by part id
   Given I want change current working Leanda folder
     And set part id
    When I run the command
    Then I am in other remote folder

Scenario: Change current working Leanda folder to folder identified by part name
   Given I want change current working Leanda folder
     And set part
    When I run the command
    Then I am in other remote folder

Scenario: Change current working Leanda folder to folder ambiguously identifyed by part name
   Given I want change current working Leanda folder
     And set ambiguously identifyed part name
    When I run the command
    Then I get an error

Scenario: Change current working Leanda folder to folder ambiguously identifyed by part id
   Given I want change current working Leanda folder
     And set ambiguously identifyed part id
    When I run the command
    Then I get an error

Scenario: Change current working Leanda folder to folder identified by invalid full id
   Given I want change current working Leanda folder
     And set invalid full id
    When I run the command
    Then I get an error

Scenario: Change current working Leanda folder to folder identified by not exists full id
   Given I want change current working Leanda folder
     And set not existed full id
    When I run the command
    Then I get an error

# names:
#     - container
# nargs: '?'
# default: .

Scenario: Remove item identified by full id
   Given I want remove item
     And set full id
    When I run the command
    Then Item doesn't exist

Scenario: Remove item identified by part id
   Given I want remove item
     And set part id
    When I run the command
    Then Item doesn't exist

Scenario: Remove item identified by part name
   Given I want remove item
     And set part name
    When I run the command
    Then Item doesn't exist

Scenario: Remove item ambiguously identifyed by part name
   Given I want remove item
     And set ambiguous part name
    When I run the command
    Then I get an error

Scenario: Remove item ambiguously identifyed by part id
   Given I want remove item
     And set ambiguous part id
    When I run the command
    Then I get an error

Scenario: Remove item ambiguously identifyed by part id
   Given I want remove item
     And set invalid full id
    When I run the command
    Then I get an error

# names:
#     - container
# nargs: 1

Scenario: List contents of current folder
   Given I want to list folder contents
    When I run the command
    Then I get list of folder contents

Scenario: List contents of folder identified by full id
   Given I want to list folder contents
     And set full id
    When I run the command
    Then I get list of folder contents

Scenario: List contents of folder identified by part id
   Given I want to list folder contents
     And set part id
    When I run the command
    Then I get list of folder contents

Scenario: List contents of folder identified by part name
   Given I want to list folder contents
     And set part name
    When I run the command
    Then I get list of folder contents

Scenario: List contents of folder ambiguously identifyed by part name
   Given I want to list folder contents
     And set ambiguous part name
    When I run the command
    Then I get an error

Scenario: List contents of folder ambiguously identifyed by part id
   Given I want to list folder contents
     And set ambiguous part id
    When I run the command
    Then I get an error

Scenario: List contents of folder identified by invalid full id
   Given I want to list folder contents
     And set invalid full id
    When I run the command
    Then I get an error

Scenario: List contents of folder identified by full id and limit list to 20 items
   Given I want to list folder contents
     And set full id
     And set limit items to 20
    When I run the command
    Then I get list of folder contents

Scenario: List contents of folder identified by full id and limit list to 20 items and show 2 page
   Given I want to list folder contents
     And set full id
     And set limit items to 20
     And set page to 2
    When I run the command
    Then I get list of folder contents

Scenario: List contents of folder identified by full id and show 2 page
   Given I want to list folder contents
     And set full id
     And set page to 2
    When I run the command
    Then I get list of folder contents

# names:
#     - container
# default: ''
# nargs: '?'
# -
# names:
#     - -s
#     - --size
# default: 10
# help: Report page size (default value 10)
# -
# names:
#     - -p
#     - --page
# default: 1
# help: Report page number (default value 1)

# '''
