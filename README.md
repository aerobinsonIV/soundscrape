# SoundScrape
Tools to help automate the process of downloading songs and embedding accurate and high-quality metadata.

# Installation
`
pip install undetected-chromedriver
pip install pydub
pip install stagger
`

### from the pydub readme: https://github.com/jiaaro/pydub#dependencies
Download and extract libav from Windows binaries provided [here](http://builds.libav.org/windows/).
Add the libav `/bin` folder to your PATH envvar
Reboot

### avoiding bot detection
https://github.com/ultrafunkamsterdam/undetected-chromedriver

## Use case goal

### Downloading
- User runs searcher/downloader program with artist and song title
- Program shows list of sources that song is available from
    - SoundCloud
    - YouTube
    - Beatport
    - Amazon
- User chooses a source
- File is downloaded automatically if purchase is not required
- User buys if purchase is required

### Lyrics
- User runs metadata program with file, artist, song title
- Program gets lyrics from multiple sources and cleans them
- Compares sources to generate guesses of correct lyrics
- User can accept or reject each guess
- If all guesses are rejected, program requests user paste in lyrics which are then cleaned
- Optionally, user can request to perform manual edits in a text editor at this point
- Lyrics are saved into file

### Basic metadata
- User runs program and specifies year, artist, album, title, album artist
- Program adds metadata to file
- If album isn't specified, album field is set to title
- If album artist isn't specified, album artist fieled is set to artist

### Cover artwork
- User runs artwork program with some combination of the following that provides at least name and artist
    - File w/ metadata
    - Title and artist params if file doesn't have metadata
    - Optional parameter to choose album artwork or single artwork
    - Link to a picture
- Program searches out images, finds ones that are high-resolution and probably the correct artwork
- Displays top several choices to user, user chooses best
- Image is automatically embedded in file
