# scratchhh.tk (wip)

## Table of contents
- [Installation](#installation)
  - [Config](#config)
- [Endpoints](#endpoints)
  - [GET /](#get-)
  - [GET /whyus](#get-whyus-)

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

## Endpoints
Pretty much every endpoint with docs

### GET /

*Response: HTML*
<br>
The root landing page. Shows a bit of information.

### GET /whyus/

*Response: HTML*
<br>
Talks about why you might want to use this.

### GET /projects/:ID:/

*Response: HTML*
<br>
Return project information, such as likes, views, or comments.

### GET /projects/:ID:/get/

*Response: send_file()*
<br>
Return Scratch project as sb3. Can be used with Scratch Desktop.

### GET /projects/:ID:/comments/get

*Response: Raw HTML*
<br>
Return top 3 comments for a Scratch project.

