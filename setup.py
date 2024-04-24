from setuptools import setup, find_packages

setup(
    name='regplates',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'pygame_gui',
        'pandas',
        'openpyxl'
    ],
    entry_points={
        'console_scripts': [
            'regplates = regplates.main:main_function'],
    },
    package_data={
        'regplates': ['Resources/**']
    }
)