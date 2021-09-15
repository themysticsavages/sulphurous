# Table of contents
- [Installation](#installation)
  - [Config](#config)
- [Endpoints](#endpoints)
  - [GET /](#get-)
  - [GET /whyus](#get-whyus)
  - GET /projects/
    - [GET /projects/:ID:/](#get-projectsid)
      - [GET /projects/:ID:/get](#get-projectsidget) 
      - [GET /projects/:ID:/embed](#get-projectsidembed)
      - [GET /projects/:ID:/embed-light](#get-projectsidembed-light)
    - GET /projects/:ID:/comments
      - [GET /projects/:ID:/comments/get](#get-projectsidcommentsget)
  - [GET /archive/](#get-archive)
    - [GET /archive/docs](#get-archivedocs)
    - [GET /archive/:ID:](#get-archiveid)
      - [GET /archive/:ID:/:PRO:](#get-archiveidpro)  

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

### GET /projects/:ID:/embed

*Response: HTML*
<br>
Return a smaller version of a project page which contains almost all the same information.

### GET /projects/:ID:/embed-light

*Response: HTML*
<br>
Basically an embed but adapted for light mode websites.

### GET /archive/

*Response: JSON*
<br>
Return all current archived project directories as JSON. It's JSON because it's more of an API thing.

### GET /archive/docs/

*Response: HTML*
<br>
Get detailed information about using the archive endpoint.

### GET /archive/:ID:/

*Response: JSON*
<br>
Return all current archived projects for a directory as JSON.

### GET /archive/:ID:/:PRO:

*Response: send_file()*
<br>
Get an archived project in a directory as sb3.
