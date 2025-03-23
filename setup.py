from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    with open('requirements.txt') as f:
        lines = f.readlines()
    return [
        line.strip()
        for line in lines
        if line.strip() != '-e .'
        and not line.startswith('#')
        and not line.startswith('-r')
        and line.strip() != ''
    ]

setup(
    name='NetworkSecurity',
    version='0.1',
    packages=find_packages(),
    install_requires=get_requirements(),
    author='EsmaelAwad',
    author_email='eawad9329@gmail.com'
)
