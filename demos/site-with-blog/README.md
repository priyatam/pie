This is a sample site with blog created using [Literatte](https://github.com/Facjure/literatte).

Structure:
    - lambdas: custom logic implemented as mustache lambdas
    - styles: scss, less, css files (pre-processors automatically applied)
    - templates: mustache templates with HTML5

For content, we'll reuse literatte's 'docs' folder.

Optional site configuration, like first page, title, etc., is stored in config.yml.

As you can see, content, design, and logic is distributed across the filesystem--yet Literatte brings them together, and generates a static site,
complete with back button, and responsiveness.

## Usage

    alias pie=/path-to-literatte/pie/pie.py
    
    pie --root=/path-to-literatte/demos/site-with-blog --contents=/path-to-literatte/docs
    
    open -a "/Applications/Google Chrome.app" .build/index.html


Simplicity *is* possible.
