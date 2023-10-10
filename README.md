# Sitemap Parser and Validator

This project aims to parse and validate sitemaps according to certain criteria. Below are the steps and checks performed by the code:

1. Parse sitemaps and check if `news:news` tag is present on sitemap.
   - If not, flag it as `False`.
   - Put `loc` into a variable.

## To-Do
- [ ] If `loc` is not present, check if `sitemap` tag is present.
- [ ] Try opening `sitemap` tag.
  - [ ] If `sitemap` is not present, mark media as invalid.
- [ ] Repeat the function to ensure complete validation.
- [ ] If `loc` is present, check if `lastmod` or `news:publication_date` tags are present.
- [ ] Ensure publication date is not older than 2 months.
- [ ] Check if `news:language` tag is present.
  - [ ] If not, flag it as `False`.

## Meta Tags Validation
Check if the following meta tags are present on the webpage:
- `og:type` content set to `article`.
- `og:locale` or `html/lang` or `Content-Type` set to `en`.
   - If both are not present and `news:language` flag is not `True`, mark media as invalid.
