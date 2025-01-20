FROM jenkins/jenkins:2.479.3-lts-jdk17

USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

WORKDIR /var/jenkins_scripts

COPY ./scripts/requirements.txt /var/jenkins_scripts/

RUN python3 -m venv .venv
RUN bash -c "source .venv/bin/activate"
RUN bash -c "python3 -m pip install --break-system-packages -r /var/jenkins_scripts/requirements.txt"

USER jenkins