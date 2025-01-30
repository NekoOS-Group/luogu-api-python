# CHANGELOG of luogu-api-python

## In Development - [0.0.2] - 2025-01-30

This is a pre-release version. Breaking changes may occur in future updates.

### pyLuogu

- **[FEATURE]** Added an asynchronous variant of the API.
- **[ENHANCEMENT]** Introduced error definitions:
  - Now supports `LuoguAPIError`, `RequestError`, `AuthenticationError`, `NotFoundError`, `RateLimitError`, `ServerError`, and `ForbiddenError`.
- **[ENHANCEMENT]** Refactored `types.py`:
  - Improved type hints and introduced new types.
- **[ENHANCEMENT]** Optimized header-related implementation in `api.py`.
- **[ENHANCEMENT]** Implemented multiple new methods:
  - `luoguAPI.login()`, `luoguAPI.update_testcases_settings()`, `luoguAPI.transfer_problem()`, `luoguAPI.get_user()`,  
    `luoguAPI.get_user_info()`, `luoguAPI.get_user_following_list()`, `luoguAPI.get_user_follower_list()`,  
    `luoguAPI.get_user_blacklist()`, `luoguAPI.search_user()`, `luoguAPI.me()`, `luoguAPI.get_tags()`.
- **[META]** Updated `.gitignore`.
- **[DOCUMENTATION]** Updated `README.md` to reflecting async api change and migration to `pyproject.toml`.
- **[PACKAGING]** Migrated to `pyproject.toml`, replacing `setup.py`.
- **[EXAMPLES]** Added new example scripts:
  - `auto_add_tags.py`
  - `store_problem.py`
  - `store_problem_async.py`
  - `readme_example.py`
  - `readme_example_async.py`
  - `transfer_problem.py`
- **[EXAMPLES]** Removed `store_problem_settings.py` as it requires moderator privileges.

### bits

- **[FEATURE]** Added cache pool support.
- **[ENHANCEMENT]** Various optimizations.

### Unreleased

- **[FEATURE, WIP]** Developing a static API interface for advanced use cases.
- **[TESTS, WIP]** Setting up the test framework.
