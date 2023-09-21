from setuptools import  setup


setup(name='clean_folder',
      version = '0.0.2',
      packages=['clean_folder'],
      description='code for clean folders',
      author='Mykhailo Symchyra',
      author_email='sumchura@gmail.com',
      url='https://github.com/Symchyra-M',
      license='MIT',
      entry_points={
          'console_scripts': ['clean-folder = clean_folder.clean:main']

      },
      zip_safe=False,
      install_requires=[
          'markdown',
      ],
)
