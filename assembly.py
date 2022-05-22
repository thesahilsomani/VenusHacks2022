import requests
from time import sleep

class Assembly:
    def __init__(self, file_name = 'assemblyAPIKEY.txt'):
        try:
            with open(file_name)  as f:
                self.api_key = f.readlines()[0].rstrip()
        except:
            print("Error with Opening API_KEY File")

    def convert_url(self, url, fields=['text']):
        id = self._enqueue_url(url)
        out = self._fetch_id(id, fields)
        if len(out) == 1:
            return out[fields[0]]
        else:
            print('len out not 1')
            return out

    def convert_file(self, filename, fields=['text']):
        url = self._get_url(filename)
        id = self._enqueue_url(url)
        out = self._fetch_id(id, fields)
        if len(out) == 1:
            return out[fields[0]]
        else:
            print('len out not 1')
            return out

    def _enqueue_url(self, url):
        json = { "audio_url": url}
        headers = { "authorization": self.api_key,
                    "content-type": "application/json" }
        response = requests.post("https://api.assemblyai.com/v2/transcript", json=json, headers=headers)
        return response.json()['id']

    def _fetch_id(self, id, fields):
        endpoint = f"https://api.assemblyai.com/v2/transcript/{id}"
        headers = { "authorization": self.api_key }
        response = requests.get(endpoint, headers=headers).json()
        status = response['status']
        while(status == 'queued' or status == 'processing'):
            sleep(1)
            response = requests.get(endpoint, headers=headers).json()
            status = response['status']
        out = dict()
        for field in fields:
            out[field] = response[field]
        return out

    def _get_url(self, filename, chunk_size=5242880):
        headers = {'authorization': self.api_key}
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                 headers=headers,
                                 data=self._read_file(filename, chunk_size))
        return response.json()['upload_url']

    def _read_file(self, filename, chunk_size):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

