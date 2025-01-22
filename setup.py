from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()
    install_requires = install_requires[2:] # remove setuptools and wheel

setup(
    name='luogu-api-python',
    description='A Python library to interact with the Luogu online judge system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.0.1-alpha',
    packages=['pyLuogu', 'pyLuogu.bits'],
    install_requires=install_requires,
    url='https://github.com/NekoOS-Group/luogu-api-python',
    license='GPL-3.0',
    author='bzy',
    author_email='bzy.cirno@gmail.com'
)
