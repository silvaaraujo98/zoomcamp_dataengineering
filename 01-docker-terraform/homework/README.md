Question 1. Understanding Docker images
Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?

<font color="green">25.3</font>
24.3.1
24.2.1
23.3.1

Ans:
$ docker run -it --rm --entrypoint bash python:3.13-slim
pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)