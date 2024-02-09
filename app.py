from cs50 import SQL
from datetime import datetime
from flask import Flask, current_app as app, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import os
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import allowed_file, apology, art_scene_options, login_required, slugify, state_options # Anything else


app = Flask(__name__)

app.jinja_env.filters['slugify'] = slugify

# Configure session to use filesystem
# Sets session to the browsing length only
app.config["SESSION_PERMANENT"] = False
# This means that session data will be stored on the server's file system.
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Use SQLite database (this is the cs50 way of opening the database)
db = SQL("sqlite:///artfinity.db")

# Define UPLOAD_FOLDER
BASE_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'IMAGES')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])




@app.after_request
def after_request(response):
    """Ensures the responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return(response)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
<<<<<<< Updated upstream
        return render_template("home.html")


@app.route("/art")
def art():
    # Fetch all art from the database
    all_art = db.execute("SELECT * FROM Art")
=======
        # Fetch all art from the database
        all_art = db.execute("SELECT * FROM Art ORDER BY RANDOM() LIMIT 6")
        users = db.execute("SELECT user_id, username, artist_name, profile_picture_url FROM Users ORDER BY RANDOM() LIMIT 6")
        scenes = db.execute("SELECT * FROM Scenes ORDER BY RANDOM() LIMIT 6")

        return render_template("home.html", all_art=all_art or [], scenes=scenes or [], users=users or [])



@app.route("/art")
def all_artworks():
    all_art = db.execute("""
        SELECT Art.title, Art.image_url, Users.artist_name
        FROM Art
        JOIN UserArt ON Art.art_id = UserArt.art_id
        JOIN Users ON UserArt.user_id = Users.user_id
        ORDER BY Art.title
    """)
    # Process each artwork to include a URL path or complete URL
    for art in all_art:
        slugged_title = (art['title'])
        slugged_artist_name = slugify(art['artist_name'])
        # Construct the path or URL here
        art['url'] = f"/art/{slugged_artist_name}/{slugged_title}"

    return render_template("art.html", all_art=all_art)
 

@app.route("/art/<artist_name>/<art_title>")
def artwork(artist_name, art_title):
    search_artist_name = artist_name.replace("-", " ").replace("_", " ")
    search_title = art_title

    query = """
        SELECT Art.*, Users.username, Users.artist_name
        FROM Art
        INNER JOIN UserArt ON Art.art_id = UserArt.art_id
        INNER JOIN Users ON UserArt.user_id = Users.user_id
        WHERE LOWER(Users.artist_name) LIKE LOWER(?) AND LOWER(Art.title) LIKE LOWER(?)
    """
    art_details = db.execute(query, "%" + search_artist_name + "%", "%" + search_title + "%")

    if art_details:
        # Assuming you want to display the first match or a specific artwork
        art_detail = art_details[0] if art_details else None
        
        # Generate the URL for the artwork's image
        image_url = url_for('static', filename=art_detail['image_url'])
        
        # Pass the image URL along with other artwork details to the HTML template
        return render_template("artwork.html", art_detail=art_detail, image_url=image_url)
    else:
        return "Artwork not found", 404




>>>>>>> Stashed changes



@app.route("/artists")
def artists():
    # Fetch all users' profile picture URLs and other relevant info from the database
    users = db.execute("SELECT user_id, username, artist_name, profile_picture_url FROM Users")

    # Render the template, passing the users data
    return render_template("artists.html", users=users)



@app.route("/artists/<artist_name>")
def artist_profile(artist_name):
    artist_info = db.execute("SELECT * FROM Users WHERE artist_name = :artist_name", artist_name=artist_name)
    artist_info = artist_info[0]

    if not artist_info:
        return "Artist not found", 404
    print(type(artist_info))

    return render_template("artist_profile.html", artist_info=artist_info)
    




@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "GET":
        return render_template("checkout.html")
    

@app.route("/create_artist_profile", methods=["GET", "POST"])
def create_artist_profile():
    if request.method == "POST":

        # Define varaibles
        artist_name = request.form.get("artist_name")
        short_bio = request.form.get("short_bio")
        long_bio = request.form.get("long_bio")
        media_link1 = request.form.get("media_link1")
        media_link2 = request.form.get("media_link2")
        media_link3 = request.form.get("media_link3")
        media_link4 = request.form.get("media_link4")

        # Save the profile information to the database
        db.execute("INSERT INTO Artists (artist_name, short_bio, long_bio, media_link1, media_link2, media_link3, media_link4) VALUES (?, ?, ?, ?, ?, ?, ?)", artist_name, short_bio, long_bio, media_link1, media_link2, media_link3, media_link4)

        return redirect(url_for('artist_profile'))
    
    else:
        return render_template("create_artist_profile.html")


@app.route("/delete-art/<int:art_id>")
def delete_art(art_id):
    # Authentication and authorization checks go here

    # Delete the entry from the UserArt table
    db.execute("DELETE FROM UserArt WHERE art_id = :art_id", art_id=art_id)

    # Delete the entry from the Art table
    db.execute("DELETE FROM Art WHERE art_id = :art_id", art_id=art_id)

    # Redirect back to the profile page or another appropriate page
    return redirect(url_for('profile'))


@app.route("/edit_artist_profile", methods=["GET", "POST"])
def edit_artist_profile():
    if request.method == "POST":

        # Define varaibles
        artist_name = request.form.get("artist_name")
        city = request.form.get("city")
        short_bio = request.form.get("short_bio")
        long_bio = request.form.get("long_bio")
        media_link1 = request.form.get("media_link1")
        media_link2 = request.form.get("media_link2")
        media_link3 = request.form.get("media_link3")
        media_link4 = request.form.get("media_link4")

        if 'user_id' in session:
            user_id = session['user_id']

            # Check if the record already exists in the database
            existing_record = db.execute("SELECT * FROM Users WHERE user_id = ?", user_id)

            if existing_record:
                # If the record exists, update it
                db.execute("UPDATE Users SET artist_name = ?, city = ?, long_bio = ?, media_link1 = ?, media_link2 = ?, media_link3 = ?, media_link4, state = ?, country = ?, zip = ?, phone = ? WHERE user_id = ?", email, first_name, last_name, address_line1, address_line2, city, state, country, zip_code, phone, user_id)
            else:
                # If the record does not exist, insert it
                db.execute("INSERT INTO Users (email, first_name, last_name, address_line1, address_line2, city, state, country, zip, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", email, first_name, last_name, address_line1, address_line2, city, state, country, zip_code, phone)

        return redirect(url_for('artist_profile'))
    
    elif request.method == "GET":
        if 'user_id' in session:
            user_id = session['user_id']

            user_info = db.execute("SELECT * FROM Artists WHERE user_id = ?", user_id)

            if user_info:
                return render_template("edit_artist_profile.html", user_info=user_info, city_options=city_options)
            else:
                # Handle case when user_info is not found
                return apology("User information not found", 404)
        else:
            return redirect("login.html")
    



@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if request.method== "POST":
        if 'user_id' in session:
            user_id = session['user_id']

        # Define variables
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        address_line1 = request.form.get("address_line1")
        address_line2 = request.form.get("address_line2")
        city = request.form.get("city")
        state = request.form.get("state")
        country = request.form.get("country")
        zip_code = request.form.get("zip_code")
        phone = request.form.get("phone")
        email = request.form.get("email")
        artist_name = request.form.get("artist_name")
        long_bio = request.form.get("long_bio")
        genres = request.form.get("genres")
        media_link1 = request.form.get("media_link1")
        media_link2 = request.form.get("media_link2")
        media_link3 = request.form.get("media_link3")
        media_link4 = request.form.get("media_link4")

        scene_id = request.form.get("scene_id")
        print(scene_id)


        # Construct the path for the user's upload folder
        user_upload_folder = os.path.join(BASE_UPLOAD_FOLDER, artist_name)

        # Check if this folder exists, create it if not
        if not os.path.exists(user_upload_folder):
            os.makedirs(user_upload_folder)


        image_file = request.files['profile_picture_url']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if image_file.filename == '':
            return redirect(request.url)

        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            # Create a subdirectory for the user inside 'static/images'
            user_folder = os.path.join('images', str(user_id))
            full_folder_path = os.path.join(app.static_folder, user_folder)

            if not os.path.exists(full_folder_path):
                os.makedirs(full_folder_path)

            # Save the file
            save_path = os.path.join(full_folder_path, filename)
            image_file.save(save_path)
            # Relative path to be stored in the database
            relative_path = os.path.join(user_folder, filename)


            # Check if the record already exists in the database
            existing_record = db.execute("SELECT * FROM Users WHERE user_id = ?", user_id)

            if existing_record:
                # If the record exists, update it
                db.execute("UPDATE Users SET scene_id = ?, profile_picture_url = ?, email = ?, first_name = ?, last_name = ?, address_line1 = ?, address_line2 = ?, city = ?, state = ?, country = ?, zip_code = ?, phone = ?, artist_name = ?, long_bio = ?, genres = ?, media_link1 = ?, media_link2 = ?, media_link3 = ?, media_link4 = ? WHERE user_id = ?", scene_id, relative_path, email, first_name, last_name, address_line1, address_line2, city, state, country, zip_code, phone, artist_name, long_bio, genres, media_link1, media_link2, media_link3, media_link4, user_id)
            else:
                # If the record does not exist, insert it
                db.execute("INSERT INTO Users (scene_id, profile_picture_url, email, first_name, last_name, address_line1, address_line2, city, state, country, zip_code, phone, artist_name, long_bio, genres, media_link1, media_link2, media_link3, media_link4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", scene_id, relative_path, email, first_name, last_name, address_line1, address_line2, city, state, country, zip_code, phone, artist_name, long_bio, genres, media_link1, media_link2, media_link3, media_link4)


            return redirect(url_for("profile"))
        else:
            return redirect("login.html")
        
    elif request.method == "GET":
        if 'user_id' in session:
            user_id = session['user_id']

            # Fetch the profile picture URL from the database
            profile_picture_result = db.execute("SELECT profile_picture_url FROM Users WHERE user_id = ?", (user_id,))
            if profile_picture_result:
                profile_picture_url = profile_picture_result[0]['profile_picture_url']
            else:
                profile_picture_url = None  # Default or placeholder image URL

            user_info = db.execute("SELECT * FROM Users WHERE user_id = ?", user_id)
            scenes = db.execute("SELECT * FROM Scenes")

            art_scene_options = {scene['scene_id']: scene for scene in scenes}

            if user_info:
                # user_info = user_info[0]
                return render_template("edit_profile.html", user_info=user_info, scenes=scenes, state_options=state_options, art_scene_options=art_scene_options, profile_picture_url=profile_picture_url)
            else:
                # Handle case when user_info is not found
                return apology("User information not found", 404)
        else:
            return redirect("login.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user id
    session.clear()

    if request.method == "POST":
        # Ensure email and password are submitted
        if not request.form.get("email"):
            return apology("Please enter your email", 404)
        elif not request.form.get("password"):
            return apology("Please enter your password", 404)
        
        # Query the database for the email
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        if len(rows) != 1:
            return apology("email address not yet registered, go to register")

        # Ensure the password is correct
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid email and/or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    # Forget any user id
    session.clear()
    return render_template("home.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        if 'user_id' in session:
            user_id = session['user_id']

            # Fetch the profile picture URL from the database
            profile_picture_result = db.execute("SELECT profile_picture_url FROM Users WHERE user_id = ?", (user_id,))
            if profile_picture_result:
                profile_picture_url = profile_picture_result[0]['profile_picture_url']
            else:
                profile_picture_url = None  # Default or placeholder image URL


            user_info = db.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))

            # Fetch user information and their associated scene information
            user_info_result = db.execute("""
                SELECT Users.*, Scenes.scene_city_name, Scenes.scene_city_picture, Scenes.scene_city_description 
                FROM Users
                LEFT JOIN Scenes ON Users.scene_id = Scenes.scene_id
                WHERE Users.user_id = ?
                """, (user_id,))
            user_info = user_info_result if user_info_result else None
            print(user_info)



            #####

            # Fetch art associated with the user through UserArt
            art_query_result = db.execute("""
                SELECT Art.* 
                FROM Art 
                JOIN UserArt ON Art.art_id = UserArt.art_id 
                WHERE UserArt.user_id = ?
                """, (user_id,))

            # Prepare a list of image URLs for Artwork
            image_urls = [art['image_url'] for art in art_query_result] if art_query_result else []

            if user_info:
                return render_template("profile.html", art_scene_options=art_scene_options, user_info=user_info, profile_picture_url=profile_picture_url, image_urls=image_urls, state_options=state_options)
            else:
                # Handle case when user_info is not found
                return apology("User information not found", 404)
            
        else:
            return redirect("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user id
    session.clear()

    if request.method == "POST":
        # Ensure email, password and password confirmation are submitted
        if not request.form.get("email"):
            return apology("must provide email", 404)
        if not request.form.get("password"):
            return apology("must provide password", 404)
        if not request.form.get("password_confirmation"):
            return apology("must provide password confirmation", 404)

        # Define varaibles
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

    # OK to have multiple of the same username but must be a unique email
        # Check db to see if email address is unique
        rows = db.execute("SELECT * FROM Users WHERE email = ?", email)
        if len(rows) > 0:
            return apology("This email is already registered, please login or register with a different email address")
        
    # Require user passwords to be more complex
        if len(password) < 6:
            return apology("Password must contain 6-20 characters", 400)
        if not any(char.isdigit() for char in password):
            return apology("Password must contain at least one number", 400)
        
    # Ensure password and password_confirmation match
        if password != password_confirmation:
            return apology("Password and it's confirmation do not match, please try one more time, you can do it", 400)
    
    # Hash the password
        hashpassword = generate_password_hash(password)

    # Submit email and password to the database
        db.execute("INSERT INTO Users (email, hash) VALUES (?, ?)", email, hashpassword)

    # Remember which user has logged in
        new_user = db.execute("SELECT user_id FROM Users WHERE email = ?", email)
        user_id = new_user[0]["user_id"]
        session["user_id"] = user_id

    # Redirect user to homepage (or make an artist profile)
        return redirect("/")

    else:
        return render_template("register.html")
    

@app.route("/scenes", methods=["GET", "POST"])
def scenes():
    if request.method == "GET":
        scenes = db.execute("SELECT * FROM Scenes")

        return render_template("scenes.html", scenes=scenes)
    


@app.route("/scene_art/<int:scene_id>")
def scene_art(scene_id):
    art = db.execute("""
        SELECT Art.* FROM Art
        JOIN Users ON Art.user_id = Users.user_id
        WHERE Users.scene_id = :scene_id
    """, {"scene_id": scene_id})
    return render_template("scene_art.html", art=art)



@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        if 'user_id' in session:
            user_id = session['user_id']
            return render_template("upload.html")
        else:
            return redirect("/login")

    elif request.method == "POST":
        if 'user_id' in session:
            user_id = session['user_id']

            # Retrieve artist_name from the database
            artist_row = db.execute("SELECT artist_name FROM Users WHERE user_id = :user_id", user_id=user_id)
            if artist_row and artist_row[0]['artist_name']:
                artist_name = artist_row[0]['artist_name']  # Extracting artist_name
            else:
                # Handle the case where artist_name is not found
                return "Artist not found", 404

            # Check if the post request has the file part
            if 'image_url' not in request.files:
                return redirect(request.url)
            image_file = request.files['image_url']

             # Validate the file before saving
            if image_file and allowed_file(image_file.filename):

                # Construct the path for the user's upload folder
                user_upload_folder = os.path.join(BASE_UPLOAD_FOLDER, artist_name)

            # Check if this folder exists, create it if not
            if not os.path.exists(user_upload_folder):
                os.makedirs(user_upload_folder)

            # Check if the post request has the file part
            if 'image_url' not in request.files:
                return redirect(request.url)
            image_file = request.files['image_url']

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if image_file.filename == '':
                return redirect(request.url)

            if image_file:
                filename = secure_filename(image_file.filename)
                # Define a relative path within the static directory
                relative_path = os.path.join('uploads', artist_name, filename)
                
                # Construct the absolute save path using Flask's app.static_folder
                save_path = os.path.join(app.static_folder, relative_path)
                
                # Ensure the directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # Save the image file
                image_file.save(save_path)

                # Define other variables
                title = request.form.get("title")
                description = request.form.get("description")
                genres = request.form.get("genres")
                original_size = request.form.get("original_size")
                print_size_a5 = request.form.get("print_size_a5") if 'print_size_a5' in request.form else None
                print_size_a4 = request.form.get("print_size_a4") if 'print_size_a4' in request.form else None
                print_size_a3 = request.form.get("print_size_a3") if 'print_size_a3' in request.form else None
                a5_price = request.form.get("a5_price", "14.99")
                a4_price = request.form.get("a4_price", "24.99")
                a3_price = request.form.get("a3_price", "39.99")

                # Request.form.get returns strings so convert to float
                try:
                    a5_price = float(a5_price)
                    a4_price = float(a4_price)
                    a3_price = float(a3_price)
                except ValueError:
                # Handle the error if the conversion fails
                    return "Invalid price format. Please enter a valid number."

                # Upload the art into the database
                db.execute("INSERT INTO Art (image_url, title, description, genres, original_size, print_size_a5, print_size_a4, print_size_a3, a5_price, a4_price, a3_price) VALUES (:image_url, :title, :description, :genres, :original_size, :print_size_a5, :print_size_a4, :print_size_a3, :a5_price, :a4_price, :a3_price)",
                        image_url=relative_path, title=title, description=description, genres=genres, original_size=original_size, print_size_a5=print_size_a5, print_size_a4=print_size_a4, print_size_a3=print_size_a3, a5_price=a5_price, a4_price=a4_price, a3_price=a3_price)
                
                # Now, retrieve the art_id based on the 'image_url'
                art_id_row = db.execute("SELECT art_id FROM Art WHERE image_url = :image_url",
                                        image_url=relative_path)
                if art_id_row:
                    art_id = art_id_row[0]['art_id']  # Assuming the query returns a list of dicts

                    # Now, insert the linkage into UserArt table
                    db.execute("INSERT INTO UserArt (user_id, art_id) VALUES (:user_id, :art_id)",
                            user_id=user_id, art_id=art_id)

                return redirect(url_for("profile"))
        else:
            return redirect("/login")
        
