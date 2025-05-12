from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

LESSONS = {
    1: {
        "prompt": "Which of this sets is Dogme 95?",
        "img1": "https://www.momendeavors.com/wp-content/uploads/2017/02/GuardiansVol2-On-Set.jpg",
        "img2": "https://static1.colliderimages.com/wordpress/wp-content/uploads/2022/08/idiotse.jpeg",
        "answer": "Real Location = Dogme 95"
    },
    2: {
        "prompt": "Which of these opening credits is Dogme 95?",
        "img1": "https://lh5.googleusercontent.com/proxy/jwzeWFdIrKD_cQGQO47stuP45PGYomKqVaAIQWDFGWitX80NI-gzleKBxSUAUu_Tq1SgEHIZwzew_9zzEmvD-KTJTtEa-VXD6fiW5CLWFKyBoUuDAUolqdva6gdJ8hE45Be14ObcJiD7IwzgoVMuHFbFmU7rbndFT3hEcqU7Hw",
        "img2": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIhFtvd2yi0fIh9gjxMOjv5M-7CAFJqEW69Q&s",
        "answer": "No Director Credit = Dogme 95"
    },
    3: {
        "prompt": "Which of this camera work is Dogme 95?",
        "img1": "https://s.studiobinder.com/wp-content/uploads/2020/06/What-is-a-Zoom-Shot-And-What-to-Consider-When-Using-One-Featured.jpg",
        "img2": "https://i.ytimg.com/vi/C1MqmlDeEH4/maxresdefault.jpg",
        "answer": "Handheld Shaky Cam = Dogme 95"
    },
    4: {
        "prompt": "Which of this light usage is Dogme 95?",
        "img1": "https://i.ytimg.com/vi/sWaPAQwDS5s/sddefault.jpg",
        "img2": "https://wdwmagic.twic.pics/ElementGalleryItems/attractions/Fullsize/Guardians-of-the-Galaxy_Full_48575.jpg?twic=v1",
        "answer": "Natural light = Dogme 95"
    },
    5: {
        "prompt": "Special Effects vs. Pure Realism (Use the slider to choose)",
        "img1": "https://metrograph.imgix.net/2023/05/TheIdiots_Still4.jpg?fm=pjpg&ixlib=php-3.3.1",
        "img2": "https://i.ytimg.com/vi/EIM78NrhixA/maxresdefault.jpg",
        "answer": "Drag Yellow Slider for Pure Realism"
    }
}

RULES = {
    1: {"title": "On-location shooting", "content": "Shooting must be done on location. Props and sets must not be brought in (if a particular prop is necessary for the story, a location must be chosen where this prop is to be found)."},
    2: {"title": "Sound with image", "content": "The sound must never be produced apart from the images or vice versa (Music must not be used unless it occurs where the scene is being shot)."},
    3: {"title": "Hand-held camera", "content": "The camera must be hand-held. Any movement or immobility attainable in the hand is permitted."},
    4: {"title": "Must be in color", "content": "The film must be in color. Special lighting is not acceptable (If there is too little light for exposure the scene must be cut or a single lamp be attached to the camera)."},
    5: {"title": "No filters", "content": "Optical work and filters are forbidden."},
    6: {"title": "No superficial action", "content": "The film must not contain superficial action (Murders, weapons, etc. must not occur)."},
    7: {"title": "No time/place distortion", "content": "Temporal and geographical alienation are forbidden (That is to say that the film takes place here and now)."},
    8: {"title": "No genre", "content": "Genre movies are not acceptable."},
    9: {"title": "Academy 35mm", "content": "The film format must be Academy 35 mm."},
    10:{"title": "No director credit", "content": "The director must not be credited."}
}
# immediately after your RULES dict:

