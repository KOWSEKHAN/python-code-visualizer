from models.frame import FrameModel
from models.object_model import ObjectModel


frame = FrameModel("Global Frame")

frame.add_variable("student", "Student Object #1")
frame.add_variable("x", 10)

print(frame)


student = ObjectModel("object_1", "Student")

student.set_attribute("name", "Kowshik")
student.set_attribute("age", 23)

print(student)