Building a local copy of the HTML manual
----------------------------------------
1. Install python and pip

2. Install the sphinx python package using the following terminal command

        pip install sphinx
    
3. Install the readthedocs theme template for sphinx

        pip install sphinx_rtd_theme

4. Start a terminal instance in the "docs" folder of your local PythonDriver repo and enter the following to kick off a build

        sphinx-build -nWb html . ./_build/html

    html is the build format and ./_build/html is the folder location where the build output will go

5. Open docs/_build/html/index.html with your preferred browser, and you should have a website style version of the docs!

Notes
-----
If you experience pages appearing and disappearing in the table of contents, add -a to your build command to force a full rebuild like so:

        sphinx-build -a -b html . ./_build/html