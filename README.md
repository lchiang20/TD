RUN With (Ubuntu linux)
open terminal: go to location 
example: administrator@C020-Dell3670:~/Works/TD$ python manage.py runserver 80
>>
October 04, 2019 - 03:58:27 Django version 1.11.24, 
using settings 'TutoringDragons.settings' 
Starting development server at http://127.0.0.1:8000/ 
Quit the server with CONTROL-C.
copy link http://127.0.0.1:8000/ and run in website


website: http://honnguyen.ssis.edu.vn


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^adminview/$', adminview, name='adminview'),
    url(r'^studentview/$', studentview, name='studentview'),
]

http://honnguyen.ssis.edu.vn for index
http://honnguyen.ssis.edu.vn/adminview for adminview
http://honnguyen.ssis.edu.vn/studentview for studentview
