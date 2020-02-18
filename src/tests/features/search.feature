@common
Feature: Search for demo
    Basic demo portal functionality


@search
Scenario Outline: Search for certain control
    Given I am on a demos page
    And Search box is displayed in sidebar
    When I type <control_name> in the search box
    Then There should be <N> expected results in the list


    Examples:
    | control_name  | N |
    | Check         | 3 |
    | Pass          | 1 |
    | Auto          | 1 |