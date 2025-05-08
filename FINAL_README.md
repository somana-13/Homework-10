# Event Manager API - Validation and Testing Improvements

## Overview
This repository contains a FastAPI-based web application that enables event management functionalities with a robust user management system using OAuth2 authentication. This submission focuses on improving API validation and test coverage.

## Issues Addressed
- [Issue #1: Username Validation](https://github.com/somana-13/Homework-10/issues/1) - Added comprehensive validation for username fields
- [Issue #2: Password Security](https://github.com/somana-13/Homework-10/issues/4) - Implemented strong password requirements
- [Issue #3: Profile Field Edge Cases](https://github.com/somana-13/Homework-10/issues/3) - Improved handling of edge cases in profile fields
- [Issue #4: Email Test Failures](https://github.com/somana-13/Homework-10/issues/2) - Fixed email service testing
- [Issue #5: Test Coverage](https://github.com/somana-13/Homework-10/issues/5) - Increased test coverage from 81% to 87%

## Docker Deployment
The application has been deployed as a Docker image and is available on Dockerhub:
[Event Manager Docker Image](https://hub.docker.com/r/YOUR_DOCKERHUB_USERNAME/event_manager)

## Learning Reflection

Working on this project provided valuable insights into building secure and robust APIs. The task of implementing comprehensive validation for usernames and passwords taught me about balancing security requirements with user experience considerations. I learned that effective validation must account for a wide range of edge cases while remaining transparent to the user. The challenge of creating password validation that prevents common security pitfalls while allowing legitimate test data reinforced the importance of thinking from both an attacker's and a legitimate user's perspective.

Testing an application with external dependencies like email services presented unique challenges. I discovered the value of proper mocking techniques to isolate components during testing. This experience improved my understanding of test architecture and the importance of creating tests that are both comprehensive and maintainable. Increasing test coverage from 81% to 87% required methodical analysis of untested code paths and creative approaches to testing edge cases.

Collaboratively, this project reinforced the importance of clear documentation and communication when implementing security features. Each validation rule and test case needed clear rationale and documentation to ensure future developers understand the reasoning behind implementation decisions. The structured approach to fixing issues—starting with a clear problem statement, devising a solution approach, implementing changes, and verifying with tests—mirrors real-world software development practices and has strengthened my systematic approach to problem-solving.

## Key Improvements

### 1. Username Validation
Added comprehensive validation for usernames:
- Length constraints (3-30 characters)
- Character restrictions (alphanumeric, underscores, hyphens only)
- Consecutive special character prevention
- Start/end character validation
- Reserved word checks

### 2. Password Validation
Implemented robust password security:
- Minimum length requirement (8 characters)
- Complexity rules:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters
- Common password detection
- Sequential character pattern prevention

### 3. Profile Field Edge Case Handling
Enhanced validation for profile fields:
- URL validation with protocol checking
- Empty string handling
- Multiple field update consistency
- Length validation for fields like bio

### 4. Email Service Tests
Fixed email-related test failures:
- Implemented mock SMTP client
- Added proper test isolation
- Created appropriate fixtures for token-based tests

### 5. Test Coverage Improvements
- Increased overall test coverage from 81% to 87%
- Added 15+ new test cases
- Reached 100% coverage in critical modules
