# NeSI Performance Optimisation Training

Training materials for hands-on workshops on performance optimisation.

View the content here:
[https://nesi.github.io/perf-training/](https://nesi.github.io/perf-training/).

## Developing content

### Adding a new section

1. Create a new file in *sections/*, based on the files that are already
   there, with unique `permalink` and `chapter`. The `order` value is used to
   detemine the order they appear in the list on the website.
2. Edit *_config.yml* and add the new section file to the `header_pages` list.
3. Create a folder under *_lessons/* with the name used in `permalink` above.
   This is where the lessons will go.

### Adding a new lesson

1. Create a new file in the *sections/<section_name>/* folder, based on files
   that are already there.
2. Make sure the `permalink` is unique.
3. Make sure `chapter` matches the chapter that was set in the corresponding
   section file.

### Viewing HTML pages locally

Ruby and bundler are required.

In the main repo directory run:

1. `bundle install --path vendor/bundle`
2. `bundle exec jekyll server` (run the web server)
3. View web page, probably at: http://127.0.0.1:4000/perf-training/
