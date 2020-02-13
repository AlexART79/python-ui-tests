@checkbox
Feature: Checkbox tests
    React checkbox component tests


@basic
Scenario: Basic checkbox toggle
    Given I have basic checkbox control
    Then Checkbox checked state should be 'Off'
    When I toggle checkbox state
    Then Checkbox checked state should be 'On'


@advanced
Scenario: Advanced checkbox on off
    Given I have advanced checkbox control
    Then Checkbox checked state should be 'Off'
    And Checkbox label should be 'New York'

    When I set checkbox state to 'On'
    Then Checkbox checked state should be 'On'

    When I set checkbox state to 'Off'
    Then Checkbox checked state should be 'Off'