import pytz
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify
from datetime import datetime, timedelta
from pytz import timezone
from enum import Enum
from flask_security import UserMixin, RoleMixin
from sqlalchemy import func
db = SQLAlchemy()

# Define the association table for roles and users
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(120), default='default_avatar.png')
    date_of_birth = db.Column(db.Date, nullable=True)
    city = db.Column(db.String(120), nullable=True)
    active = db.Column(db.Boolean())
    fs_token_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    theaters = db.relationship(
        'Theater', backref='user', lazy=True, cascade="all, delete-orphan")
    bookings = db.relationship(
        'Booking', backref='user', lazy=True, cascade="all, delete-orphan")

    reviews = db.relationship('Review', backref='user',
                              lazy=True, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'))

    activities = db.relationship(
        'UserActivity', backref='user', lazy='dynamic')

    created_at = db.Column(
        db.DateTime(), default=datetime.now(timezone('Asia/Kolkata')))
    updated_at = db.Column(
        db.DateTime(),
        default=datetime.now(timezone('Asia/Kolkata')),
        onupdate=datetime.now(timezone('Asia/Kolkata')),
    )

    def get_all_theaters(self):
        theaters = Theater.query.filter_by(user=self).order_by(
            Theater.created_at.desc()).all()
        return theaters

    def get_all_bookings(self):
        bookings = Booking.query.filter_by(user=self).order_by(
            Booking.created_at.desc()).all()
        return bookings

    def get_user_last_visit(self):
        last_visit = UserActivity.query.filter_by(user=self).order_by(
            UserActivity.created_at.desc()).first()
        return last_visit

    def count_active_days_previous_month(self):
        today = datetime.now().date()
        first_day_of_this_month = today.replace(day=1)
        last_day_of_prev_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_prev_month = last_day_of_prev_month.replace(day=1)

        active_days = (
            UserActivity.query.filter(
                UserActivity.user == self,
                UserActivity.created_at >= first_day_of_prev_month,
                UserActivity.created_at < first_day_of_this_month
            )
            .with_entities(func.DATE(UserActivity.created_at))
            .distinct()
            .count()
        )

        return active_days

    def count_last_month_confirmed_bookings(self):
        today = datetime.now().date()
        first_day_of_this_month = today.replace(day=1)
        last_day_of_prev_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_prev_month = last_day_of_prev_month.replace(day=1)

        bookings_count = Booking.query.join(Show).filter(
            Booking.user == self,
            Booking.status == BookingStatus.CONFIRMED,
            Show.status == ShowStatus.FINISHED,
            Booking.created_at >= first_day_of_prev_month,
            Booking.created_at < first_day_of_this_month
        ).count()

        return bookings_count

    def get_amount_spent_previous_month(self):
        today = datetime.now().date()
        first_day_of_this_month = today.replace(day=1)
        last_day_of_prev_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_prev_month = last_day_of_prev_month.replace(day=1)

        amount_spent = Booking.query.join(Show).filter(
            Booking.user == self,
            Booking.status == BookingStatus.CONFIRMED,
            Show.status == ShowStatus.FINISHED,
            Booking.created_at >= first_day_of_prev_month,
            Booking.created_at < first_day_of_this_month
        ).with_entities(func.sum(Booking.amount)).scalar()

        return amount_spent or 0.0

    def get_last_month_confirmed_bookings(self):
        today = datetime.now().date()
        first_day_of_this_month = today.replace(day=1)
        last_day_of_prev_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_prev_month = last_day_of_prev_month.replace(day=1)

        confirmed_bookings = Booking.query.join(Show).filter(
            Booking.user == self,
            Booking.status == BookingStatus.CONFIRMED,
            Show.status == ShowStatus.FINISHED,
            Booking.created_at >= first_day_of_prev_month,
            Booking.created_at < first_day_of_this_month
        ).all()

        return confirmed_bookings

    def get_confirmed_finished_bookings(self):
        return Booking.query.join(Show).filter(
            Booking.status == BookingStatus.CONFIRMED,
            Show.status == ShowStatus.FINISHED,
            Booking.user == self
        ).all()

    def get_next_weekend_shows(self):
        today = datetime.now().date()
        next_weekend_start_date = today + \
            timedelta(days=(5 - today.weekday()) % 7)
        next_weekend_end_date = next_weekend_start_date + timedelta(days=2)

        next_weekend_shows = Show.query.join(Theater).filter(
            Theater.city == self.city,
            Show.showtime >= next_weekend_start_date,
            Show.showtime <= next_weekend_end_date,
            Show.status == ShowStatus.UPCOMING
        ).all()

        return next_weekend_shows


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=True)
    theater_id = db.Column(
        db.Integer, db.ForeignKey('theater.id'), nullable=True)
    visit_count = db.Column(db.Integer, default=1, nullable=False)
    path = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime(), default=datetime.now(timezone('Asia/Kolkata')))


