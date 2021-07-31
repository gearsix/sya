import setuptools

DESC='download & split long youtube videos as audio tracks'
LONG_DESC='download long youtube videos as audio tracks using youtube-dl and split them into multiple audio tracks using ffmpeg.'

with open('README.txt', 'r') as f:
    LONG_DESC = f.read()

setuptools.setup(
	name='sya',
	version='0.8.0',
	author='gearsix',
	author_email='gearsix@tuta.io',
	description=DESC,
        long_description=LONG_DESC,
        long_description_content_type='text/plain',
	url='https://notabug.org/gearsix/sya',
	packages=setuptools.find_packages(),
	classifiers=[
			'Programming Language :: Python',
			'Environment :: Console',
			'License :: Public Domain',
			'Operating System :: OS Independent',
	],
        scripts=['sya', 'sya-pyqt']
)
