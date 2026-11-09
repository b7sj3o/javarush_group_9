"""Шукає файл у кожному шарі образу: python dig_layers.py secret.tar .env"""
import json
import sys
import tarfile

image_path, name = sys.argv[1], sys.argv[2]

with tarfile.open(image_path) as image:
    layers = json.load(image.extractfile("manifest.json"))[0]["Layers"]
    print(f"Шарів в образі: {len(layers)}")
    for number, layer in enumerate(layers, 1):
        with tarfile.open(fileobj=image.extractfile(layer), mode="r:*") as files:
            for member in files:
                if not member.name.endswith(name):
                    continue
                if ".wh." in member.name:
                    print(f"Шар {number}: {member.name}  <- лише мітка «файл видалено»")
                else:
                    text = files.extractfile(member).read().decode().strip()
                    print(f"Шар {number}: {member.name}  <- вміст: {text}")
