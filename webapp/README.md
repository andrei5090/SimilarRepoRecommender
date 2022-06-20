# Hierarchy Visualiser
This repository represents the frontend for the application Hierarchy Visualiser: [Deployed app](https://hierarchy-visualiser.herokuapp.com/) developed by Andrei Ionescu during his Research Project CSE3000 (Bachelor Thesis) at the Delft University of Technology.

## Background
Developers do not want to reinvent the wheel when establishing a new software system. Open-source software
repositories are packed with resources that may assist developers with their work. Our research intends to
assist developers in locating such resources, allowing them to concentrate on the essential functions of an
application or system rather than implementing fundamental functionalities from scratch.
Each repository tag englobes knowledge about the application that is developed in a particular repository,
and a set of tags represents the architecture, and the overall system characteristics and dependencies.
Since GitHub enabled the repository tagging, a new opportunity arose to help the developers to find the
needed resources based on their needs.

The currently available literature and tools do not offer many solutions directly related to recommending
similar repositories which are tailored and based on the researcher or developer’s needs. Recommender
systems and tools can identify comparable repositories, but they focus on static approaches that can be
used just for a small number of repositories (e.g. Java Repositories). Furthermore, some of these approaches
are limited to their training data and cannot adapt to newly published repositories or technologies.
During our research, we aim to address the recommendation generality gap in recommending similar
repositories. 

## Project setup
```
npm install
```
Modify the `./.env` file with the adress on which the backend service runs ([Backend Repo](https://github.com/andrei5090/SimilarRepoBackend)).

Modify the `./.env.production` file with the adress on whitch the backend service runs in case you use it in production.

## How to run:
```
npm run serve
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

## Info
The application will lauch by default on the port `8080` and can be accessed using `localhost:8080`
