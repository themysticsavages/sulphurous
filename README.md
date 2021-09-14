# scratchhh.tk (wip)

![root](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.web.png)

scratchhh.tk is basically [scratch.mit.edu](https://scratch.mit.edu) with more pros. This clone offers many features that are not available on Scratch.
It's obviously available [here](https://scratchhh.tk). Just please note that the site may be down for maintainance or something. That's why I offer local hosting!

# Installation
```bash
git clone https://github.com/themysticsavages/scratchhh.tk
cd scratchhh.tk
python -m pip install -r requirements.txt
```
## Config
```bash
nano application/config.py
```
```python
port = 2000
host = '0.0.0.0'
# Need SSL? Configure it in app.py
```
```bash
# Run as root if you are using "restricted ports"
python host.py
```
Bam! Scratchhh.tk is now running at http://IP:PORT

# Endpoints

## `/projects/<id>` endpoint
Make a GET request to return project information in nicely styled HTML.

![search](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.proj.png)

https://{domain}/projects/{id}

## `/projects/<id>/get` endpoint
Make a GET request to return a Scratch project download .sb3

## `/projects/<id>/comments/get` endpoint

![comm](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.comm.png)

Make a GET request to return top 3 Scratch comments as HTML.

## `/archive` endpoint
Fetch archived projects. More information can be found [here](https://scratchhh.tk/archive/docs)
