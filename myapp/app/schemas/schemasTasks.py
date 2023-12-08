from app import ma
from app.models.modelTasks import Task

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        # fields = ('id', 'title', 'description')

# task_schema = TaskSchema()
# tasks_schema = TaskSchema(many=True)

