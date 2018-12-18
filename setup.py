import io
from setuptools import setup


with io.open('README.md', 'rt', encoding='utf8') as readme_file:
    readme = readme_file.read()

setup(
    name='lakeshore',
    version='0.0.3',
    maintainer='Lake Shore Cryotronics, Inc.',
    maintainer_email='service@lakeshore.com',
    license='MIT',
    description='A package to connect to and interact with Lake Shore instruments.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=[r'lakeshore'],
    url='https://github.com/lakeshorecryotronics/python-driver',
    install_requires=['pyserial>=3.0', 'iso8601']
)
