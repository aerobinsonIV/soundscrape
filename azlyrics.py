def get_lyrics_azlyrics(artist, title):

    search_soup = soup_url(f'https://search.azlyrics.com/search.php?q={artist}+{title}')
    
    # Find bold tags
    bolds = search_soup.find_all('b')

    for bold in bolds:
        # Song results pane is labelled by a b tag with this text
        if bold.text == "Song results:":
            song_results_pane = bold.parent.parent
            break
        
    if not ('song_results_pane' in locals()):
        # Couldn't find this song
        return None

    # Find anchor tags
    anchors = song_results_pane.find_all('a')

    found_result = False
    best_confidence = 0

    for anchor in anchors:
        # Valid links to lyrics pages have format like '1. "Breathe" - Mako'. All other a tags don't have periods.
        if("." in anchor.text):

            # just be happy it's not regex
            a_title = anchor.text[4:anchor.text[4:].find("\"") + 4].strip().lower()
            a_artist = anchor.text[anchor.text[1:].find("-") + 3:].strip().lower()

            confidence = match_confidence(title, artist, a_title, a_artist)
            if confidence > best_confidence:
                best_url = anchor['href']
                best_confidence = confidence
            
            # We found at least one result
            found_result = True

    if not found_result:
        return None

    if best_confidence == 0:
        # None of the results were even close
        return None

    print(best_url)

    # Get lyrics page from link that best matched input title and artist
    lyrics_soup = soup_url(best_url)

    # The lyrics section is a div.
    divs = lyrics_soup.find_all('div')

    # The div containing the lyric starts with this comment
    licensing_comment_text = ' Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. '
    
    for i, div in enumerate(divs):
        
        # Get all comments in this div
        comments = div.find_all(string=lambda text: isinstance(text, Comment))
        
        # If the div has a comment, it might be our target div
        if(len(comments) > 0):
            # Check if the first comment is the licensing warning
            if(comments[0] == licensing_comment_text):
                
                divs_in_lyric_div_candidate = div.find_all('div')

                # The lyrics div has no divs nested inside it
                if(len(divs_in_lyric_div_candidate) == 0):
                    # If we've passed all these tests, we definetly have the lyrics
                    return div.text.strip()

    return ""