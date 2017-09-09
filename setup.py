from setuptools import setup

setup(name='s3santa',
      version='0.1',
      description='Data request user manager for AWS S3',
      url='https://github.com/kunanit/s3-santa',
      author='Andrew Ang',
      author_email='andrew_ang@harvard.edu',
      license='MIT',
      packages=['s3santa'],
      install_requires=[
            'boto3',
      ],
)
