FROM    python:3.7
LABEL   maintainer="Bhanuka Mahanama <@mahanama94>"

WORKDIR /app
COPY    requirements.txt ./
RUN     pip install -r requirements.txt
COPY    demo-server ./

CMD     ["flask", "run", "--host=0.0.0.0"]
