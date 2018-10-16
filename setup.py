import io
from setuptools import setup


with io.open('README.md', 'rt', encoding='utf8') as readme_file:
    readme = readme_file.read()

setup(
    name='lakeshore',
    version='0.0.1',
    maintainer='Lake Shore Cryotronics, Inc.',
    maintainer_email='service@lakeshore.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=[r'lakeshore'],
    url='',  # TODO: Add GitHub URL
    install_requires=[]  # TODO: Add dependencies
)
