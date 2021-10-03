<h1 align='center'>scratchhh.xyz - a clone of Scratch that isn't dead</h1>

![badge](https://img.shields.io/codacy/grade/a69a147a35534c83bc02a32687fa80da)

![root](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.web.png)

# Highlights
  - A consistent and built-in dark mode
  - Gist creation; create small snippets of Scratch code for the world to see (i guess)
  - Easy-to-use API for downloading projects, your backpack, and more
  - 100% reliable and secure (won't steal your passwords!)

# Installation
```bash
git clone https://github.com/themysticsavages/scratchhh.xyz
cd scratchhh.xyz
python -m pip install -r requirements.txt
```

## Config
Modify the application with `application/config.json`
```bash
cat application/config.json
{
  "port": 2000,
  "host": "0.0.0.0",
  "ip_bans": [
  ],
  "pid_bl": [
    "10128407"
  ]
}
```
`ip_bans` is used to ban users by public IP, and `pid_bl` is simply a blacklist for projects.

## Endpoints
Pretty much every endpoint with docs (there is a lot of them)

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

### GET /search/

*Response: HTML*
Search for Scratch projects by name.

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

### GET /api/gists/getbyid

*Response: JSON*
<br>
Get a gist by it's ID.

Parameters:
  - `id`

### GET /api/gists/all

*Response: JSON*
<br>
Return all posted gists, their information, and the count for convenience.

### GET /api/gists/post

*Response: redirect()*
<br>
Post a gist! Like how GitHub gists are (mostly) snippets of text code, Scratchhh gists are snippets of Scratch blocks.

Parameters:
  - `u` (user)
  - `p` (pass)
  - `c` (content)
  - `t` (title)

### GET /gists/

*Response: HTML*
<br>
Return a barely edited copy of the index page; used to search for gists by ID.

### GET /gists/:ID:

*Response: HTML*
<br>
Return a gist and it's blocks.

## The End
lol
