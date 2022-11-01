# Place *.mp3* sound samples in this folder...

## 1) Download *.zip* file with samples

- https://philharmonia.co.uk/resources/sound-samples (original source)
- https://archive.org/details/philharmonicorchestrasamples (alternative source)

e.g. `wget <url>/all-samples.zip`

## 2) Extract *.mp3* samples

e.g. `unzip all-samples.zip && cd all-samples && unzip '*.zip'`

## 3) Update database file *data.json.zip*

e.g. `python3 data.py -u`
