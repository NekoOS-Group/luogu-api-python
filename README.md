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

2. Install the dependencies:
    ```commandline
    $ pip3 install -r requirements.txt
    ```

3. Install the package:
    ```commandline
    $ python3 setup.py install
    ```

## Usage

Here is an example of how to use the package:

```python
import pyLuogu

# Initialize the API with cookies
cookies = pyLuogu.LuoguCookies.from_file("cookies.json")
luogu = pyLuogu.luoguAPI(cookies=cookies)

# Get a list of problems
problems = luogu.get_problem_list()
for problem in problems:
    print(problem.title)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Todo List

Methods of class `LuoguAPI`

 - [x] Problem
   - [x] get_problem_list
   - [x] get_created_problem_list
   - [ ] get_team_problem_list 
   - [x] get_problem
   - [x] get_problem_settings
   - [x] update_problem_settings
   - [ ] update_testcases_settings
   - [x] create_problem
   - [x] delete_problem
   - [ ] transfer_problem
   - [ ] download_testcases
   - [ ] upload_testcases
 - [x] UserOperation
   - [ ] login
   - [ ] logout
   - [ ] me

Others

 - [ ] asyncLuoguAPI
 - [ ] staticLuoguAPI
