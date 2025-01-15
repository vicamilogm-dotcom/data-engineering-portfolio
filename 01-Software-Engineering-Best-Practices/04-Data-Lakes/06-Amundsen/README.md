# Amundsen

This is an example which shows an open source alternative as meta data catalog created by lyft along with an early preview of docker compose for creating complicated setups!

Clone the required repo

```bash
git clone --recursive https://github.com/amundsen-io/amundsen.git
```

```bash
cd amundsen
```

Start Amundsen in a docker compose stack:

```bash
docker compose -f docker-amundsen.yml up
```

Load some data:

```bash
cd databuilder
```

```python
python example/scripts/sample_data_loader.py
```

Then check out http://localhost:5000/  and have a look at the metadata catalog!

It's also worth checking out the script `example/scripts/sample_data_loader.py` which shows how to load data into the system and although the gcp loading with metadata had some tricky parts, it is no where nearly as tricky as Amundsen. It is only recommended when you want to work with an extensive multi cloud setup (i.e. beyond one data base on another cloud provider)!
