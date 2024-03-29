import io
from setuptools import setup


with io.open('README.md', 'rt', encoding='utf8') as readme_file:
    readme = readme_file.read()

with io.open('VERSION', 'rt', encoding='utf8') as version_file:
    version = version_file.read().strip()

setup(
    name='lakeshore',
    version=version,
    maintainer='Lake Shore Cryotronics, Inc.',
    maintainer_email='service@lakeshore.com',
    license='MIT',
    description='A package to connect to and interact with Lake Shore instruments.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=[r'lakeshore'],
    url='https://github.com/lakeshorecryotronics/python-driver',
    python_requires='>=3.7',
    install_requires=['pyserial>=3.0',
                      'iso8601',
                      'packaging',
                      "enum34;python_version<'3.4'",
                      'wakepy>=0.7.1'],
    classifiers=['Programming Language :: Python :: 3']
)
