# Sitemap Parser and Validator

This project aims to parse and validate sitemaps according to certain criteria. Below are the steps and checks performed by the code:

Parse sitemaps and check if `news:news` tag is present on sitemap.
   - If not, flag it as `False`.
   - If `loc` is present, checking if `lastmod` or `news:publication_date` tags are present.
   - If `loc` is not present, checking if `sitemap` tag is present.
   - Recursively check if nested sitemaps contain valid URLs
   - Ensure publication date is not older than 2 months.
   - `og:type` content set to `article` check.
## To-Do
- [ ] Check if `news:language` tag is present.
  - [ ] If not, flag it as `False`.
- [ ] Remove user inputs and base it on file reading

Check if the following meta tags are present on the webpage:
- [ ] `og:locale` or `html/lang` or `Content-Type` set to `en`.
   - If both are not present and `news:language` flag is not `True`, mark media as invalid.
