# 🛡️ Global QA Engineering Standard Operating Procedure (SOP)

> **"Quality is not an act, it is a habit."**  
> *Effective Date: 2025-12-22 | Version: 2.0 | Owner: QA Lead*

---

## 1. 🎯 QA Philosophy & Mandate
Our mandate is to **prevent** defects, not just find them. We act as the voice of the user and the guardian of production stability.
- **Zero Critical Bugs** in Production.
- **Shift-Left**: QA participates in PRD reviews and technical design discussions.
- **Automate First**: Manual testing is reserved for exploratory and usability testing.

---

## 2. 🐛 Defect Management Lifecycle

### 2.1 Bug Report Standard (Mandatory)
Any ticket failing to meet this standard will be **immediately rejected**.

*   **Title**: `[Area/Component] Concise Summary of the failure`
*   **Severity**: (See Matrix)
*   **Priority**: (Determined by PM/PO)
*   **Environment**: URL/Build Version / Device / OS
*   **Pre-conditions**: User state, data setup.
*   **Steps to Reproduce**:
    1.  Login as `user_type`.
    2.  Navigate to `Page X`.
    3.  Click on `Button Y`.
*   **Expected Result**: Exact behavior described in the spec.
*   **Actual Result**: Technical description of the failure (not just "it didn't work").
*   **Evidence**:
    *   📸 Screenshot (Annotated)
    *   🎥 Video (for UI interactions)
    *   📂 Network Logs (HAR file) or Server Logs (Stack trace) – **MANDATORY for 5xx errors.**

### 2.2 Severity Matrix
| Severity | Definition | SLA for Fix |
| :--- | :--- | :--- |
| **🚨 P0 - Critical** | **System Down / Data Loss / Blocked Revenue**. No workaround. Examples: Login down, Checkout broken, DB corruption. | **Immediate (Hotfix)** |
| **🔴 P1 - High** | **Major functionality broken**. Workaround is complex/risky. Examples: Search not working, Email notifications failed. | **24 Hours** |
| **🟠 P2 - Medium** | **Minor functionality broken**. Stable workaround exists. Examples: UI alignment issues causing confusion, non-critical API errors. | **Next Sprint** |
| **🟢 P3 - Low** | **Cosmetic / Suggestion**. Typos, color mismatch, nice-to-have UI polish. | **Backlog** |

---

## 3. 🚦 Testing Strategy & Scope

### 3.1 The Testing Pyramid
1.  **Unit Tests** (Dev): 70% coverage.
2.  **Integration/API Tests** (QA/Dev): 20% coverage.
3.  **E2E UI Tests** (QA): 10% coverage (Critical flows only).

### 3.2 Test Entry & Exit Criteria
*   **Entry**: Code deployed to Staging, Unit tests passed, Sanity Smoke check passed.
*   **Exit (Release Candidate)**:
    *   100% Pass rate on Regression Suite.
    *   0 Open P0/P1 bugs.
    *   Signed-off Test Execution Report.
    *   Performance metrics within defined thresholds (<2s load time).

---

## 4. 🤖 Automation Framework Standards

**Stack**: Playwright (TypeScript)
**Pattern**: Page Object Model (POM)

### 4.1 Coding Standards
*   **Selectors**: Use `data-testid` attributes. NEVER use XPath or brittle CSS selectors (e.g., `div > div:nth-child(3)`).
*   **Independency**: Every test must encompass its own data setup and teardown. No test chaining.
*   **Waiting**: No hardcoded sleeps (`await page.waitForTimeout(5000)` is **FORBIDDEN**). Use smart awaits (`expect(locator).toBeVisible()`).

### 4.2 Flaky Test Protocol
Any test failing intermittently is marked `[FLAKY]`, removed from the CI pipeline, and assigned a P1 ticket to fix immediately. **We do not tolerate false negatives.**

---

## 5. 🚀 Release Governance (`Go/No-Go`)

Before any deployment to Production:
1.  **Staging Verification**: Full regression pass on Staging.
2.  **UAT Sign-off**: Product Owner approval.
3.  **Change Log**: Review of all merged PRs against Jira tickets.
4.  **Rollback Plan**: Verified procedure to revert changes if smoke test fails.

> **Rule of Thumb**: If you are unsure, the answer is **NO-GO**.

---

## 6. 🔍 API Testing Guidelines
*   Validate **Status Codes** (200, 201, 400, 401, 403, 500).
*   Validate **Response Schema** (JSON Validation).
*   Validate **Response Time** (Latency check).
*   **Negative Testing**: Malformed payloads, invalid tokens, SQL injection attempts.

---

*This document is a living artifact. Updates require approval from the QA Chapter Lead.*
