from setuptools import setup

setup(name='plisp',
      version='0.1',
      description='A simple lisp implemented in python',
      author='Michael Smith',
      packages=['plisp'],
      entry_points={
          'console_scripts': [
              'plisp = plisp.__main__:main'
              ]
          }
      )