RULE_IMAGES = {
    1: "https://upload.wikimedia.org/wikipedia/commons/f/fc/Mike_Chin_filming_on_location.jpg",
    2: "https://catalyst-magazine.org/wp-content/uploads/2020/05/3D-sound-header-01.png",
    3: "https://artlist.io/blog/wp-content/uploads/2019/12/Gabriel_Stella_-__ZAC0822_750x.jpg",
    4: "https://digitalsynopsis.com/wp-content/uploads/2016/05/cinema-palettes-famous-movie-colors-top-gun.jpg",
    5: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYy7RnO9o5vyPfa626Kx5_xD4eZk3wvPu9vQ&s",
    6: "https://static1.colliderimages.com/wordpress/wp-content/uploads/2022/08/Feston-Superficial-Acts.jpeg",
    7: "https://www.shutterstock.com/image-photo/spacetime-universe-scifi-concept-twist-260nw-2406288249.jpg",
    8: "https://upload.wikimedia.org/wikipedia/commons/4/42/LabelNoGenre.jpg",
    9: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/35_mm_film_%284-perf_Academy_Ratio%29.svg/640px-35_mm_film_%284-perf_Academy_Ratio%29.svg.png",
    10:"https://www.electric-shadows.com/wp-content/uploads/2020/05/Christopher-Nolan-directors-credit.jpg"
}


# … up above in server.py …

# 3️⃣ Directors & Films (slides 25–...)
DIRECTORS = {
    'Denmark': [
        {
            "id": 1,
            "name": "Thomas Vinterberg",
            "image": "https://m.media-amazon.com/images/M/MV5BMTNiYzMxZmMtYjUxNi00MmE0LTkyMzUtMGRkYzlkMzZkMjFjXkEyXkFqcGc@._V1_.jpg",
            "bio": [
                "Born 1969 in Frederiksberg, Denmark",
                "Co-founded Dogme 95 alongside Lars von Trier",
                "His directorial style is marked by emotional intensity, intimate camera work, and compelling explorations of family dynamics, societal pressures, and human vulnerability"
            ],
            "filmography": [
                "Festen (1998)",
                "Submarino (2010)",
                "The Hunt (2012)",
                "Far from the Madding Crowd (2015)",
                "Another Round (2020)"
            ],
            "films": ["Festen (1998)"]
        },
        {
            "id": 2,
            "name": "Lars von Trier",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZwlEuO1eeuHnJEMhD0x1XdCn6-1JyDeG0mA&s",
            "bio": [
                "Born 1956 in Lundtofte, Denmark",
                "Co-founded the Dogme 95 movement, advocating minimalistic, realistic filmmaking, rejecting elaborate special effects and promoting authenticity",
                "Known for his provocative style and experimental narratives"
            ],
            "filmography": [
                "The Element of Crime (1984)",
                "Epidemic (1987)",
                "Europa (1991)",
                "Breaking the Waves (1996)",
                "The Idiots (1998)",
                "Dancer in the Dark (2000)",
                "Dogville (2003)",
                "Manderlay (2005)",
                "The Boss of It All (2006)",
                "Antichrist (2009)",
                "Melancholia (2011)",
                "Nymphomaniac (2013)",
                "The House That Jack Built (2018)"
            ],
            "films": ["The Idiots (1998)"]
        },
        {
            "id": 3,
            "name": "Søren Kragh-Jacobsen",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8Dw7qXCfTjqLoPZ1aofAobHv2QGWLdtuITw&s",
            "bio": [
                "Born 1947 in Copenhagen, Denmark",
                "Emerged prominently with his contributions to the Dogme 95 movement",
                "His style emphasizes nuanced human relationships, combining sensitivity with social realism, and highlighting character-driven storytelling without artificial cinematic techniques"
            ],
            "filmography": [
                "Wanna See My Beautiful Navel? (1978)",
                "Thunderbirds (1983)",
                "Emma’s Shadow (1988)",
                "Shower of Gold (1988)",
                "The Boys from St. Petri (1991)",
                "The Island on Bird Street (1997)",
                "Mifune’s Last Song (1999)",
                "Skagerrak (2003)",
                "What No One Knows (2008)",
                "The Hour of the Lynx (2013)",
                "Oh, To Be a Butterfly (2020)"
            ],
            "films": ["Mifune’s Last Song (1999)"]
        }
    ],
    'USA': [
        {
            "id": 1,
            "name": "Harmony Korine",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPyCJRfcGUCqnsn0SzIEkpLaHLdZU8sCnVdg&s",
            "bio": [
                "Born 1973 in Bolinas, California",
                "Gained recognition for his provocative and experimental approach, often exploring marginalized, eccentric characters",
                "The showcase chaotic narratives, raw visuals, and confrontational realism earned him a reputation as an auteur of avant-garde cinema"
            ],
            "filmography": [
                "Gummo (1997)",
                "Julien Donkey-Boy (1999)",
                "Mister Lonely (2007)",
                "Trash Humpers (2009)",
                "Spring Breakers (2012)",
                "The Beach Bum (2019)"
            ],
            "films": ["Julien Donkey-Boy (1999)"]
        },
        {
            "id": 2,
            "name": "James Merendino",
            "image": "https://upload.wikimedia.org/wikipedia/commons/f/f7/James_Merendino_2.jpg",
            "bio": [
                "Born 1969 in Long Branch, New Jersey",
                "Best known for his energetic and subculture-focused style",
                "His work frequently blends dark humor with youthful rebellion, characterized by raw aesthetics and vibrant storytelling"
            ],
            "filmography": [
                "Beware of Dog (1993)",
                "Hard Drive (1994)",
                "Livers Ain’t Cheap (1996)",
                "River Made to Drown In (1997)",
                "SLC Punk! (1998)",
                "Amerikana (2000)",
                "Evil Remains (2001)",
                "Death Club (2008)",
                "The Invisible Life of Thomas Lynch (2009)",
                "Pox (2011)",
                "Punk’s Dead: SLC Punk 2 (2016)",
                "Double Proposal (2018)",
                "Ashes (2020)",
                "Cat in a Box (TBD)",
                "Arthur Kill Road (TBD)"
            ],
            "films": ["Amerikana (2000)"]
        },
{
            "id": 3,
            "name": "Rich Martini",
            "image": "https://m.media-amazon.com/images/M/MV5BMWVjZTg5YTctODY3Zi00MDFkLWFlMzAtYmZmYTkyY2Y2MzJmXkEyXkFqcGc@._V1_.jpg",
            "bio": [
                "Born 1955 in Northbrook, Illinois",
                "Known for blending documentary investigation with narrative fiction, often taking on multiple roles—writer, director, producer—in a single project",
                "Frequently explores metaphysical and cultural themes, bridging Hollywood storytelling with international art-house sensibilities"
            ],
            "filmography": [
                "Flipside: A Journey into the Afterlife (2012)",
                "Salt (2010)",
                "Amelia (2009)",
                "My Bollywood Bride (2006)",
                "Cowboy Up (2000)",
                "Camera – Dogme #15 (2001)",
                "Cannes Man (1997)",
                "Point of Betrayal (1996)",
                "Limit Up (1989)",
                "You Can't Hurry Love (1988)",
                "Three for the Road (1987)",
                "My Champion (year TBD)"
            ],
            "films": [
                "Camera (2000)"
            ]
        }    ]
}

