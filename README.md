# 365

A photo a day, by [Chris Becker](http://becker.am)

## About

I chose to document my 25th year alive on this planet with a 365 project, also
known as “a photo a day.” I’ve tried to do one in the past, and got pretty far,
but ended up giving up.

After watching my good friend Ted Rysz document his 25th year on instagram, I’m
going to give it another try… this time on film.

Each day’s picture will appear on the site when I get the roll developed. Expect
updates around once a month!

## Technology

This website is written in Markdown and SASS, and compiled down to pure HTML/CSS
with [Jekyll](http://jekyllrb.com).

The website is hosted on S3 with CloudFront handling caching and HTTPS
redirection. Since this site is image-heavy, I decided to investigate a caching
solution and CloudFront's first-tier S3 support made that a no-brainer. SSL was
a bonus.

I wrote some handy little [fab](http://www.fabfile.org/) scripts to manage some
of the more monontinous tasks that come with a dynamically generated static
site.

## License

As always, MIT. See the `LICENSE` file for more information.
