from application import app
import datetime
import os

os.chdir('application')
print('Server started!')
print(os.listdir())
app.run()
