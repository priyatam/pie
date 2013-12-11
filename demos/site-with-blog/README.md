This is a sample site with blog created using [Literatte](https://github.com/Facjure/literatte).

Structure:

- templates: HTML5 + Mustache
- styles: CSS3, SCSS or LESS (pre-processed by lit.py automatically)
- lambdas (optional): custom logic, implemented as mustache lambdas

For content, we'll reuse literatte's 'docs' folder.

Optional site configuration, like first page, title, etc., is stored in `config.yml`.

Though _contents, design, and logic_ are distributed across the filesystem, Literatte brings them together and generates a static site,
with dynamic behavior injected into index.html (back button, logic).

## Usage

    lit.py /path-to-literatte/demos/site-with-blog /path-to-literatte/docs
    
    open -a "/Applications/Google Chrome.app" .build/index.html


Simplicity *is* possible.
