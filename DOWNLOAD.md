Dataset **CBIS-DDSM** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/v/F/oX/CardEma5UytUxK9cmygaMxpwmvFhJY4XJCs88mmZT6McM3udg63RwDfAFjreYzR7UaBj2AtuoH6yo1ES8vuvanUvlYzFbmJXFt4iiMICpxqCWqX0ds2kYPXbK2RU.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='CBIS-DDSM', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

