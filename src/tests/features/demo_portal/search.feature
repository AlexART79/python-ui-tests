@common
Feature: Search for demo
    Basic demo portal functionality


Background:
    Given I am on a demos page
    And Search box is displayed in sidebar


@search
@sidebar
Scenario Outline: Search for certain control
    When I type <control_name> in the search box
    Then There should be <N> expected results in the list


    Examples:
    | control_name  | N |
    | Check         | 3 |
    | Pass          | 1 |
    | Auto          | 1 |