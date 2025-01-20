FROM jenkins/jenkins:2.479.3-lts-jdk17

USER root

RUN apt-get update && apt-get install -y python3 python3-pip

RUN mkdir -p /var/jenkins_scripts
RUN chown -R jenkins:jenkins /var/jenkins_scripts

USER jenkins