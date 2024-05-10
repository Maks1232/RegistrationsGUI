from setuptools import setup, find_packages

setup(
    name='regplates',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'regplates = regplates.main:main_function'],
    },
    package_data={
        'regplates': ['Resources/*', 'Resources/Images/*']
    }
)