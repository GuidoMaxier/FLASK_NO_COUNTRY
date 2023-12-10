from app import ma
from app.models.modelUser import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'location', 'is_active')