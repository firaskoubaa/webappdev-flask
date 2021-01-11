FROM alpine:latest

RUN apk add py3-pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt                                                                        

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["application.py"]


# similaire

# FROM alpine:latest
# RUN apk add python3-dev \
#     && pip3 install --upgrade pip
# COPY . /app
# RUN make /app
# CMD python /app/app.py
