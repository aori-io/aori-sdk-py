from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aori-sdk-py',
    version='0.6',
    packages=['aori_sdk_py'],  # Adjusted to explicitly specify the package
    package_dir={'aori_sdk_py': 'aori_sdk_py'},  # Map package name to directory
    install_requires=[
        'requests',
        'python-dotenv',
        'websocket-client'
    ],
    author='Joshua Baker',
    author_email='joshua@aori.io',
    description='aori.io python sdk',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='aori',
    url='https://github.com/aori-io/aori-sdk-py'
)