
# Help

**sya - split youtube audio**, downloads, converts & splits audio from youtube videos into multiple audio tracks.

## Overview

To work sya requires some manual work: **tracklist** information. For more details on this, see **Tracklists** below.<br/>
The rest of the options can be configured but are provided with defaults.

Here's an overview of the options:

- **Tracklist** - the text file containing tracklist information
- **Format** - set the format to convert the audio to
- **Quality** - set the audio quality to download in, for reference 5 is equal to *128k*
- **Keep unsplit file** - keep the downloaded audio file (before it gets split up)
- **Output** - the directory to download the audio track to and split it into multiple tracks

The resulting files can be found at the *Output:* filepath on your system.

If you've found a bug or want to suggest improvements, email: `gearsix@tuta.io`

## Tracklists

A tracklist is just a text file some where on your system.
It should contains:

- A *youtube URL* to download the audio from, this should be on the first line.
- Timestamps and titles for each track to split, there should be one timestamp and one title per-track (this can usually be found in the youtube video description or a top comment).

**Example**

Below you can see the contents of an example playlist.<br/>
Try saving it to a text file on your computer and as a test if you like.

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
