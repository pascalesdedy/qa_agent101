# Standard Operating Procedure (SOP) for QA Engineering

## 1. Introduction
This document outlines the standard procedures for Quality Assurance (QA) to ensure high-quality software delivery.

## 2. Bug Reporting Standards
All bugs must be reported in the issue tracking system with the following mandatory fields:
- **Title**: [Component] Short description of the issue.
- **Severity**: Critical, High, Medium, Low (see section 3).
- **Environment**: Staging, Production, Dev.
- **Steps to Reproduce**: Detailed numbered list.
- **Expected Result**: What should happen.
- **Actual Result**: What actually happened.
- **Screenshots/Logs**: Evidence of the bug.

## 3. Severity Levels
| Level | Description | SLA |
| :--- | :--- | :--- |
| **Critical** | System down, data loss, blocking main flow. No workaround. | 2 hours |
| **High** | Major functionality broken. Workaround difficult. | 24 hours |
| **Medium** | Minor functionality broken. Workaround exists. | 3 days |
| **Low** | Cosmetic issues, typos, suggestions. | Next release |

## 4. Test Cycle Process
1. **Requirement Analysis**: Review PRD/Design specs.
2. **Test Planning**: Create Test Plan and Strategy.
3. **Test Case Creation**: Write BDD or traditional test cases.
4. **Execution**: Run tests on the designated environment.
5. **Reporting**: Log defects and send daily status reports.
6. **Sign-off**: QA Lead approves release candidate.

## 5. Automation Strategy
- **Tool**: Playwright with TypeScript.
- **Scope**: Smoke tests and Regression suite.
- **CI/CD**: Automation must pass before merging to main.

## 6. Best Practices
- **Shift Left**: Involve QA early in the SDLC.
- **Zero Tolerance**: No critical bugs in production.
- **Code Review**: QA reviews unit tests where possible.
