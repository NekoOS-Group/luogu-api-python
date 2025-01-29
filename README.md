# luogu-api-python
A Python implementation of the Luogu API

## Project Description

`luogu-api-python` is a Python library that provides an interface to interact with the Luogu online judge system. It allows users to programmatically manage problems, and user operations on Luogu. This library aims to simplify the process of automating tasks on Luogu by providing easy-to-use methods and classes.

Upstream docs: [https://github.com/sjx233/luogu-api-docs](https://github.com/sjx233/luogu-api-docs)

## Installation

To install the package, use pip:

```commandline
$ pip3 install luogu-api-python
```

To install the package from source, follow these steps:

1. Clone the repository:
    ```commandline
    $ git clone https://github.com/NekoOS-Group/luogu-api-python.git
    $ cd luogu-api-python
    ```

2. Install the package:
    ```commandline
    $ python3 -m pip install .
    ```

## Usage

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

Methods of class `LuoguAPI`

 - [x] Problem
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
 - [x] User
   - [x] get_user
   - [x] get_user_info
   - [x] get_user_followings_list
   - [x] get_user_followers_list
   - [x] get_user_blacklist
   - [x] search_user
 - [x] UserOperation
   - [ ] login
   - [ ] logout
   - [x] me
   - [ ] submit_code
   - [x] get_created_problem_list
   - [ ] get_created_problemset_list
   - [ ] get_created_content_list
   - [ ] update_setting
 - [x] Miscs
   - [x] get_tags
   - [ ] get_captcha
   - [ ] sign_up

Others

 - [ ] asyncLuoguAPI
 - [ ] staticLuoguAPI
