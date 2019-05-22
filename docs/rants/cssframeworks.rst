All CSS frameworks suck
=======================

This project, as many others of mine, started with Bootstrap 4. This was
the 1st choice for me because I had a previous knowledge of Bootstrap and it
was quite straightforward. But while popular and mature, Bootstrap has some
limitations and there are some things I don't like about it so I started
looking for alternatives. From this point a way downhill started.

Bulma, extreme divitis
----------------------

From the years back there is a word "divitis" that initially described a case
of HTML layout converted from tables to divs that replaced all table related
elements with divs. With the advent of contemporary HTML authoring this faded
and almost all references I found are from early 2000's. Then I stumbled upon
Bulma CSS framework. What's wrong with it? It discourages writing semantic
HTML to extreme point where all elements are stripped out of its visual
representation. HTML still may be semantic, but without styling with CSS
classes it's just a soup of visually indistinguishable texts. To apply any
visual representation one has to wrap semantic elements in bunch of
divs and spans that will apply any visual representation.

This is specially bad for template authoring. Without any styling, the template
content is cluttered with contextually meaningless divs and spans that are
there only for styling content. So for web application development with Flask
(or any traditional request-response method) this is more a problem than a
cure.
