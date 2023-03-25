# MyNance
### Video Demo: [link](https://youtu.be/PBpXTabZ6P8)
### Features:
I included the Werkzeug Library, to add hashing and password checking features.
```python
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
```
Also, I used the [Flask Web Framework](https://flask.palletsprojects.com/en/1.1.x/) based in Python to build my website's back-end; while using HTML, CSS and basic Javascript for the front-end side.

### Description:
This is a website that allows the user to register an account or login to a previously registered account to keep a record of their finances. The user can also change their profile picture into something more personal, instead of the basic image; also, they may check their transactions on a specific date using the calendar tab. Another feature of note is the ability to delete all the transactions, to start with a clean slate.

### Sqlite3:
I made _four_ different tables:
* **Users** table, with columns: ID (Primary Key), Username, Hash, Money.
* **Expenses** and **Income**, with columns: User Id (references Primary Key ID), Expense/Income, Category, Description.
* **History**, User Id, Amount, Category, Type, Desc, Date.

### Changing Profile Pictures Code Snippet:
```python
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect("/user")
        file = request.files['file']
        if file.filename == '':
            return redirect("/user")

        # and allowed_file(file.filename)
        if file:
            files = os.listdir("./static/profilePictures")
            username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']
            for f in files:
                if username in str(f):
                    os.remove(f'./static/profilePictures/{f}')
                    break

            file.filename = f"{username}.{file.filename.split('.')[1].lower()}"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/user")


```

### Login Code Snippet:
```python
    if request.method == "POST":
        #ensure proper input
        #ensure user filled username

        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if rows == None:
            return render_template("fail_log.html")

        #ensure user filled password
        password = request.form.get("password")
        if not password:
            return render_template("fail_log.html")

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("fail_log.html")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

```
##
### CS50
CS50 (Computer Science 50) is an on-campus and online introductory course on computer science taught at Harvard University and Yale University. In 2016, CS50 became available to high school students as an Advanced Placement Computer Science course. The on-campus version is Harvard's largest class with 800 students, 102 staff and up to 2,200 participants in their regular hackathons.

The course material is available online for free on the EdX platform, with a range of certificates available for a fee. As of 2022, this online version, called CS50x, teaches the languages C, Python, SQL, HTML, CSS, and JavaScript. It also teaches fundamental computer-science concepts including arrays and data structures, and the Flask web framework. The 2021 iteration of the course introduced three new additional lectures on computer security, artificial Intelligence, and the ethics of technology.

Check out [CS50](https://cs50.harvard.edu/x/2022/)!