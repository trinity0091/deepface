#base image
FROM python:3.8
LABEL org.opencontainers.image.source https://github.com/trinity0091/deepface


# docker build  -f /workspace/codespace/category/facedetection/deepface/deepface-api.Dockerfile -t trinity0091/deepface-api . 



# -----------------------------------
# create required folder
RUN mkdir /app

# -----------------------------------
# Copy required files from repo into image
COPY . /app
# -----------------------------------
# switch to application directory
WORKDIR /app
# -----------------------------------
# update image os
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y





# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt



# -----------------------------------
# if you will use gpu, then you should install tensorflow-gpu package
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org tensorflow-gpu
# -----------------------------------
# install deepface from pypi release (might be out-of-the-date)
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org deepface
# -----------------------------------
# install deepface from source code (always up-to-date)
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -e .
# -----------------------------------
# some packages are optional in deepface. activate if your task depends on one.
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org cmake==3.24.1.1
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org dlib==19.20.0
# RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org lightgbm==2.3.1
# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1
# -----------------------------------
# run the app (re-configure port if necessary)
EXPOSE 5011
CMD ["python", "api/api.py", "-p", "5011"]
