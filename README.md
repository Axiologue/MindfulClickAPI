# The Mindful Click API

The Mindful Click project is about tracking the ethical histories of products and companies.  In part of our commitment to open, community-based sharing, our data is available as an open API.  This repo contains both the code underlying our data collection/organizing and a description for our API endpoints, for developers. For more information on the axiologue project, check out [axiologue.org](https://www.axiologue.org).

## API Description

Our Data is broken down into the following models:

* Company: Self-explanatory
* Product: Same
* Reference: The sources from which our data is derived -- a reference is essentially a link to an external source (journalism, NGO reports, company policies, etc), with metadata
* Categories / Subcategories: The ethical taxonomy
* Tags / TagTypes: A TagType is a specific kind of ethical fact (such as "50% reduction in carbon use" or "No sexual harassment policy"). A Tag is a single instance tying a TagType to an reference and a product/company.  It is from this association that our data is derived 
* User:
* Preference: a numerical rating (-5 to 5) the indicates how a user feels about a given Tag.  Used to construct personalized rankings

## API Endpoints

#### Scores

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required | Query Parameters
-----------  |  --------  |  ------  |  -------------  | -------------- | ----------------
All Company Scores | https://api.mindful.click/profile/scores/company/all/ | GET | | No (for Generic Scores), Yes (for Personal Scores) | include_subcategories, include_object, use_generics, use_fuzzy_fetch 
Company Score | https://api.mindful.click/profile/scores/company/ | GET | | No (for Generic Scores), Yes (for Personal Scores) | name, id, include_subcategories, include_object, use_generics, use_fuzzy_fetch 
Product Score | https://api.mindful.click/profile/scores/product/ | GET | | No (for Generic Scores), Yes (for Personal Scores) | name, id, include_subcategories, include_object, use_generics, use_fuzzy_fetch 

#### Products

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required | Query Parameters
-----------  |  --------  |  ------  |  -------------  | -------------- | ----------------
Product List | https://api.mindful.click/products/products/list/ | GET |    | No | none, name, company, company_id, price_min, price_max, category, division
Product Detail | https://api.mindful.click/products/products/{PRODUCT:ID}/ | GET |    | No | 
Add Product | https://api.mindful.click/products/products/new/ | POST | name, company_id, price [optional: category, division, image_url] | Yes | 

#### Companies

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required | Query Parameters
-----------  |  --------  |  ------  |  -------------  | -------------- | ----------------
All Companies | https://api.mindful.click/products/companies/all/ | GET |    | No |
Company Detail | https://api.mindful.click/products/companies/{COMPANY:ID}/ | GET |    | No |
Company Detail (alt) | https://api.mindful.click/products/companies/{COMPANY:NAME}/ | GET |    | No |

#### References

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required | Query Parameters
-----------  |  --------  |  ------  |  -------------  | -------------- | ----------------
All Tagged References  |  https://api.mindful.click/references/tagged/  |  GET  |    |  No
All Untagged References  |  https://api.mindful.click/references/untagged/  |  GET  |   |  No
All References w/out Relevant Data  |  https://api.mindful.click/references/noData/  |  GET  |   |  No
Add Reference  |  https://api.mindful.click/references/new/  |  POST  |  url, title, notes  |  Yes
Edit Reference  |  https://api.mindful.click/references/{REFERENCE:ID}/  |  PUT  |  url, title, notes |  Yes

#### Tags

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required | Query Parameters
-----------  |  --------  |  ------  |  -------------  | -------------- | ----------------
Create Ethics Tag  |  https://api.mindful.click/tags/etags/new/  |  POST  |  company, subcategory, tag_type, excerpt, [optional: value]  |  Yes
Edit Ethics Tag  |  https://api.mindful.click/tags/etags/{TAG:ID}/  |  PUT  |  company, subcategory, tag_type, excerpt, [optional: value]  |  Yes
Create New Ethics Type  |  https://api.mindful.click/tags/etypes/new/  |  POST  |  subcategory, name  |  Yes
Mark Reference as Having No Relevant Data  |  https://api.mindful.click/tags/mtags/  |  POST  |  reference  |  Yes
Remove No Relevant Data Tag  |  https://api.axiologe.org/tags/mtags/{TAG:ID}/  |  DELETE  |   |  Yes

#### Profile

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required | Query Parameters
-----------  |  --------  |  ------  |  -------------  | -------------- | ----------------
Get User's Ethical Preferences  |  https://api.mindful.click/profile/prefs/all/  |  GET  |    |  Yes
Alter Individaul Preference  |  https://api.mindful.click/profile/prefs/{PREF:ID}/  |  PUT  |  id, preference  |  Yes
User Account Info | http://api.mindful.click/rest-auth/user/ | GET | | Yes | 

#### Authentication

Some of our content is avialable without login.  However, editing Mindful Click data will always require authentication (for many reasons, not the least of which is accountability).  Mindful Click is set up to use Token authentication, with the following endpoints:

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required | Query Parameters
-----------  |  --------  |  ------  |  -------------  | -------------- | ----------------
Login  |  https://api.mindful.click/rest-auth/login  |  POST  |  username, password  |  No
Registration  | https://api.mindful.click/rest-auth/regsitration/  |  POST  | username, password1, password2, email  |  No
Logout  |  https://api.mindful.click/rest-auth/login/  |  POST  |   |   Yes
Password Change  |  https://api.mindful.click/rest-auth/password/change/  |  POST  |  password1, password2  |  Yes
Password Reset  |  https://api.mindful.click/rest-auth/password/reset/  |  POST  |  email  |  Yes
Get Profile Information  |  https://api.mindful.click/rest-auth/user/  |  GET  |     |  Yes
Update Profile  |  https://api.mindful.click/rest-auth/user  |  PATCH  |  data  |  Yes
Email Verification  |  https://api.mindful.click/registration/verify-email/  |  POST  |  key  |  No
Password Reset Confirm  |  https://api.mindful.click/password/reset/confirm/  |  POST  |  uid, token, password1, password2  |  Yes

