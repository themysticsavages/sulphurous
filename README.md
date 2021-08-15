# scratchhh.web (wip)

![root](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.web.png)

scratchhh.web is a clone of the website [scratch.mit.edu](https://scratch.mit.edu). This clone offers a calm dark mode and easy access to project downloading (in an non-obvious way).
I'm planning to make this availible on the domain **scratchhh.xyz**, but for now, you can access it [here](https://scratchhhweb.ajskateboarder.repl.co). This uses flask and scratchhh.

## `/projects` endpoint
Make a GET request to return project information in nicely styled HTML.

![search](https://raw.githubusercontent.com/ajskateboarder/stuff/main/scratchhh.web/scratchhh.proj.png)

https://{domain}/projects/{id}

## `/projects/<id>/get` endpoint
Make a GET request to return a Scratch project download .sb3
