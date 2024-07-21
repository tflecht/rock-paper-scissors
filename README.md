# localdev - local development environment for Mood4
localdev let's you easily run Mood4's components and interact with them from your host OS (e.g. via a web browser). It is inspired by [this](https://blog.moove-it.com/vagrant-multiple-projects/) blog post.


## A workflow for developing against components from localdev
The `localdev` repository (.git)ignores the existance of the github repositories cloned under it used by each of the guest hosts. 

You can edit the files of those repositories locally, and manage branching, committing, pushing up changes, pulling down new changes, etc from each of those subdirectories (e.g. when you run git commands from within localdev/gamers_service, you are running them against the `gamers_service` repository (either locally or upstream).

So, just develop against any of those repositories like you normally do with your workflow and interacting with git and github.

You can also make changes to `localdev`, just like any other repository. Keep in mind that `localdev` knows a lot about the other repositories, but those other repositories can't depend on `localdev` in any way; doing so would break other development workflows and shared qa, sandbox and production environments.


# Using docker(-compose) to start/stop/build components
Comand to build:
docker compose build

Command to start:
docker compose up
docker compose up service # for example, to individually start service

Command to stop:
docker compose down
docker compose down service # for example, to individually stop service

Command to run tests:
docker compose exec service make test

