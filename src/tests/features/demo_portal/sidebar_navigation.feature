@common
Feature: Sidebar navigation
    Basic demo portal functionality


Background:
    Given I am on a demos page
    And Sidebar is displayed on left side


@sidebar
Scenario Outline: Navigate throug demos
    When I click <control_name> link in the sidebar
    Then <control_name> demo page should be displayed

    Examples:
    | control_name  |
    | Checkbox      |
    | Password      |
    | AutoComplete  |
    | Calendar      |
    | Editor        |
    | Listbox       |
