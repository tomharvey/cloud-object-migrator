from setuptools import setup, find_packages

setup(
    name='phasst-migrate',
    version='0.0.1',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    classifiers=['Private :: Do Not Upload'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'migrate = migrate.interfaces.cli:cli',
        ],
    },
    install_requires=[
        'boto3',
        'rackspacesdk',
        'click',
    ]
)
