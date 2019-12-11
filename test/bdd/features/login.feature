Feature: Authorization workflow with Leanda

  Scenario: Login as valid user
    Given I am a valid user
      And I want to login
     Then I run command
      And get successfull message
      And get my username

  @wip
  Scenario: Login as invalid user
    Given I am an invalid user
      And I want to login
     Then I run command
      And I get an error message

  Scenario Outline: Login as valid user having extra info
    Given I am a valid user
      And I want to login
      And ask <extra> info
     Then I run command
      And get asked info

     Examples: Verbosity
      | extra     |
      | more      |
      | much more |
      | all       |

  Scenario Outline: User self identifying
    Given I want to identify myself
      And ask <extra> info
     Then I run command
      And get asked info

    Examples: Verbosity
      | extra     |
      | none      |
      | more      |
      | all       |

   Scenario: User's logout
     When I want to logout
     Then I run command
      And get successfull message

  Scenario: User self identifying after logout
    Given I want to identify myself
     Then I run command
      And I get an error message
