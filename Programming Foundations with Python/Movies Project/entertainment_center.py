__author__ = 'Maycon'

import media
import fresh_tomatoes

toy_story = media.Movie("Toy Story",
                        "A Story of a boy and his toys that came to life",
                        "http://upload.wikimedia.orr/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=vwyZH85NQC4")

avatar = media.Movie("Avatar",
                     "A marine on an alien planet",
                     "http://upload.wikimedia.orr/wikipedia/id/b/bo/Avatar_Teaser_Poster.jpg",
                     "https://www.youtube.com/watch?v=-9ceBgWV8io")

#print(toy_story.storyline)
#print(avatar.storyline)
#avatar.show_trailer()

#movies = [toy_story, avatar]
#fresh_tomatoes.open_movies_page(movies)
print(media.Movie.__doc__)
print(media.Movie.__name__)
print(media.Movie.__module__)