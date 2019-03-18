from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


setup(name='deltares',
      version='0.0.1',
      author='Cody L. Johnson',
      author_email='mail@cody-johnson.tech',
      description='modules for working with Delft3D and XBeach output',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
