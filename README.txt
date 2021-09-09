NAME
  sya - split youtube audio

SYNOPSIS
  sya.py [OPTIONS] TRACKLIST

DESCRIPTION
  sya downloads, converts and splits youtube videos into multiple audio
  tracks using `youtube-dl` and `ffmpeg`.

OPTIONS
  -h --help		displays help message
  -k, --keep	
	youtube-dl option, keep the full track on disk after post-processing,
	the video is erased by default
  -o, --output [PATH]	
	specify the directory to write output files to (defaults to a directory
	named after the tracklist filename)
  -f, --format [EXT]	
	specify the --audio-format argument to pass to youtube-dl (default: mp3)
  -q, --quality [QUALITY]	
	specify the --audio-quality argument to pass (default: 320K)
  --youtube-dl [PATH]	
	path of the youtube-dl binary to use
  --ffmpeg [PATH]	
	path of the ffmpeg binary to use

TRACKLIST
  TRACKLIST files should be text file that has the URL/v=code of the youtube video to
  download on the first line and the starting timestamp of each section to split, followed
  by the title of that section section for every line after.

  Of course, you don't have to put the timestamp first, sya will try and accomocodate
  whatever syntax is used, just beware that this might cause problems.

  Here's an example:

	https://www.youtube.com/watch?v=LbjcaMAhJRQ
	Sneaky Snitch (0:00)
	Fluffing a Duck (2:16)
	Cipher (3:24)
	Scheming Weasel (7:15)
	Carefree (8:44)
	Thatched Villagers (12:09)
	Monkeys Spinning Monkeys (16:15)
	Wallpaper (18:20)
	Pixel Peeker Polka (21:59)
	Killing Time (25:21)
	Hitman (28:46)
	The Cannery (32:07)
	Cut and Run (35:09)
	Life of Riley (38:44)
	Quirky Dog (42:39)
	The Complex (45:08)
	Hyperfun (49:35)
	Black Vortex (53:29)
	Rock on Chicago (56:19)
	Volatile Reaction (57:58)
	On the Ground (1:00:44)
	Wagon Wheel (electronic) (1:03:23)
	Call to Adventure (1:08:26)
	Hustle (1:12:33)
	Cupids Revenge (1:14:34)
	Dirt Rhodes (1:16:20)
	Rhinoceros (1:18:20)
	Who Likes to Party (1:21:43)
	Spazzmatica Polka (1:26:01)


BUILDING
  It's more convenient to build sya-pyqt into a single binary (bundled
  with assets & libraries).
  To do this 'pyinstaller' seems most convenient (installed via "pip
  install pyinstaller"):

	pyinstaller sya-pyqt.py -F --windowed --add-data "folder.png:."

  On Windows, you'll need to use the following:

	pyinstaller sya-pyqt.py -F --windowed --add-data "folder.png;."

  This process also works to create binaries for the terminal version
  of the tool (sya.py). When building that version, the "--windowed"
  and "--add-data "folder.png:."" arguments don't need to be included.

INSTALL
  There are a lot of ways to install this tool.

  For most cases, you can just download and run the distribution binaries.

  FROM SOURCE	
  This method should work on all platforms to install it for the current
  user.
  Note that there are a lot of ways to install a python package from
  source, this is just one.

	python ./setup.py install --user --record install.txt

  The "--user" argument will only install sya for the current user. Remove
  it to install the tool to the system, although note that this will require
  admin permissions.

  This will create a 'install.txt' file in the current directory. This file
  contains all the files installed to your system. To uninstall using just
  remove all of these files.


DISCLAIMER
  It should go without saying, don't use this for pirating music.
  If you do, you're a dick and you're working against whatever band/label you
  love enough to download their product.

  Service like Bandcamp (https://bandcamp.com) are great and allow you download
  audio files of the albums you've bought, properly tagged and available for
  re-download whenever you need.

AUTHORS
  - gearsix (gearsix@tuta.io)

