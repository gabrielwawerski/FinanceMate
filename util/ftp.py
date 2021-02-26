import ftplib
import util.settings as settings


ftp = ftplib.FTP(settings.ftp_hostname, settings.ftp_username, settings.ftp_password)


def ftp_retr(path: str, filename: str, file):
    return ftp.retrbinary(f"RETR {path}/{filename}", file.write)


def ftp_stor(path: str, filename):
    ftp.storbinary(f"STOR /{path}", filename)


def from_server() -> dict:
    import requests
    import jsonpickle
    data = requests.get(f"{settings.full_data_url}{settings.default_settings}").text
    return dict(jsonpickle.decode(data))
