# Frozen Pie
        
> You know you have reached perfection in design, not when there is nothing more to add, but when 
there is nothing more to be taken away - Antoine de Saint-Exupery


Today's static site generators require css, markup, templating and programming skills. Their compatibility is broken. A template in one framework doesn't work in the other. You can't mix and match languages, and add custom features in a decoupled way. You can't take a Designer's template and pipe data structures and lambdas. You can't let them both work in total independence.

And then you check for hosting, browser compatibility, plugins that blow on your face. 
 
These toolkits are built for a different mindset. For different abstractions. It requires a lot of work to perform simple tasks, like changing design on the fly, add behavior on the fly with a single lambda, cook a frozen pie from recipe. Things shouldn’t be this way. Not in Python.
    
**Frozen Pie** - a static site generator using Markdown, Mustache, and HAML.
   
create_crust
> Create content (posts and pages) in Markdown
    
put_in_pan
> Put in a logic-less templates with HAML-Mustache
    
add_filling
> Add config data in any content or template with YAML 
    
add_recipes
> Add someone else's flavors

bake_in_oven
> Compile everything into a single index.html, scripts and styles included
    
serve
> git push index.html :gh-pages
    

Under active development. Not usable until a stable release. License: GPLv3
    
