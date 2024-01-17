from tkinter import *
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageDraw
from tmdbv3api import TMDb, Movie
import requests
import io

root = Tk()
root.title("NestFlix App")

# Initialize TMDb API
tmdb = TMDb()
tmdb.api_key = '6009b11afc8bcef52fe3d9b47ad03d7e'


# Home Page

logo_img = None

def home_page():
    home_frame = Frame(body_screen, bg="#A9B1A7")

    def display_logo():
        global logo_img
        logo_img = ImageTk.PhotoImage(Image.open("Images/logo.png"))
        logo_image = Label(home_frame, image=logo_img, borderwidth=0).pack()

    display_logo()
    description = "Explore, Discover, and Enjoy the World of Movies with our Movie App. Access trending, top-rated movies, and search for your favorites with ease. Your gateway to a cinematic journey!"
    description_label = Label(home_frame, text=description, font=("Montserrat", 15, "bold"), bg="#A9B1A7", padx=10, pady=10, wraplength=600)
    description_label.pack()
    Label(home_frame, text="Made by Abdulrahman Kallarakkal", font=("Montserrat", 11), bg="#A9B1A7", padx=10, pady=100).pack()
    
    home_frame.pack(pady=20)


# Search Page
    
def search_page():
    search_results = []
    crn_index_result = 0

    # Function to get the user's query and provide results
    def search_movie():
        nonlocal search_results
        query = search_entry.get()

        if query:
            movie = Movie()
            search_results = movie.search(query)

            # To display the number of results
            times_amount.config(text=f"Results: {crn_index_result + 1} of {len(search_results)}")
        
            if search_results:
                movie_id = search_results[0].id
                display_movie_details(movie_id)
                load_and_display_poster(movie_id)

    # Function to load and display movie details
    def display_movie_details(movie_id):
        nonlocal crn_index_result
        movie = Movie()
        selected_movie = movie.details(movie_id)

        details_text.config(state=NORMAL)
        details_text.delete(1.0, END)

        details_text.insert(END, f"\n{selected_movie.title}\n")
        details_text.tag_add("title", "2.0", "2.end")
        details_text.tag_config("title", font=("Montserrat", 22, "bold"))

        details_text.tag_configure("custom_font", font=("Montserrat", 11))
        details_text.insert(END, f"\nRating: {selected_movie.vote_average}\n", "custom_font")
        details_text.insert(END, f"Release Date: {selected_movie.release_date}\n", "custom_font")
        details_text.insert(END, f"Duration: {selected_movie.runtime} min\n\n", "custom_font")
        details_text.insert(END, f"{selected_movie.overview}\n\n", "custom_font")
        details_text.insert(END, f"Country: {', '.join([country.name for country in selected_movie.production_countries])}\n", "custom_font")
        details_text.insert(END, f"Genre: {', '.join([genre.name for genre in selected_movie.genres])}\n", "custom_font")

        if selected_movie.release_date:
            details_text.insert(END, f"Release: {selected_movie.release_date}\n", "custom_font")

        credits = movie.credits(movie_id)
        details_text.insert(END, f"Director: {', '.join([director.name for director in credits['crew'] if director['job'] == 'Director'])}\n", "custom_font")
        details_text.insert(END, f"Production: {', '.join([company.name for company in selected_movie.production_companies])}\n", "custom_font")
        details_text.config(state=DISABLED)

    # Function to load and display movie poster
    def load_and_display_poster(movie_id):
        nonlocal crn_index_result
        movie = Movie()
        selected_movie = movie.details(movie_id)
        movie_image = selected_movie.poster_path

        if movie_image:
            poster_url = f"https://image.tmdb.org/t/p/w500/{movie_image}"
            pick = requests.get(poster_url)
            img = Image.open(io.BytesIO(pick.content))
            img = img.resize((240, 370), Image.BICUBIC)
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            radius = 10 
            draw.rounded_rectangle([(0, 0), img.size], radius, fill=255)
            img.putalpha(mask)
            img = ImageTk.PhotoImage(img)
            movie_area.config(image=img)
            movie_area.image = img

        else:
            movie_area.config(image="")
            movie_area.image = None

    # Function to add a background image to the page
    def set_background():
        background_img = Image.open("Images/Search_bg.png")
        new_size = (body_screen.winfo_reqwidth(), body_screen.winfo_reqheight())
        background_img = background_img.resize(new_size, Image.BICUBIC)
        background_img = ImageTk.PhotoImage(background_img)
        canvas.grid(row=0, column=0, rowspan=6, columnspan=6, sticky="nsew")
        canvas.create_image(0, 0, anchor=NW, image=background_img)
        canvas.background = background_img

    search_frame = Frame(body_screen, bg="#A9B1A7")
    search_frame.pack(side=LEFT)
    search_frame.pack_propagate(False)
    search_frame.configure(width=710, height=665)
    canvas = Canvas(search_frame, highlightthickness=0, bg="#A9B1A7")
    set_background()

    # Movie Poster Area
    movie_area = Label(search_frame, text="Poster will be displayed here", font=("Montserrat", 10), bg="#A9B1A7")
    movie_area.grid(row=1, column=0, rowspan=3, padx=10, pady=5)

    # Adding empty columns to center the widgets
    search_frame.columnconfigure(1, weight=1)
    search_frame.columnconfigure(2, weight=1)
    search_frame.columnconfigure(3, weight=1)

    # Search Entry and Button
    search_entry = Entry(search_frame, font=("Montserrat", 15), width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    search_button = Button(search_frame, text="Search", font=("Montserrat", 13), width=10, command=search_movie, bg="#697664", fg="#EAEBE9")
    search_button.grid(row=0, column=2, padx=10, pady=10)

    # Results Label
    times_amount = Label(search_frame, text="", font=("Montserrat", 12), bg="#A9B1A7")
    times_amount.grid(row=1, column=1, columnspan=3, pady=5)

    # Movie Details Area
    details_text = Text(search_frame, wrap=WORD, width=50, height=25, borderwidth=0, highlightbackground="#697664", highlightthickness=1, bg="#A9B1A7")
    details_text.grid(row=2, column=1, columnspan=3, padx=5, pady=10)

    # Next and Previous Buttons
    next_button = Button(search_frame, text=">", command=lambda: next_result(), bg="#697664", fg="#EAEBE9", font=("Bold", 13), width=5)
    prev_button = Button(search_frame, text="<", command=lambda: prev_result(), bg="#697664", fg="#EAEBE9", font=("Bold", 13), width=5)
    prev_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    next_button.grid(row=3, column=1, padx=15, pady=5)

    def next_result():
        nonlocal crn_index_result
        if crn_index_result < len(search_results) - 1:
            crn_index_result += 1
            display_movie_details(search_results[crn_index_result].id)
            load_and_display_poster(search_results[crn_index_result].id)
            times_amount.config(text=f"Results: {crn_index_result + 1} of {len(search_results)}")

    def prev_result():
        nonlocal crn_index_result
        if crn_index_result > 0:
            crn_index_result -= 1
            display_movie_details(search_results[crn_index_result].id)
            load_and_display_poster(search_results[crn_index_result].id)
            times_amount.config(text=f"Results: {crn_index_result + 1} of {len(search_results)}")

    search_frame.pack(pady=20)


#  Trending

# Function to display movie posters for the list of movies
def display_poster(poster_url, title, row_index, col_index):
    pick = requests.get(poster_url)

    if pick.status_code == 200:
        img = Image.open(io.BytesIO(pick.content))
        img = img.resize((150, 250), Image.BICUBIC)
        photo = ImageTk.PhotoImage(img)
        movie_info = Label(body_screen, image=photo)
        movie_info.grid(row=row_index * 2, column=col_index, padx=10, pady=10)
        title_label = Label(body_screen, text=title, font=("Montserrat", 13), bg="#A9B1A7")
        title_label.grid(row=row_index * 2 + 1, column=col_index, padx=10, pady=5)
        movie_info.image = photo

    else:
        Label(body_screen, text="Poster not available").grid(row=row_index * 2, column=col_index, padx=10, pady=10)

# Function to load trending movies list
def load_trending():
    trending_movies = Movie().popular()
    limited_movies = []

    for movie in trending_movies:
        limited_movies.append(movie)
        if len(limited_movies) == 8:
            break

    if trending_movies:
        row_index = 1
        col_index = 0
        trending_heading = Label(body_screen, text="Trending Movies:", font=("Montserrat", 15, "bold"), bg="#A9B1A7")
        trending_heading.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        for movie in trending_movies:
            title = movie.title
            movie_img = movie.poster_path

            if movie_img:
                poster_url = f"https://image.tmdb.org/t/p/w500/{movie_img}"
                display_poster(poster_url, title, row_index, col_index)

            col_index += 1
            if col_index == 4:
                col_index = 0
                row_index += 1
                if row_index > 2:
                    break

def trending_page():
    trending_frame = Frame(body_screen)
    load_trending()

    trending_frame.pack(pady=20)


# Top Rated Page
    
# Function to display movie posters for the list of movies
def display_top_rated_poster(poster_url, title, row_index, col_index):
    pick = requests.get(poster_url)

    if pick.status_code == 200:
        img = Image.open(io.BytesIO(pick.content))
        img = img.resize((150, 250), Image.BICUBIC)
        photo = ImageTk.PhotoImage(img)
        movie_info = Label(body_screen, image=photo)
        movie_info.grid(row=row_index * 2, column=col_index, padx=10, pady=10)
        title_label = Label(body_screen, text=title, font=("Montserrat", 11), bg="#A9B1A7")
        title_label.grid(row=row_index * 2 + 1, column=col_index, padx=10, pady=5)
        movie_info.image = photo

    else:
        Label(body_screen, text="Poster not available").grid(row=row_index * 2, column=col_index, padx=10, pady=10)

# Function to load top rated movies list
def load_top_rated():
    top_rated_movies = Movie().top_rated()
    limited_movies = []

    for movie in top_rated_movies:
        limited_movies.append(movie)
        if len(limited_movies) == 8:
            break

    if top_rated_movies:
        row_index = 1
        col_index = 0
        toprated_heading = Label(body_screen, text="Top Rated Movies:", font=("Montserrat", 15, "bold"), bg="#A9B1A7")
        toprated_heading.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        for movie in top_rated_movies:
            title = movie.title
            movie_img = movie.poster_path

            if movie_img:
                poster_url = f"https://image.tmdb.org/t/p/w500/{movie_img}"
                display_top_rated_poster(poster_url, title, row_index, col_index)

            col_index += 1
            if col_index == 4:
                col_index = 0
                row_index += 1
                if row_index > 2:
                    break

def toprated_page():
    global toprated_frame
    toprated_frame = Frame(body_screen)
    load_top_rated()

    toprated_frame.pack(pady=20)


# Navigation Menu

# Function to erase the pages already viewed
def clear_screens():
    for frame in body_screen.winfo_children():
        frame.destroy()

# Function to hide the indicators for the navigation menu
def marking():
    home_mark.config(bg="#283B22")
    search_mark.config(bg="#283B22")
    trending_mark.config(bg="#283B22")
    toprated_mark.config(bg="#283B22")

# Function to indicate for the navigation menu
def mark(lb, page):
    marking()
    lb.config(bg="#A9B1A7")
    clear_screens()
    page()

navigation = Frame(root, bg="#283B22")

# Function to display the logo in the navigation menu
def display_nav_logo():
    global logo_img
    try:
        pil_image = Image.open("Images/nav_logo.png")
        pil_image = pil_image.resize((120, 130), Image.BICUBIC)
        logo_img = ImageTk.PhotoImage(master=navigation, image=pil_image)
        logo_label = Label(navigation, image=logo_img, borderwidth=0)
        logo_label.image = logo_img
        logo_label.place (y=15)
    except Exception as e:
        print(f"Error loading logo: {e}")

display_nav_logo()

# Adding Labels, Buttons, and the Main Frame
home_btn = Button(navigation, text="Home", font=("Montserrat", 15), fg="#A9B1A7",
                     bd=0, bg="#283B22", command=lambda: mark(home_mark, home_page))
home_btn.place(x=10, y=240)

home_mark = Label(navigation, text='', bg="#283B22")
home_mark.place(x=3, y=240, width=5, height=40)

search_btn = Button(navigation, text="Search", font=("Montserrat", 15), fg="#A9B1A7",
                     bd=0, bg="#283B22", command=lambda: mark(search_mark, search_page))
search_btn.place(x=10, y=290)

search_mark = Label(navigation, text='', bg="#283B22")
search_mark.place(x=3, y=290, width=5, height=40)

trending_btn = Button(navigation, text="Trending", font=("Montserrat", 15), fg="#A9B1A7",
                   bd=0, bg="#283B22", command=lambda: mark(trending_mark, trending_page))
trending_btn.place(x=10, y=340)

trending_mark = Label(navigation, text='', bg="#283B22")
trending_mark.place(x=3, y=340, width=5, height=40)

toprated_btn = Button(navigation, text="Top Rated", font=("Montserrat", 15), fg="#A9B1A7",
                       bd=0, bg="#283B22", command=lambda: mark(toprated_mark, toprated_page))
toprated_btn.place(x=10, y=390)

toprated_mark = Label(navigation, text='', bg="#283B22")
toprated_mark.place(x=3, y=390, width=5, height=40)

navigation.pack(side=LEFT)
navigation.pack_propagate(False)
navigation.configure(width=120, height=670)

body_screen = Frame(root, highlightbackground="#A9B1A7", highlightthickness=3, bg="#A9B1A7")
body_screen.pack(side=RIGHT)
body_screen.pack_propagate(False)
body_screen.configure(width=710, height=670)

home_page()


root.mainloop()
