from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite3'
app.config['SECRET_KEY'] = "fkveF8c8V13i9r2"

db = SQLAlchemy(app)

class authors(db.Model):
    id = db.Column('author_id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(100))
    status = db.Column(db.String(200))
    created = db.Column(db.String(100))
    updated = db.Column(db.String(100))

    def __repr__(self):
        return '<Author %r>' % self.lastName

class books(db.Model):
    id = db.Column('book_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    isbn = db.Column(db.Integer)
    year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
    authors = db.relationship('authors', backref=db.backref('books', lazy=True))
    status = db.Column(db.String(200))
    created = db.Column(db.String(100))
    updated = db.Column(db.String(100))
    view = db.Column(db.String(100))
    vote = db.Column(db.Integer)
    download = db.Column(db.Integer)

    def __repr__(self):
        return '<Book %r>' % self.title


@app.route('/list_authors')
def show_list_authors():
    return render_template('show_authors.html', list_authors=db.session.query(authors).all())

@app.route('/list_books')
def show_list_books():
    return render_template('show_books.html', list_books=db.session.query(books).all())

@app.route('/search_by_isbn/<isbn>')
def search_by_isbn(isbn):
    return render_template('show_books.html', list_books=db.session.query(books).filter(books.isbn == isbn).all())

@app.route('/search_by_title/<title>')
def search_by_title(title):
    return render_template('show_books.html', list_books=db.session.query(books).filter(books.title.contains(title)).all())

@app.route('/newauthor', methods=['GET', 'POST'])
def newauthor():
    if request.method == 'POST':
        if not request.form['firstName'] or not request.form['lastName'] or not request.form['email'] or not request.form['phone']:
            abort(400)
        else:
            if invalid_author(request.form['email'], request.form['phone']): abort(400)
            else:
                author = authors(firstName=request.form['firstName'], lastName=request.form['lastName'],
                                email=request.form['email'], phone=request.form['phone'],
                                address=request.form['address'], status=request.form['status'],
                                created=request.form['created'], updated=request.form['updated'])
                db.session.add(author)
                db.session.commit()
                flash('Record was successfully added')
                return redirect(url_for('show_list_authors'))

    return render_template('newauthor.html')

@app.route('/newbook', methods=['GET', 'POST'])
def newbook():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['isbn'] or not request.form['author_id']:
            abort(400)
        else:
            if invalid_book(request.form['isbn'], request.form['year']): abort(400)
            else:
                book = books(title=request.form['title'], isbn=request.form['isbn'], year=request.form['year'],
                            author_id=request.form['author_id'], status=request.form['status'],
                            created=request.form['created'], updated=request.form['updated'],
                            view=request.form['view'], vote=request.form['vote'], download=request.form['download'])
                db.session.add(book)
                db.session.commit()
                flash('Record was successfully added')
                return redirect(url_for('show_list_books'))

    return render_template('newbook.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if not request.form['SearchType'] or not request.form['SearchContent']:
            abort(400)
        else:
            if request.form['SearchType'] == 'isbn':
                return redirect(url_for('search_by_isbn',isbn=request.form['SearchContent']))
            elif request.form['SearchType'] == 'title':
                return redirect(url_for('search_by_title', title=request.form['SearchContent']))
            else:
                abort(400)
    return render_template('search.html')

@app.route('/')
def home():
    return render_template('home.html')

def invalid_author(email, phone):
    aa = 0
    bb = 0
    flag = True
    for c in email:
        if c == '@':
            aa = aa + 1
            flag = False
        if flag == False and c == '.': bb = bb + 1

    if aa != 1 or bb == 0: return True

    aa = 0
    for c in phone: aa = aa + 1
    if aa != 10 or phone[0] != 0: return True
    return False

def invalid_book(isbn, year):
    for c in isbn:
        if c < '0' or c > '9': return True

    c = int(year, 10)
    if c > 2019: return True
    return False

if __name__ == '__main__':
    db.create_all()
    app.run()