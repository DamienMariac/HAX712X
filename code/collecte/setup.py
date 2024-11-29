from setuptools import setup, find_packages

setup(
    name='recolte', 
    version='1',  
    packages=find_packages(), 
    description='Un package pour télécharger et fusionner des fichiers JSON',  
    install_requires=[
        'requests',  
    ],
)
