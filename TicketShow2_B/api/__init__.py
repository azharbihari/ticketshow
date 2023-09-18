from flask_restful import marshal, fields


from routes.user import (ProfileResource,
                         MyReviewResource, MyBookingResource, AvatarResource)

from routes.theater import (
    TheaterResource, ExportResource, ExportStatusResource, InsightResource)


from routes.show import (ShowResource, PosterResource)


from routes.home import (HomeResource, UserCityShowResource,
                         SearchResource, SingleShowResource, TheaterShowResource)


from routes.auth import (
    RegisterResource, LoginResource, UserResource, LogoutResource
)
from routes.booking import (BookingResource)
from routes.review import (ReviewResource)
from flask_restful import Api


api = Api(prefix='/api')

api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(UserResource, '/user')
api.add_resource(LogoutResource, '/logout')


api.add_resource(ProfileResource, '/profile', endpoint='profile')
api.add_resource(AvatarResource, '/avatar')
api.add_resource(MyBookingResource, '/mybookings',
                 '/<int:show_id>/mybookings', '/mybookings/<int:booking_id>', endpoint='mybookings')
api.add_resource(
    MyReviewResource, '/myreviews', '/<int:booking_id>/myreviews', endpoint='myreviews')

api.add_resource(HomeResource, '/', endpoint='home')
api.add_resource(SingleShowResource, '/<int:show_id>', endpoint='show')
api.add_resource(UserCityShowResource, '/city/shows', endpoint='city_shows')
api.add_resource(SearchResource, '/search', endpoint='search')
api.add_resource(TheaterShowResource,
                 '/theaters/<int:theater_id>/shows', endpoint='theater_shows')


# Admin Routes
api.add_resource(BookingResource, '/<int:show_id>/bookings')
api.add_resource(ReviewResource, '/<int:show_id>/reviews')
api.add_resource(TheaterResource, '/theaters', '/theaters/<int:theater_id>')
api.add_resource(ExportResource, '/exports/<int:theater_id>')
api.add_resource(ExportStatusResource, '/exports/<string:task_id>/status')
api.add_resource(ShowResource, '/<int:theater_id>/shows',
                 '/shows/<int:show_id>')
api.add_resource(PosterResource, '/posters/<int:show_id>')
api.add_resource(InsightResource, '/insights')
