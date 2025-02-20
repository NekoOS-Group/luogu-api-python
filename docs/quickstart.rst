Quickstart
==========

Installation
------------

To install ``luogu-api-python``, simply run this command in your terminal of choice::

    $ pip3 install luogu-api-python

Installing via source is also available, for example, clone the repository::

    $ git clone https://github.com/NekoOS-Group/luogu-api-python.git 

and install::

    $ cd luogu-api-python
    $ python3 -m pip install .

Synchronous API
---------------

Here is an example of how to use::

    import pyLuogu

    # Initialize the API without cookies
    luogu = pyLuogu.luoguAPI()

    # Get a list of problems
    problems = luogu.get_problem_list().problems
    for problem in problems:
        print(problem.title)
    
Asynchronous API (Experimental)
-------------------------------

``luogu-api-python`` also provides experimental support for async operations::

    import asyncio
    import pyLuogu

    # Initialize the async API without cookies
    luogu = pyLuogu.asyncLuoguAPI()

    async def main():
        problems = (await luogu.get_problem_list()).problems
        for problem in problems:
            print(problem.title)

    asyncio.run(main())

    