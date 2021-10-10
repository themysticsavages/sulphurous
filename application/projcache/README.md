The projcache directory

> When projects are downloaded, they get saved in sub directories. So for example, if a user downloaded project `569068479`, it would get saved to `projcache/569068479/`. If that project doesn't exist yet, it will download it with `-0` appended and will be served to the user. If it does exist, it will be checked for differences. If the project is not different at all, the current project will be given. So until project `569068479` is changed - for example - the same version will always be given. But if the project is indeed different, the project will be downloaded with the number after the previous project. So if `project569068479-0.sb3` exists, it will downloaded as `project569068479-1.sb3`.

> Oh, and in addition to projects, users' backpacks are also stored here temporarily. If a user requests `/backpack/get` if logged in, the server will fetch all assets from `assets.scratch.mit.edu` that are sounds or pictures, put them in a ZIP directory, and will be given to the user. After it is served, it will be deleted.

(If I add gist exporting, I may store it here, and simply name the folder `cache`.)
