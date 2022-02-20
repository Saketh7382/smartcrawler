import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smartcrawler",                    
    version="0.0.2",                        
    author="Saketh Gundlapalli",                     
    description="Package for crawling items from webpages and store them as json file",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',                
    py_modules=["smartcrawler","exceptions","object"],             
    package_dir={'':'smartcrawler/src'},     
    install_requires=[
        'selenium==3.141.0',
        'webdriver_manager==3.4.2'
    ]                     
)