# … rest of your Flask app …


FILM_IMAGES = {
    ('Denmark', 1, 0): "https://madmuseum.org/sites/default/files/styles/5_x_3/public/2014/11/Festen%2002-HERO.jpg",
    ('Denmark', 2, 0): "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTieTxFLEl-qtSEilaQ_H0YbE-h4VUx1WIZ6w&s",
    ('Denmark', 3, 0): "https://assets.mubicdn.net/images/film/24378/image-w856.jpg?1585120678",
    ('USA',     1, 0): "https://play-lh.googleusercontent.com/proxy/OCB1MlWEfshrn6NUr-V4WKfn4w7h7Xecdifi3ZvOlWlahMFq8nn1gIMq0IFDVuJ8t6JO2-lmXHA3YC6aAX8mcAjNlT9fPW6Pg25OwciDoDFSKzHZEg=s1920-w1920-h1080",
    ('USA',     2, 0): "https://media.senscritique.com/media/000006321430/375x230/amerikana.jpg",
    ('USA',     3, 0): "https://images.squarespace-cdn.com/content/v1/5abfa48c96e76ffee936efe1/1573768496848-CCSEGDZWUT4VLNKA59TG/Camera+by+Rich+Martini?format=2500w"
}
YOUTUBE_IDS = {
    ('Denmark', 1, 0): "BqlWIKwC2PE",    # Thomas Vinterberg
    ('Denmark', 2, 0): "xisKX3IVSzc",    # Lars von Trier
    ('Denmark', 3, 0): "CusoMGWCMnU",    # Søren Kragh-Jacobsen
    ('USA',     1, 0): "gZFCYRpm7a8",    # Harmony Korine
    ('USA',     2, 0): "9zwzwHcYuKg",    # James Merendino
    ('USA',     3, 0): "FLIpXsMpME4"     # Rich Martini
}

