FROM python:3.8

# set the working directory in the container
WORKDIR /app

# copy the application code into the container
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose the port that the application runs on
EXPOSE 5000

# run the application
CMD ["python", "app.py"]
>>>>>>> Test-all-the-modules-in-the-application-using-the-pytest