class Theater(db.Model):
    __tablename__ = 'theater'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shows = db.relationship('Show', backref='theater',
                            lazy=True, cascade="all, delete-orphan")

    activities = db.relationship('UserActivity', backref='theater', lazy=True)

    created_at = db.Column(
        db.DateTime(), default=datetime.now(timezone('Asia/Kolkata')))
    updated_at = db.Column(
        db.DateTime(),
        default=datetime.now(timezone('Asia/Kolkata')),
        onupdate=datetime.now(timezone('Asia/Kolkata')),
    )

    def __init__(self, name, city, capacity, user):
        self.name = name
        self.city = city
        self.capacity = capacity
        self.user = user
        self.slug = slugify(self.name)

    def get_running_or_upcoming_shows(self):
        shows = Show.query.filter_by(theater=self).filter(
            Show.status.in_([ShowStatus.RUNNING, ShowStatus.UPCOMING])).order_by(Show.showtime.asc()).all()
        return shows

    def get_finished_shows(self):
        shows = Show.query.filter_by(theater=self).filter(
            Show.status == ShowStatus.FINISHED).order_by(Show.showtime.desc()).all()
        return shows

    def get_all_shows(self):
        shows = Show.query.filter_by(theater=self).order_by(
            Show.showtime.desc()).all()
        return shows


class ShowStatus(Enum):
    UPCOMING = "Upcoming"
    FINISHED = "Finished"
    RUNNING = "Running"


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    showtime = db.Column(db.DateTime(), nullable=False)
    end_showtime = db.Column(db.DateTime(), nullable=False)
    poster = db.Column(db.String(255), default='default_poster.png')
    status = db.Column(db.Enum(ShowStatus), nullable=False,
                       default=ShowStatus.UPCOMING)
    available_tickets = db.Column(db.Integer, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey(
        'theater.id'), nullable=False)
    bookings = db.relationship(
        'Booking', backref='show', lazy=True, cascade="all, delete-orphan")

    activities = db.relationship('UserActivity', backref='show', lazy=True)
    reviews = db.relationship('Review', backref='show',
                              lazy=True, cascade="all, delete-orphan")

    created_at = db.Column(
        db.DateTime(), default=datetime.now(timezone('Asia/Kolkata')))
    updated_at = db.Column(
        db.DateTime(),
        default=datetime.now(timezone('Asia/Kolkata')),
        onupdate=datetime.now(timezone('Asia/Kolkata')),
    )

    def __init__(self, name, genre, description, runtime, language, showtime, ticket_price, theater):
        self.name = name
        self.genre = genre
        self.description = description
        self.language = language
        self.showtime = showtime
        self.end_showtime = showtime + timedelta(minutes=runtime)
        self.available_tickets = theater.capacity
        self.ticket_price = ticket_price
        self.runtime = runtime
        self.theater = theater
        self.slug = slugify(self.name)

    @classmethod
    def get_running_or_upcoming_shows_in_city(cls, city):
        return cls.query.join(Theater).filter(Theater.city == city, cls.status != ShowStatus.FINISHED).order_by(Show.showtime.asc()).limit(5).all()

    @classmethod
    def get_latest_shows(cls):
        return cls.query.filter(cls.status != ShowStatus.FINISHED).order_by(cls.showtime.asc()).all()

    def get_bookings_ordered_by_created_at(self):
        return Booking.query.filter_by(show=self).order_by(Booking.created_at.desc()).all()

    def get_reviews_ordered_by_created_at(self):
        return Review.query.filter_by(show=self).order_by(Review.created_at.desc()).all()


class BookingStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(BookingStatus), nullable=False,
                       default=BookingStatus.CONFIRMED)
    review = db.relationship('Review', uselist=False, backref='booking')

    created_at = db.Column(
        db.DateTime(), default=datetime.now(timezone('Asia/Kolkata')))
    updated_at = db.Column(
        db.DateTime(),
        default=datetime.now(timezone('Asia/Kolkata')),
        onupdate=datetime.now(timezone('Asia/Kolkata')),
    )

    def __init__(self, user, show, number_of_tickets):
        self.user = user
        self.show = show
        self.number_of_tickets = number_of_tickets
        self.amount = show.ticket_price * number_of_tickets


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey(
        'booking.id'), nullable=False)

    show_id = db.Column(db.Integer, db.ForeignKey(
        'show.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255))
    created_at = db.Column(
        db.DateTime(), default=datetime.now(timezone('Asia/Kolkata')))
    updated_at = db.Column(
        db.DateTime(),
        default=datetime.now(timezone('Asia/Kolkata')),
        onupdate=datetime.now(timezone('Asia/Kolkata')),
    )

    def __init__(self, booking, rating, comment, user, show):
        self.booking = booking
        self.rating = rating
        self.comment = comment
        self.user = user
        self.show = show
