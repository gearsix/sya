NAME
  sya - split youtube audio

SYNOPSIS
  sya.py [OPTIONS] TRACKLIST

DESCRIPTION
  sya downloads, converts and splits youtube videos using `youtube-dl` and `ffmpeg`.
  while intended for long audio mixtapes, the tools it uses are quite flexible so
  you could use it to download & split long videos as well.

OPTIONS
  -h --help	displays help message
  -k, --keep	youtube-dl option, keep the video file on disk after the
				post-processing; the video is erased by default
  -o [PATH], --output [PATH]	specify the directory to write output files to
								(default: ./<tracklist filename>/)
  -f [EXT], --format [EXT]	specify the --audio-format argument to pass to youtube-dl
							(default: mp3)
  -q [QUALITY], --quality [QUALITY]	youtube-dl option, specify the --audio-quality argument
									to pass (default: 320K)
  --youtube-dl [PATH]	path of the youtube-dl binary to use
  --ffmpeg [PATH]	path of the ffmpeg binary to use

TRACKLIST
  TRACKLIST files should be text file that has the URL/v=code of the youtube video to
  download on the first line and the starting timestamp of each section to split, followed
  by the title of that section section.
  Here is an example:

	https://www.youtube.com/watch?v=ors0wpcVDcc
	Los Natas - Brisa Del Desierto [00:00]
	Sleeping Pandora - Through The Maze [02:05]
	Fluidage - Feel Like I Do [12:43]
	My Sleeping Karma - Psilocybe [18:11]
	Daisy Pusher - While Wailing (Only a Part) [26:01]
	The Whirlings - Worries on a Shelf [30:49]
	Arenna - Move Through Figurehead Lights [36:28]
	Ten East - Skyline Pressure [43:32]
	Wooden Shjips - These Shadows [49:24]
	King Buffalo - Orion Subsiding [54:48]
	UFO Över Lappland - Nothing That Lives Has . . . . Such Eyes [1:00:18]
	Papir - III.III [1:09:31]
	Mirovia - Multiversum [1:14:24]
	Quest For Fire - Strange Waves [1:23:32]
	35007 - 22 25 & 61 74 [1:31:07]
	Stoned Cobra - Black Spiral Dancer [1:39:39]
	U.S. Christmas - Suzerain [1:48:09] 
	(I fucked up, the picture didn't make it. 
	Comacozer - BinBeal [1:56:53]
	Kungens Män- Bortkopplad från tiden [2:14:52]
	The Kings of Frog Island - Laid [2:35:03]
	Sungrazer - Behind [2:37:44]
	The Re-Stoned - Crystals [2:51:30]
	Deepspacepilots - Space Ghost [3:00:51]
	KR3TURE - Anthropocene [3:06:55]
	Domo - Samsara [3:10:37]
	KAMNI - Mandala [3:24:36]
	Blaak Heat -  Shadows (The Beast Pt. Ii) [3:31:21]
	Mick Clarke - Time Is Now [3:39:28]
	Weedpecker - Nothingness [3:42:45]
	Gypsy Sun Revival - Pisces [3:47:51]
	Black Bombaim - Blow, Vanish #1 [4:02:37]
	Colour Haze - Inside [4:05:10]
	Sutrah - La marcha del cordero [4:12:27]
	Sun of Man - Space [4:18:23]
	Fatso Jetson - Seroquel [4:30:41]
	Halma - Treadmill [4:37:15]
	Sonora Ritual - Spring [4:44:59]
	Causa Sui - Fichelscher Sun [4:49:16]
	Folkvang - Ensamhetens Famn [4:51:27]
	Graveyard - Longing [4:53:58]
	Maha Sohona - Asteroids Part 2: Trajectory [4:58:45]
	Judd Madden - In Absence [5:02:05]

INSTALL
  If you'd like to use sya from the CLI, then "cd" into the the sya directory
  and run "sudo make install"

AUTHORS
  - gearsix <gearsix@tuta.io>

