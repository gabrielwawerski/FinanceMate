import urllib.request
import jsonpickle
from util.settings import server_url, data_dir, default_settings
# handles reading json data from server


def server_default_settings():
    with urllib.request.urlopen(f"{server_url}{data_dir}{default_settings}") as url:
        server_data = url.read()
        return jsonpickle.decode(server_data)
