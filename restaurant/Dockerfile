# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /restaurant

COPY ../requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /restaurant/

ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

EXPOSE 5099
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /