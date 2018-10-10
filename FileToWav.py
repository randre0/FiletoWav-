import requests, json, time, os, sys, random, string


def get_server(api):
    url = "https://api2.online-convert.com/jobs"
    payload = "{\"conversion\":[{\"category\":\"audio\",\"target\":\"wav\"}]}"
    headers = {
        'x-oc-api-key': api,
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    data = json.loads(response.text)
    url = data['server'] + '/upload-file/' + data['id']
    return url


def upload_file(server_url, api):
    headers = {
        'x-oc-api-key': api,
        'cache-control': "no-cache",
    }
    name = sys.argv[1].split("\\")
    filename = name[len(name) - 1]
    path = "\\".join(name[0:len(name) - 1])
    filepath = (os.path.join(path))
    for x in range(len(sys.argv[0].split("\\")) - 1):
        os.chdir('..')
    os.chdir(filepath)
    music_mp3 = open(filename, "rb")
    send_files = {'file': (''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.wav',
                           music_mp3, 'audio/mp3')}
    r = requests.request("POST", server_url, files=send_files, headers=headers)
    job_id = (json.loads(r.text))["id"]["job"]
    return job_id, filename


def download_file(api, job_id, filename):
    headers = {
        'x-oc-api-key': api,
        'cache-control': "no-cache"
    }

    url = "https://api2.online-convert.com/jobs"
    r = requests.get(url + "/" + job_id, headers=headers)
    r = json.loads(r.text)
    uri = r['output'][0]['uri']
    status = r['status']['code']

    while status != 'completed':
        time.sleep(5)
        r = requests.get(url + "/" + job_id, headers=headers)
        r = json.loads(r.text)
        status = r['status']['code']
    headers = {
        'cache-control': "no-cache"
    }

    song = requests.get(uri, headers=headers)

    result = filename.replace(".mp3", ".wav")
    with open(result, 'wb') as f:
        f.write(song.content)


if __name__ == '__main__':
    api = "XXXXXXX"
    server_url = get_server(api)
    job_id, filename = upload_file(server_url, api)
    download_file(api, job_id, filename)
