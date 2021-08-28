# scratchhh.web (wip)

![root](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.web.png)

scratchhh.web is a clone of the website [scratch.mit.edu](https://scratch.mit.edu). This clone offers a calm dark mode and easy access to project downloading (in an non-obvious way).
I'm planning to make this availible on the domain **scratchhh.xyz**. This uses flask and scratchhh.

## `/projects` endpoint
Make a GET request to return project information in nicely styled HTML.

![search](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.proj.png)

https://{domain}/projects/{id}

## `/projects/<id>/get` endpoint
Make a GET request to return a Scratch project download .sb3

## `/projects/<id>/comments/get` endpoint
Retrieve 3 comments from a Scratch project in raw HTML.

![search](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.comm.png)

## `/projects/<id>/embed` endpoint
Get a minimal version of a project from scratchhh.tk. Best used in embeds, obviously
