# Table of contents
- [Installation](#installation)
  - [Config](#config)
- [Endpoints](#endpoints)
  - [GET /](#get-)
  - [GET /whyus](#get-whyus)
  - [GET /login](#get-login)
  - [GET /backpack/](#get-backpack)
    - [GET /backpack/get](#get-backpackget) 
  - GET /projects/
    - [GET /projects/:ID:/](#get-projectsid)
      - [GET /projects/:ID:/get](#get-projectsidget) 
      - [GET /projects/:ID:/embed](#get-projectsidembed)
      - [GET /projects/:ID:/embed-light](#get-projectsidembed-light)
    - GET /projects/:ID:/comments
      - [GET /projects/:ID:/comments/get](#get-projectsidcommentsget)
  - [GET /archive/](#get-archive)
    - [GET /archive/docs](#get-archivedocs)
    - [GET /archive/search](#get-archivesearch)
  - [GET /api/](#get-api)
      - [GET /api/archive/](#get-apiarchive) 
        - [GET /api/archive/:ID:](#get-apiarchiveid)  
          - [GET /api/archive/:ID:/:PRO:](#get-apiarchiveidpro) 
      - [GET /api/postcomment/](#get-apipostcomment)
      - [GET /api/checkuser/](#get-checkuser) 
- [Private endpoints](#private-endpoints)

# scratchhh.xyz (wip)

![badge](https://img.shields.io/codacy/grade/a69a147a35534c83bc02a32687fa80da)

![root](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.web.png)

scratchhh.xyz is basically [scratch.mit.edu](https://scratch.mit.edu) with more pros. This clone offers many features that are not available on Scratch. It's still a work in progress so some endpoints are not there YET.
It's obviously available [here](https://scratchhh.xyz). Just please note that the site may be down for maintainance or something. That's why I offer local hosting!

# Installation
```bash
$ git clone https://github.com/themysticsavages/scratchhh.tk
$ cd scratchhh.tk
$ python -m pip install -r requirements.txt
```
## Config
```bash
$ nano application/config.py
```
```python
port = 2000
host = '0.0.0.0'
# Need SSL? Configure it in app.py
```
```bash
# Run as root if you are using "restricted ports"
$ python host.py
```
**Bam!** Scratchhh.tk is now running at http://localhost:2000 (by default)

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

### GET /login/

*Response: HTML*
<br>
Login with a valid Scratch account! Once logged in, your login info is stored as cookies and is used when required.

### GET /backpack/

*Response: HTML*
<br>
Return all assets like images and music (not sprites though).

### GET /backpack/get/

*Response: send_file()*
<br>
Get all your assets in a convenient ZIP file.

### GET /projects/:ID:/

*Response: HTML*
<br>
Return project information, such as likes, views, or comments.

### GET /projects/:ID:/get/

*Response: send_file()*
<br>
Return Scratch project as sb3. Can be used with Scratch Desktop.

### GET /projects/:ID:/comments/get/

*Response: Raw HTML*
<br>
Return top 3 comments for a Scratch project.

### GET /projects/:ID:/embed/

*Response: HTML*
<br>
Return a smaller version of a project page which contains almost all the same information.

### GET /projects/:ID:/embed-light/

*Response: HTML*
<br>
Basically an embed but adapted for light mode websites.

### GET /archive/

*Response: HTML*
<br>
Return a friendly search page to search for archived projects.

### GET /archive/docs/

*Response: HTML*
<br>
Get detailed information about using the archive endpoint.

### GET /archive/search/

*Response: HTML*
<br>
Search for archived projects under a directory.

Parameters:
 - `q`

### GET /api/

*Response: JSON*
<br>
Gets a jokish response. It's more of a place holder rather than something useful.

### GET /api/archive/
<br>
Get current project directories contain projects and their versions.

### GET /api/archive/:ID:/

*Response: JSON*
<br>
Return all current archived projects for a directory as JSON.

### GET /api/archive/:ID:/:PRO:/

*Response: send_file()*
<br>
Get an archived project in a directory as sb3.

### GET /api/postcomment/

*Response: redirect()*
<br>
Post a comment on a particular project.
Yeah I know, it's a GET request.

Parameters:
 - `pid`
 - `user` (send as base64)
 - `pass` (send as base64)
 - `content`

### GET /api/checkuser/

*Response: JSON*
<br>
See if a user exists but much easier.

## Private endpoints
Endpoints that are not in this repo but are available in [scratchhh.xyz](https://scratchhh.xyz). Don't worry, they don't do much.

**GET /selfdestruct/:** Basically play some FNAF 2 music.
<br>
**GET /buglist/:** Talk about any bugs on the main site.
