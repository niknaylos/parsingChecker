# Sitemap Parser and Validator

This project aims to parse and validate sitemaps according to certain criteria. Below are the steps and checks performed by the code:

  Parse sitemaps:
   - check if `news:news` tag is present on sitemap, If not, flagging it as `False`.
   - If `loc` is present, checking if `lastmod` or `news:publication_date` tags are present.
   - If `loc` is not present, checking if `sitemap` tag is present.
   - Recursively check if nested sitemaps contain valid URLs
   - Ensure publication date is not older than 2 months.
   - Checking if `og:type` tag exists and its content is set to `article`.
   - Check if the following meta tags are present on the webpage:
           `og:locale` or `html/lang` or `Content-Type`
## To-Do
- [ ] Remove user inputs and base it on file reading



