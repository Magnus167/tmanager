import requests


class QBittorrentClient:
    def __init__(self, url="http://localhost:8080/"):
        self.url = url
        self.session = requests.Session()

    def login(self, username, password):
        response = self.session.post(
            f"{self.url}api/v2/auth/login",
            data={"username": username, "password": password},
        )
        if response.text != "Ok.":
            raise Exception("Failed to login")

    def add_torrent(self, torrent_url):
        files = (
            {"torrents": (torrent_url, open(torrent_url, "rb"))}
            if torrent_url.startswith("/")
            else None
        )
        data = {"urls": torrent_url} if not files else None
        response = self.session.post(
            f"{self.url}api/v2/torrents/add", files=files, data=data
        )
        return response.ok

    def get_torrents(self):
        response = self.session.get(f"{self.url}api/v2/torrents/info")
        return response.json()


# Example usage
client = QBittorrentClient()
client.login("username", "password")  # Replace with your qBittorrent credentials
client.add_torrent(
    "magnet:?xt=urn:btih:..."
)  # Replace with your magnet link or torrent file path

# Fetch and print torrent info
torrents = client.get_torrents()
for torrent in torrents:
    print(torrent["name"], torrent["state"], torrent["progress"])
