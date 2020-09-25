import requests 
from pathlib import Path
import json
from tqdm import tqdm

journals = {
    'Эрмитаж':'https://figgy.princeton.edu/concern/scanned_resources/6b561fbb-ba28-4afb-91d2-d77b8728d7d9/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/6b561fbb-ba28-4afb-91d2-d77b8728d7d9/manifest',
    'Вестник искусств':'https://figgy.princeton.edu/concern/scanned_resources/ad256b35-9ad0-4f75-bf83-3bad1a7c6018/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/ad256b35-9ad0-4f75-bf83-3bad1a7c6018/manifest',
    'Советский театр':'https://figgy.princeton.edu/concern/scanned_resources/f33993bb-a041-40a1-b11f-f660da825583/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/f33993bb-a041-40a1-b11f-f660da825583/manifest',
    'Рабис':'https://figgy.princeton.edu/concern/scanned_resources/01f4236f-0a2f-473c-946f-d9bbec12f8ea/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/01f4236f-0a2f-473c-946f-d9bbec12f8ea/manifest',
    "Даёшь":'https://figgy.princeton.edu/concern/scanned_resources/e036a5da-97a8-4041-ad62-a57af44359e2/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/e036a5da-97a8-4041-ad62-a57af44359e2/manifest',
    'Персимфанс':'https://figgy.princeton.edu/concern/scanned_resources/af43d19a-3659-4dd0-a0fc-4c74ce521ad6/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/af43d19a-3659-4dd0-a0fc-4c74ce521ad6/manifest',
    'Тридцать дней':'https://figgy.princeton.edu/concern/scanned_resources/d2d488af-2980-4554-a9ef-aacbaf463ec8/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/d2d488af-2980-4554-a9ef-aacbaf463ec8/manifest',
    'За пролетарское искусство':'https://figgy.princeton.edu/concern/scanned_resources/38f89d57-8e64-4033-97d6-b925c407584a/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/38f89d57-8e64-4033-97d6-b925c407584a/manifest',
    'Бригада художников':'https://figgy.princeton.edu/concern/scanned_resources/66d00a87-5ea9-439a-a909-95d697401a2b/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/66d00a87-5ea9-439a-a909-95d697401a2b/manifest',
    'Зрелища':'https://figgy.princeton.edu/concern/scanned_resources/1af8b322-a0b1-46af-8541-5c3054af8098/manifest?manifest=https://figgy.princeton.edu/concern/scanned_resources/1af8b322-a0b1-46af-8541-5c3054af8098/manifest',

}
def download_images(journal:str, manifest_url:str, output_dir:str):
    path = Path(output_dir)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    data = requests.get(manifest_url)
    data = json.loads(data.content)
    for manifest in data['manifests']:
        id_ = manifest["@id"]
        label = manifest["label"][0]
        new_manifest = requests.get(id_)
        new_data = json.loads(new_manifest.content)
        for i in range(len(new_data['metadata'])):
            try:
                count = len(new_data["sequences"][0]["canvases"])
                for i in range(count):
                    URI = new_data["sequences"][0]["canvases"][i]["images"][0][
                        "resource"
                    ]["@id"]
                    image = requests.get(URI)
                    name = journal + '_' +label + '_' + str(i) + '.jpg'
                    (path / name).write_bytes(image.content)
            except Exception as e:
                print(e)                

                
if __name__ == "__main__":
    for journal, url in tqdm(journals.items()):
        download_images(journal,url,'images')
      