QUIZ = {
    1: {
        "prompt": "Which of these countries have Dogme 95 films? (Select all that apply)",
        "options": ["Denmark","USA","Canada","Mexico"],
        "answer": ["Denmark","USA"],
        "multi": True
    },
    2: {
        "prompt": "Which Dogme 95 Director Is This?",
        "img": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Harmony_Korine_at_81st_Venice_Film_Festival_%28cropped%29.jpg",
        "options": ["Harmony Korine","Rich Martini","Lars von Trier","Thomas Vinterberg"],
        "answer": "Thomas Vinterberg",
        "multi": False
    },
    3: {
        "prompt": "Which Dogme 95 Director Is This?",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Lars_von_Trier_2014_%28cropped%29.jpg/640px-Lars_von_Trier_2014_%28cropped%29.jpg",
        "options": ["Harmony Korine","Rich Martini","Lars von Trier","Thomas Vinterberg"],
        "answer": "Lars von Trier",
        "multi": False
    },
    4: {
        "prompt": "Which Dogme 95 Director Is This?",
        "img": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Thomas_Vinterberg_Berlinale_2010_%28cropped%29.jpg",
        "options": ["Harmony Korine","Rich Martini","Lars von Trier","Thomas Vinterberg"],
        "answer": "Harmony Korine",
        "multi": False
    },
    5: {
        "prompt": "Which Dogme 95 Film Is This?",
        "img": "/static/images/quiz_image1.png",
        "options": ["The Idiots","Julien Donkey-Boy","Festen","Amerikana"],
        "answer": "Julien Donkey-Boy",
        "multi": False
    },
    6: {
        "prompt": "Which Dogme 95 Film Is This?",
        "img": "/static/images/quiz_image2.png",
        "options": ["The Idiots","Julien Donkey-Boy","Festen","Amerikana"],
        "answer": "The Idiots",
        "multi": False
    },
    7: {"prompt": "Does Dogme 95 use artificial light?",   "options": ["True","False"], "answer": "False", "multi": False},
    8: {"prompt": "Does Dogme 95 use handheld shots?",      "options": ["True","False"], "answer": "True",  "multi": False},
    9: {"prompt": "Does Dogme 95 use fabricated sets?",    "options": ["True","False"], "answer": "False", "multi": False},
    10: {
        "prompt": "Drag all the following that are Dogme 95 rules into the box below:",
        "options": [
            "On-location shooting",        # real rule 1
            "Hand-held camera",            # real rule 3
            "No director credit",          # real rule 10
            "Use color filters",           # fake
            "Add background music",        # fake
            "Use special effects"          # fake
        ],

        "answer": [
            "On-location shooting",
            "Hand-held camera",
            "No director credit"
        ],
        "multi": True
    }
}

