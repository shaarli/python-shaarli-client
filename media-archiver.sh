#!/bin/bash
# Description: export links tagged 'music' from a shaarli instance, download them with youtube-dl
# Status: proof-of-concept/draft
# Source: https://github.com/nodiscc/python-shaarli-client
# License: MIT
set -e

##################
# TODO

#Desired features:

# * Command line interface
# * export: Export shaares from a shaarli instance to plain text
# * export: Filter shaares by tag/private setting/fulltext search/date...
# * export: Export shaares to other formats (HTML? + browseable/filterable index + list of tags? Markdown?....) http://work.krasimirtsonev.com/git/bubblejs/example/# https://github.com/nodiscc/awesome-selfhosted/blob/yaml/html/filtering.js
# * youtube-dl: Extract audio content using youtube-dl
# * youtube-dl: Extract video content using youtube-dl
# * youtube-dl: implementation: import youtube-dl as a library? or use subprocess calls?
# * youtube-dl: Customizable extraction options (path, file naming, format...) - currently everything is hardcoded.
# * youtube-dl: Blacklist items from being downloaded through a blacklist or special tags
# * youtube-dl: Ignore already downloaded items, or force re-downloading them
# * youtube-dl: Log success and failures

#Might be wanted someday:

# * youtube-dl: Separate public/private link output directories
# * youtube-dl: don't use --no-playlist when link matches a pattern/tag (album, playlist...)
# * youtube-dl: Convert multimedia files to other formats
# * youtube-dl: Instead of downloading items, create an m3U playlist for media, linking to the media url reported by youtube-dl --get-url
# * webpages: Download webpage contents
# * webpages: Low priority for me, https://github.com/pirate/bookmark-archiver seems to do a good job
# * webpages: Delegate to another lib/program? httrack, wget, pavuk, scrapy, https://github.com/lorien/grab?
# * webpages: Use special downloaders/extractors when link matches a pattern/tag (git clone, git clone mediawiki://, https://github.com/beaufour/flickr-download, https://github.com/bdoms/tumblr_backup, https://github.com/Szero/imgur-album-downloader...)
# * webpages: Recursively download certain files (htm,html,zip,png,jpg,wav,ogg,mp3,flac,avi,webm,ogv,mp4,pdf...) when link matches a pattern/tag. Ability to restric to the same sub/domain
# * webpages: filter ads from downloaded webpages (dnsmasq? host files: https://github.com/nodiscc/superhosts, filterlists.com)
# * webpages: download links in descriptions
# * webpages: add "readability" features: cleanup pages from useless elements (https://github.com/wallabag/wallabag/tree/master/inc/3rdparty/site_config) - less needed thanks to firefox reading mode, the only benefit would be lower disk usage
# * export: append archive.org URL to HTML index
# * other: download magnet links
# * other: upload to archive.org (public links only) - curl https://web.archive.org/save/$url ; https://github.com/Famicoman/ia-ul-from-youtubedl

###################
# configuration

outdir="music" # Output directory for downloaded files
exportfile="${outdir}/shaarli.export" # Write plain text 
logfile="${outdir}/youtube-dl.log" # Archiver log file location
blacklist="${outdir}/youtube-dl.blacklist" # URLs listed there will not be downloaded
youtube_dl_extra_options="--no-playlist --add-metadata" # Extra options for youtube-dl
wait_time="1" # time to wait between requests

###################

function _install {
python3 -m venv venv
source venv/bin/activate
python setup.py install
pip freeze
}

#################

function _export_music_links {
	# get links tagged 'music' and write them to a file
	# TODO python-shaarli-client --format text option does not work
	# dirty workaround using jq json parser
	shaarli get-links --limit 100000 --searchtags music | \
		jq '.[] | {url: .url} | .[]' | sed 's/\"//g' >| "$exportfile"
}

function _download_music_links {
	# Download
	cat "$exportfile" | while read -r url; do
		echo "[archiver] $url" | tee -a "$logfile"
		# check URL against blacklist
		if egrep "^${url}$" "$blacklist"; then
			echo "[archiver] URL is in blacklist, skipping"
		else
			# download media with youtube-dl
			youtube-dl \
			$youtube_dl_extra_options \
			--extract-audio \
			--audio-format best \
			--download-archive music/youtube-dl.archive \
			"$url" \
			--output 'music/%(title)s-%(extractor)s-%(id)s.%(ext)s' 2>&1 | tee -a "$logfile"
		fi
		sleep "$wait_time"
	done
}

function _warn_on_errors {
	ytdl_errors=$(grep ERROR "$logfile"  |sort --unique)
	if [ ! "$ytdlerrors" == "" ]; then
		errorcount=$(echo "$ytdl_errors" | wc -l)
		echo "WARNING: there are $errorcount errors in $logfile:"
		echo "$ytdl_errors"
	fi
}

#############
# main loop

if [ ! -d "$outdir" ]; then mkdir -p "$outdir"; fi
date | tee -a "$logfile"

_install
_export_music_links
_download_music_links
_warn_on_errors
