from datetime import datetime, timedelta
from models import Show, ShowStatus, db
from celery import shared_task
from models import db, Theater, BookingStatus, UserActivity, User
import pandas as pd
from flask import current_app, render_template
from flask_mail import Message, Mail
from humanize import naturaltime
import calendar
from pytz import timezone
from pathlib import Path
mail = Mail()


@shared_task(ignore_result=False)
def update_show_status():
    shows = Show.query.filter(Show.status != ShowStatus.FINISHED).all()
    current_datetime = datetime.now()

    for show in shows:
        if current_datetime >= show.showtime and current_datetime <= show.end_showtime:
            show.status = ShowStatus.RUNNING
        elif current_datetime > show.end_showtime:
            show.status = ShowStatus.FINISHED
        else:
            show.status = ShowStatus.UPCOMING
    db.session.commit()
    return 'Shows status changed'


@shared_task(ignore_result=False)
def update_dynamic_price():
    shows = Show.query.filter(Show.status == ShowStatus.UPCOMING).all()
    for show in shows:
        remaining_hours = (show.showtime - datetime.now()
                           ).total_seconds() / 3600
        percentage_sold = (show.theater.capacity -
                           show.available_tickets) / show.theater.capacity

        if remaining_hours < 24 and percentage_sold > 0.9:
            show.ticket_price *= 1.1
        elif remaining_hours < 24 and percentage_sold <= 0.5:
            show.ticket_price *= 0.9
        else:
            show.ticket_price *= 1

    db.session.commit()
    return 'Shows price changed'


@shared_task(ignore_result=False)
def export_theater_data_to_csv(theater_id):
    theater = db.get_or_404(Theater, theater_id)
    if not theater:
        return {'error': 'Theater not found'}

    shows = theater.get_finished_shows()

    try:
        data = [{
            'Show Name': show.name,
            'Genre': show.genre,
            'Language': show.language,
            'Showtime': show.showtime.strftime('%Y-%m-%d %H:%M:%S'),
            'Status': show.status.value,
            'Tickets Sold': show.theater.capacity - show.available_tickets,
            'Number of Bookings': len([booking for booking in show.bookings if booking.status == BookingStatus.CONFIRMED]),
            'Revenue': sum([booking.amount for booking in show.bookings if booking.status == BookingStatus.CONFIRMED])
        } for show in shows]

        df = pd.DataFrame(data)
        file_name = f"{theater.name.replace(' ', '_')}_{theater_id}.csv"
        file_path = f"media/exports/{file_name}"
        df.to_csv(file_path, index=False)

        return file_path

    except Exception as e:
        return {'error': str(e)}


@shared_task(ignore_result=False)
def add_user_activity(user_id, show_id, theater_id, path):
    try:
        user = db.get_or_404(User, user_id) if user_id else None
        show = db.get_or_404(Show, show_id) if show_id else None
        theater = db.get_or_404(Theater, theater_id) if theater_id else None

        existing_activity = user.activities.filter(
            UserActivity.path == path).first()

        if existing_activity:
            existing_activity.created_at = datetime.now()
            existing_activity.visit_count += 1
        else:
            user_activity = UserActivity(
                user=user, show=show, theater=theater, path=path)
            db.session.add(user_activity)
        db.session.commit()
        return 'User activity added successfully'
    except Exception as e:
        return {'error': str(e)}


@shared_task(ignore_result=False)
def send_inactive_user_email():
    try:
        cutoff_time = datetime.now().date() - timedelta(days=30)
        inactive_users = User.query.filter(~User.activities.any(
            UserActivity.created_at > cutoff_time)).all()

        for user in inactive_users:
            last_visit = user.get_user_last_visit()
            last_visited_at = last_visit.created_at if last_visit else None
            msg = Message(
                'Inactive User Notification',
                recipients=[user.email],
                html=render_template(
                    'emails/inactive_user_email.html', user=user, last_visited_at=last_visited_at)
            )
            mail.send(msg)

        return 'Email sent successfully'
    except Exception as e:
        return {'error': str(e)}


@shared_task(ignore_result=False)
def send_monthly_entertainment_report():
    try:
        now = datetime.now()
        previous_month = (now.month - 2) % 12 + 1
        previous_year = now.year if now.month > 1 else now.year - 1
        users = User.query.all()
        for user in users:
            report_data = {
                'user': user,
                'month_name': calendar.month_name[previous_month],
                'year': previous_year,
                'days_active': user.count_active_days_previous_month(),
                'shows_booked': user.count_last_month_confirmed_bookings(),
                'amount_spent': user.get_amount_spent_previous_month(),
                'bookings': user.get_last_month_confirmed_bookings(),
                'next_weekend_shows': user.get_next_weekend_shows()
            }
            msg = Message(
                subject=f"Monthly Entertainment Report - {calendar.month_name[previous_month]} {previous_year}",
                recipients=[user.email],
                html=render_template(
                    'emails/monthly_entertainment_report.html', **report_data)
            )

            mail.send(msg)
        return 'Monthly entertainment report sended successfully'
    except Exception as e:
        return {'error': str(e)}
