FROM jenkins/jenkins:2.479.3-lts-jdk17

USER root

RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install -y python3.11-venv
RUN python3 -m venv .venv && source .venv/bin/activate
RUN python3 -m pip install -r /var/jenkins_scripts/requirements.txt

RUN mkdir -p /var/jenkins_scripts
RUN chown -R jenkins:jenkins /var/jenkins_scripts

USER jenkins