import webbrowser
import os
import re

main_page_head = ''
main_page_content = ''
movie_tile_content = ''

def create_movie_tiles_content(movies):
    content = ''
    for movie in movies:
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+',
                                                         movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None
        content += movie_tile_content.format(
            movie_title=movie.title,
            movie_storyline=movie.storyline,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            movie_release_date=movie.release_date
        )
    return content

def open_movies_page(movies):
    output_file = open('fresh_tomatoes.html', 'w')
    rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))
    output_file.write(main_page_head + rendered_content)
    output_file.close()
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2) 
