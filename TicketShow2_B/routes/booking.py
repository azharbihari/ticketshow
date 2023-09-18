from flask_restful import Resource, marshal
from flask_security import auth_required, roles_required
from models import Show
from api.marshals import booking_marshal, show_marshal
from flask import abort


class BookingResource(Resource):
    @auth_required()
    @roles_required('admin')
    def get(self, show_id):
        try:
            show = Show.query.get_or_404(show_id)
            if not show:
                abort(404, message='Show not found')

            bookings = show.get_bookings_ordered_by_created_at()
            return {
                'show': marshal(show, show_marshal),
                'bookings': marshal(bookings, booking_marshal)
            }
        except Exception as e:
            abort(500, message='Internal Server Error', error=str(e))
