# luogu-api-python
A Python implementation of the Luogu API.

## Project Description

`luogu-api-python` is a Python library that provides an interface to interact with the Luogu online judge system. It allows users to programmatically manage problems, and user operations on Luogu. This library aims to simplify the process of automating tasks on Luogu by providing easy-to-use methods and classes.

Upstream docs: [https://github.com/sjx233/luogu-api-docs](https://github.com/sjx233/luogu-api-docs)

## Installation

To install the package, use pip:

```console
$ pip3 install luogu-api-python
```

To install the package from source, follow these steps:

```console
$ git clone https://github.com/NekoOS-Group/luogu-api-python.git
$ cd luogu-api-python
$ python3 -m pip install .
```

## Usage

### Synchronous API

Here is an example of how to use the package:

```python
import pyLuogu

# Initialize the API without cookies
luogu = pyLuogu.luoguAPI()

# Get a list of problems
problems = luogu.get_problem_list().problems
for problem in problems:
    print(problem.title)
```

### Asynchronous API (Experimental)

The package also provides experimental support for async operations:

```python
import asyncio
import pyLuogu

# Initialize the async API without cookies
luogu = pyLuogu.asyncLuoguAPI()

async def main():
    problems = (await luogu.get_problem_list()).problems
    for problem in problems:
        print(problem.title)

asyncio.run(main())
```

Note: The async API is currently experimental and subject to changes.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### Pull Request

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine:
    ```commandline
    $ git clone https://github.com/your-username/luogu-api-python.git
    $ cd luogu-api-python
    ```
3. Create a new branch for your feature or bugfix:
    ```commandline
    $ git checkout -b feature-or-bugfix-name
    ```
4. Make your changes and commit them with a descriptive commit message:
    ```commandline
    $ git add .
    $ git commit -m "Description of your changes"
    ```
5. Push your changes to your forked repository:
    ```commandline
    $ git push origin feature-or-bugfix-name
    ```
6. Open a pull request on the original repository and provide a detailed description of your changes.

### Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. Provide as much detail as possible to help us understand and address the issue.

## Todo List

API Implementation Status

### Core APIs

- [x] Problem API
  - [x] get_problem_list
  - [x] get_team_problem_list 
  - [x] get_problem
  - [x] get_problem_settings
  - [x] update_problem_settings
  - [x] update_testcases_settings
  - [x] create_problem
  - [x] delete_problem
  - [x] transfer_problem
  - [ ] download_testcases
  - [ ] upload_testcases

- [x] Problem Set API
  - [x] get_problem_set

- [x] Contest API
  - [x] get_contest

- [x] Discussion API
  - [x] get_discussion

- [x] Activity(benben) API
  - [x] get_activity

- [x] Team API
  - [x] get_team

- [x] Paste API
  - [x] get_paste

- [x] Artical API
  - [x] get_solution

- [x] User API
  - [x] get_user
  - [x] get_user_info
  - [x] get_user_followings_list
  - [x] get_user_followers_list
  - [x] get_user_blacklist
  - [x] search_user

- [x] User Operations
  - [ ] login
  - [ ] logout
  - [x] me
  - [ ] submit_code
  - [x] get_created_problem_list
  - [ ] get_created_problemset_list
  - [ ] get_created_content_list
  - [ ] update_setting

- [x] Miscellaneous
  - [x] get_tags
  - [x] get_image
  - [ ] get_captcha
  - [ ] sign_up

### Alternative API Implementations

- [x] asyncLuoguAPI (Experimental)
  - [x] Async versions of all implemented core APIs
  - [ ] Performance optimizations
  - [ ] Comprehensive error handling

- [ ] staticLuoguAPI
  - [ ] Initial implementation
  - [ ] Documentation

### Test Cases and Documentation

Note: Test suite and documentation are planned for implementation after API features are stabilized. This includes:

- Comprehensive test coverage for both sync and async APIs
- API reference documentation with examples
- Integration test scenarios
- Development guides and best practices

These will be prioritized once the core functionality reaches a stable state.