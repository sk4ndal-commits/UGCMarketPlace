## 🧭 Coding Guidelines – CollabMarket

This document defines the coding principles, conventions, and boundaries for the
CollabMarket MVP. It is intended to ensure maintainable, scalable, and secure
code throughout the project.

---

## 📁 1. General Principles

- **Clarity over cleverness:** Prioritize readability and explicitness over
  brevity or “smart” code tricks.
- **Consistency is key:** Follow agreed conventions consistently across the
  codebase.
- **Modularity:** Write small, composable modules and functions with single
  responsibilities.
- **Testability:** Code must be easy to unit test and integration test.
- **Documentation-first:** All significant modules, functions, and APIs must
  include docstrings and inline comments explaining the “why,” not just the
  “what.”
- **Security by design:** Treat user data, authentication, and payment-related
  logic as critical components. Never store sensitive data in plaintext.

---

## 🧰 2. Backend Guidelines

### 2.1 Structure & Organization

- Follow a **modular, domain-driven** folder structure: `auth/`, `campaigns/`,
  `applications/`, `payments/`, etc.
- Each module must include:
    - `models.py` – database models
    - `serializers.py` – data serialization logic
    - `views.py` – API views / endpoints
    - `urls.py` – routing
    - `tests.py` – unit and integration tests

### 2.2 API Design

- Use **RESTful conventions**: `/api/v1/campaigns/`, `/api/v1/applications/`,
  etc.
- Follow **CRUD + action** naming standards (`list`, `create`, `retrieve`,
  `update`, `destroy`).
- Always return JSON responses with a consistent structure:
  ```json
  {
    "status": "success",
    "data": { ... },
    "errors": []
  }
  ```

Use descriptive HTTP status codes (200 OK, 201 Created, 400 Bad Request, etc.).

2.3 Models & ORM

    Use descriptive field names, avoid abbreviations.

    Always define __str__ methods for models.

    Use database constraints (unique, null=False, on_delete) explicitly.

2.4 Error Handling

    All errors must be caught and transformed into JSON error responses.

    Never expose internal stack traces or sensitive details in production responses.🖥️ 3. Frontend Guidelines (Vue)
3.1 Structure

Use the standard Vue 3 composition API.

Organize components by feature domain (/components/campaigns/, /components/auth/).

Follow a clear hierarchy:

views/ – pages

components/ – reusable components

store/ – global state (Pinia)

services/ – API and business logic

3.2 Coding Style

Use PascalCase for component names and file names.

Prefer composition API over options API.

Keep components under ~200 lines; extract logic into composables where possible.

All user-facing text must be in i18n-ready format (English as default).

3.3 UX & Accessibility

Use semantic HTML and ARIA roles.

Loading states and empty states are mandatory for all async views.

Maximum of 3 clicks to complete any major user action (e.g., applying for a campaign).

🔒 4. Security & Compliance

Always hash and salt passwords (Django handles this by default).

Use HTTPS in all environments.

Validate and sanitize all user input on both frontend and backend.

Log and audit all payment-related actions.

Follow GDPR guidelines: implement data export, deletion, and consent features.

5. Version Control

Create a commit for each completed task.