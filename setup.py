import setuptools

DESC='download & split long youtube videos as audio tracks'
LONG_DESC='download long youtube videos as audio tracks using youtube-dl and split them into multiple audio tracks using ffmpeg.'

with open('README.md', 'r') as f:
    LONG_DESC = f.read()

setuptools.setup(
	name='sya',
	version='1.0.1',
	author='gearsix',
	author_email='gearsix@tuta.io',
	description=DESC,
        long_description=LONG_DESC,
        long_description_content_type='text/markdown',
	url='https://notabug.org/gearsix/sya',
	packages=setuptools.find_packages(),
	classifiers=[
			'License :: Public Domain',
			'Programming Language :: Python',
			'Operating System :: OS Independent',
	],
        scripts=['sya.py', 'sya-pyqt.py']
)
