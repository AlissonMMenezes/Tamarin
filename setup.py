import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='alisson_cli',  
     version='0.1',
     scripts=['tamarin.py'] ,
     author="Alisson Machado",
     author_email="alisson.itops@gmail.com",
     description="Infrastructure as code",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/AlissonMMenezes/Tamarin",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache2 License",
         "Operating System :: OS Independent",
     ],
 )