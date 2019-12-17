Application functionality
=========================

I found the requirements for the application slightly changed over time. This
makes it ever changing and evolving, and requires the spirit of constant
refactoring. Fortunately I don't think about it in terms of product that
should have a timeline and finally hit the market in somewhat finished state.
It's fun it gives me something to think about and look for improvement in both
my code and myself.

Some of these changes are described in detail in
:doc:`concepts document </concepts>` but these are rather related to
technology, not the application functionality and features.

So what are exactly functional requirements? I decided to gather this list to
have some contract with myself.

Accounts and users
------------------

Single user, single account. The account is administrator and owns all items
in site inventory. Site visitors are either anonymous or it's the site owner.
There is no account registration, the only user account is created from
command line. If there are more registered users, they all have full
administrative access to everything.

How about used friendliness of such solution? Well, there is a proverb saying
that Unix is user friendly but has high standards in deciding who is his
friend. I generally find command line operations as very friendly towards me
so I consider CLI as user friendly. Anyway, what's the problem? You login to
remote site with SSH, you do other site maintenance commands from CLI (like
create database, lauch nginx, etc) so why not create user accounts from command
line?

Blogging
--------

There are possibly many blogs, all owned by the same user. One of the blogs
is the default which is displayed on main page, others require to switch
context. First created blog becomes automatically default but this may be
changed later.

Each blog consist of posts. Posts are written in Markdown. Posts can be
written on site or imported from Markdown files with YAML metadata (like in
eg. `Jekyll <https://jekyllrb.com/docs/front-matter/>`_). Post may have some
metadata like labels (or *tags*) or mood. One post at a time in any blog may
be pinned and will be displayed at timeline top, and posts may be marked as
drafts. Only non-draft posts are displayed for anonymous users. By definition
all posts are public.

Other kind of content is pages but in fact this is only an attribute of post.
Page is special only in presentation, not in object kind. Pages are composed
exactly in the same way as posts.

Social features
---------------

There are no social features because I am antisocial.