STREAM_INFO = {
    "The Idiots (1998)": "Amazon Prime",
    "Festen (1998)": "Mubi",
    "Mifune’s Last Song (1999)": "YouTube",
    "Julien Donkey-Boy (1999)": "Criterion",
    "Amerikana (2000)": "Amazon",
    "Camera (2000)": "Not available"
}

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def start():
    session.clear()
    session['started_at'] = datetime.now().isoformat()
    return render_template('start.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    lesson = LESSONS.get(lesson_id)
    session[f'learn_{lesson_id}_entered'] = datetime.now().isoformat()
    next_id = lesson_id + 1 if lesson_id < len(LESSONS) else None
    return render_template('learn.html', lesson=lesson, lesson_id=lesson_id, next_id=next_id)

@app.route('/rules')
def rules_list():
    # make sure we have our seen list in the session
    seen = session.get('seen_rules')
    if seen is None:
       session['seen_rules'] = []
       seen = []
    return render_template(
      'rules.html',
      rules=RULES,
      seen_rules=seen
    )

@app.route('/rules/<int:rule_id>')
def rule_detail(rule_id):
    rule = RULES.get(rule_id)
    prev_id = rule_id - 1 if rule_id > 1 else None
    next_id = rule_id + 1 if rule_id < len(RULES) else None
        # mark this rule as seen
    seen = session.get('seen_rules',[])
    if rule_id not in seen:
        seen.append(rule_id)
        session['seen_rules'] = seen
    rule_image = RULE_IMAGES.get(rule_id)
    return render_template(
        'rule_detail.html',
       rule=rule,        rule_id=rule_id,
        prev_id=prev_id,
        next_id=next_id,
        rule_image=rule_image
    )

@app.route('/directors')
def directors_map():
    return render_template('map.html')

@app.route('/directors/denmark')
def denmark():
    session['denmark_viewed_at'] = datetime.now().isoformat()
    return render_template('denmark.html', directors=DIRECTORS['Denmark'])

@app.route('/directors/usa')
def usa():
    return render_template('usa.html', directors=DIRECTORS['USA'])

@app.route('/directors/<country>/<int:dir_id>')
def director_detail(country, dir_id):
    key = 'USA' if country.lower() == 'usa' else country.title()
    directors_list = DIRECTORS.get(key, [])
    director = next((d for d in directors_list if d['id'] == dir_id), None)
    return render_template(
      'director_detail.html',
      director=director,
      country=key
    )


from flask import abort

@app.route('/directors/<country>/<int:dir_id>/film/<int:film_idx>')
def film_detail(country, dir_id, film_idx):
    # normalize country key
    key = 'USA' if country.lower() == 'usa' else country.title()
    directors_list = DIRECTORS.get(key, [])
    director = next((d for d in directors_list if d['id'] == dir_id), None)
    if not director or film_idx < 0 or film_idx >= len(director['films']):
        abort(404)

    # Get the right poster, falling back to empty
    poster_url = FILM_IMAGES.get((key, dir_id, film_idx), "")

    # *** KEEP the original theatre background URL here ***
    background_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzk4YLvofhGLJ7-TOiXiiqLh9LvDgPNr4zFA&s"
    video_id = YOUTUBE_IDS.get((key, dir_id, film_idx))

    return render_template(
      'movie_detail.html',
      director=director,
      country=key,
      dir_id=dir_id,
      film_title=director['films'][film_idx],
      poster_url=poster_url,
      background_url=background_url,
      video_id=video_id
   )

@app.route('/save_movie', methods=['POST'])
def save_movie():
    title = request.form.get('title')
    saved = session.get('saved_movies', [])
    if title and title not in saved:
        saved.append(title)
        session['saved_movies'] = saved
    return ('', 204)


@app.route('/quiz/<int:q_id>', methods=['GET','POST'])
def quiz_question(q_id):
    if 'answers' not in session:
        session['answers'] = {}
    if request.method=='POST':
        ans = request.form.getlist('choice') if QUIZ[q_id]['multi'] else request.form.get('choice')
        session['answers'][str(q_id)] = ans
        next_q = q_id + 1
        if next_q <= len(QUIZ):
            return redirect(url_for('quiz_question', q_id=next_q))
        else:
            return redirect(url_for('quiz_result'))
    question = QUIZ.get(q_id)
    return render_template('quiz_question.html', question=question, q_id=q_id, total=len(QUIZ))

@app.route('/quiz/result')
def quiz_result():
    answers = session.get('answers', {})
    score = 0
    for qid, resp in answers.items():
        correct = QUIZ[int(qid)]['answer']
        if isinstance(correct, list):
            score += set(resp) == set(correct)
        else:
            score += (resp == correct)

    # Get saved titles from session
    saved = session.get('saved_movies', [])

    # Build detailed info for each saved title
    saved_info = []
    for title in saved:
        platform = STREAM_INFO.get(title, "Not available")
        saved_info.append({
            "title": title,
            "platform": platform
        })

    return render_template(
        'quiz_result.html',
        score=score,
        total=len(QUIZ),
        saved_info=saved_info
    )

if __name__ == '__main__':
   app.run(debug = True, port=5001)




