from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
	name='listorm',
	version='1.0.0',
	license='MIT',
	description='list orm methods and shortcuts for table type of dict-list',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author = 'HS Moon',
	author_email = 'pbr112@naver.com',
	py_modules = ['listorm'],
	install_requires=[],
	keywords=['listorm', 'list of dict'],
	url='https://github.com/zwolf21/listorm',
	packages=find_packages(exclude=['contrib', 'docs', 'tests']),
	install_requires=['openpyxl'],
	classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
	python_requires=">=3.6"
)
