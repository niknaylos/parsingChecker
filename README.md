Parse sitemaps, check if <news:news> is present on sitemap, +
else flag it as False, +
put <loc> into variable, +

#TODO
if no <loc> check if <sitemap> is present,
try opening <sitemap>,
if no <sitemap> – invalid media, 
repeat func,
if <loc> is present check if <lastmod> or <news:publication_date> is present,
check if publication date is not older than 2 months ago,
check if <news:language> is present. If not – flag = False.

Check if metatags are present on webpage:
a) og:type content: article,
b) og:locale OR html/lang OR Content-Type = "en",
/// if both are not present – check if <news:language> flag is True, if not – media invalid.
