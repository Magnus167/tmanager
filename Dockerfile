FROM ubuntu:latest

# Install qbittorent
RUN apt-get update && apt-get install -y qbittorrent-nox