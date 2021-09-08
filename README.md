# scratchhh.tk (wip)

![root](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.web.png)

scratchhh.tk is a clone of the website [scratch.mit.edu](https://scratch.mit.edu). This clone offers a calm dark mode and easy access to project downloading (in an non-obvious way).
It's obviously available [here](https://scratchhh.tk)

## `/projects` endpoint
Make a GET request to return project information in nicely styled HTML.

![search](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.proj.png)

https://{domain}/projects/{id}

## `/projects/<id>/get` endpoint
Make a GET request to return a Scratch project download .sb3

## `projects/<id>/comments/get` endpoint

![comm](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.comm.png)

Make a GET request to return top 3 Scratch comments as HTML.
