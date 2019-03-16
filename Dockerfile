FROM python:3.6.1

# create and set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
# ??? this will help leverage Docker cache
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add the app to the working directory
ADD . /usr/src/app

# run the server
CMD python manage.py runserver -h 0.0.0.0