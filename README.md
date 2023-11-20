NOTE: Under construction.

# tmanager

## Description

A simple torrent client with a bunch of scripts that runs on my raspberry pi.
Ultimately, the idea would be to be able to use a Python API to transfer files
across a local network.

## Usage

### Running the docker image

It's a simply copy-pasta from Github:[`qbittorrent/docker-qbittorrent-nox`](https://github.com/qbittorrent/docker-qbittorrent-nox/).
It's available on docker hub as DockerHub:[`qbittorrentofficial/qbittorrent-nox`.](https://hub.docker.com/r/qbittorrentofficial/qbittorrent-nox)

I edit the environment variables in the `docker-compose.yml` file to my liking.

Then you simply run:
```bash
docker-compose up -d
```
The default port for the WebUI is `9090` in this instance.
The default username is `admin` and the default password is `adminadmin`.

#### Volumes
I'm using these volumes in my `docker-compose.yml` file:
```yaml
volumes:
    - ./qbt-run/config:/config
    - ./qbt-run/downloads:/downloads
```

One of the key advantages of this setup is the the downloads folder can be anywhere. I have a NAS disk that I have mounted as a network drive on my raspberry pi. When doing large downloads, I can simply mount the NAS disk to the `downloads` folder and then run the docker container.

### Python API for scheduling and orchestrating downloads

This is a work in progress.

#### FileSys

I use a simple class called `FileSys` to manage the files and folders on my NAS disk. It's a simple wrapper around the `os` and `pathlib` modules. It simply makes it easier to navigate the file system using dictionaries and being bale to orchestrate file system operations.

#### TorrentClient

I use a simple class called `TorrentClient` to manage the torrent client.
Will most likely use [qbittorrent-api](https://github.com/rmartin16/qbittorrent-api/) to manage the torrent client.
