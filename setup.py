from setuptools import setup, find_packages

setup(
    name='regplates',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'pygame_gui',
        'tkinter',
        'itertools',
        'pickle',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'xxxxxxxxxx = main:main_function'],
    },
)