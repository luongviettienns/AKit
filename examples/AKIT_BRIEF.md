# AKit project contract example

Product: NestJS + PostgreSQL management web application
Goal: Build and demonstrate learner enrollment and assignment grading
Actors: Admin, teacher, student
Requirements: Student enrollment, class membership, assignment upload, teacher confirmation before publishing AI grades
Non-goals: Payment, multi-region, microservices
Stack: NestJS API, PostgreSQL, React UI (if approved)
Quality: Clear UX, mobile support, no unapproved PII disclosure, authorization by role
Acceptance:
- Invalid IDs and negative scores are rejected with documented errors.
- Unauthorized role cannot publish grades.
- Failed transactions leave data consistent.
- Integration tests run on a disposable DB before merge.
Gates: approve design prototype before UI implementation; approve migrations before running against live data.
