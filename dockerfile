FROM ubuntu:20.04 AS base

ARG user=lionking group=docker gid=998

FROM base AS build

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends \
    tzdata gcc g++ vim wget python3-pip python3-dev unixodbc-dev \
    fontconfig default-libmysqlclient-dev libssl-dev -y && \
    apt-get autoremove -y && \
    apt-get autoclean

RUN TZ=Asia/Taipei && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    groupadd -g ${gid} ${group} && \
    useradd --create-home -ms /bin/bash ${user} && \
    adduser ${user} ${group} && \
    mkdir -p /home/${user}/workspace/data/videos && \
    chown -R ${user}:${group} /home/${user}/workspace

# USER ${user}

WORKDIR /home/${user}/

# COPY --chown=${user}:${group} ./lion_dashboard/requirements.txt ./requirements.txt

COPY --chown=${user}:${group} ./ ./workspace/

FROM build AS require

RUN pip install --no-cache-dir -r ./workspace/requirements.txt
RUN pip install ./workspace/liontk-2023.3.23.post1-py3-none-any.whl

FROM require AS final

USER ${user}

ENV FILE_KEY=/home/${user}/workspace/.env/.file.key
ENV CONTENT_KEY=/home/${user}/workspace/.env/.content.key

CMD ["python3", "./workspace/app.py"]

EXPOSE 55688
