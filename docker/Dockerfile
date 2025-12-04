FROM python:3.13-alpine

# Add bash shell
RUN apk add bash

# Add git
RUN apk add git

# Add make
RUN apk add make

# Add these packages so Zed editor can do its thing
RUN apk add curl procps

# Install uv
RUN pip install "uv~=0.9"

# Needed for Django
RUN apk add gettext

CMD ["python"]
