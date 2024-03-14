from setuptools import setup

setup(name='whispervideos',
      version='0.0.2',
      description='',
      author='rpb',
      author_email = 'balandongiv@gmail.com',
      packages=['whispervideos'],
      long_description='This is the second version',
      install_requires=[
          'pandas','python-docx','openai-whisper','pydub','pytube',
            # pip install -U openai-whisper
      ]
      )
