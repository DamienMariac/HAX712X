from setuptools import setup, find_packages

setup(
    name="recolte",
    version="0.1",
    packages=find_packages(),  # Trouve automatiquement les modules
    install_requires=[
        "requests", 
        "beautifulsoup4", 
        "pooch", 
        "pandas", 
        "geopandas", 
        "shapely", 
        "folium"
    ],
)
