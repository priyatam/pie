This is a sample site with blog created using [Frozen Pie](https://github.com/priyatam/frozen-pie).

Structure:

- templates: HTML5 + Mustache
- styles: CSS3 (or copy your compiled scss or less files here)
- lambdas (optional): custom logic, implemented as Python functions

For content, we'll reuse frozen-pie's `docs` folder.

Optional site configuration, like first page, title, etc., is stored in `config.yml`.

Though _contents, design, and logic_ are distributed across the filesystem, frozen-pie brings them together and generates a static site, with all content injected into index.html as pages with back button support, automatic routes, and custom logic.

## Usage

    pie.py /path-to-pie/demos/site-with-blog /path-to-pie/docs
    open -a "/Applications/Google Chrome.app" /path-to-pie/demos/site/index.html
