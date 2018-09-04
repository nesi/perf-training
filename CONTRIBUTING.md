# Contributing to NeSI's HPC training

## Found a problem?

If you find a problem with the training material we are happy to receive Pull Requests with fixes
(see [How to make a contribution](#how-to-make-a-contribution)), otherwise let us know what the problem is:

* [open an issue](https://github.com/nesi/perf-training/issues)
* email [training@nesi.org.nz](mailto:training@nesi.org.nz)

## How to make a contribution

If you would like to contribute to the NeSI documentation and training material, you can do so in many ways:

1. Create a branch for the changes you are going to make (```git checkout -b <my_branch>```)
   * If you have access, you can create the branch directly in the main repository
   * Otherwise, fork the repository and work in a branch within your fork
2. Make your changes
   * Use a style consistent with the lesson you are editing and the guidelines here
   * Make sure that the content renders correctly when viewing the web version (for example, 
     see [Building the web version locally](#building-the-web-version-locally))
3. Create a Pull Request into the `gh-pages` branch of the main repository
4. Someone will review your Pull Request and may request additional changes before accepting

## Content structure and style guidelines

All material is organised in lessons (in the `_lessons` folder and then relavant subfolders) and
written in GitHub flavoured Markdown. When contributing, please use this structure and formatting
and follow the guidelines:

* Don't add a top level heading (`#`) for the title of the page -- the title will be generated from the
  lesson metadata
* Use level 2 headings (`##`) and lower (if required) to split the lesson into sections
* Every lesson should start with an "Objectives" section that should lists the lesson's objectives
* Follow Oxford spelling and punctuation
* No person name should appear in the material. Blank out any personal information if you need to take a screenshot
* No prompt symbol in verbatim code blocks, users should be able to copy paste the commands as they appear

## Building the web version locally

Ruby and bundler are required.

In the main repo directory run:

1. `bundle install --path vendor/bundle`
2. `bundle exec jekyll server` (run the web server)
3. View web page, probably at: http://127.0.0.1:4000/hpc_training/
