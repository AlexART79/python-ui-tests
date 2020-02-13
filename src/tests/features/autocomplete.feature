@autocomplete
Feature: Autocomplete tests
    React autocomplete component tests


@advanced
Scenario: Advanced autocomplete select
    Given I have advanced autocomplete control
    When I click dropdown button in advanced autocomplete control
    Then Autocomplete should became expanded

    When I selected value 'Audi' in autocomplete dropdown
    Then Autocomplete should became collapsed
    And Autocomplete control value should be 'Audi'


@basic
Scenario Outline: Basic autocomplete select
    Given I have basic autocomplete control
    When I start typing <text> in basic autocomplete control
    And I selected value <value> in autocomplete dropdown
    Then Autocomplete should became collapsed
    And Autocomplete control value should be <value>

    Examples:
    | text | value          |
    | Uni  | United States  |
    | Uni  | United Kingdom |
    | Uk   | Ukraine        |