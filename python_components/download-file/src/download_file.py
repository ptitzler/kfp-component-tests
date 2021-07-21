import kfp


def download(url, file_content: kfp.components.OutputPath(str)):

    import requests

    response = requests.get(url=url)
    if response.status_code == 200:
        with open(file_content, 'wb') as file_content:
            file_content.write(response.content)
    else:
        raise RuntimeError(f'Download of {url} returned HTTP status code {response.status_code}')
