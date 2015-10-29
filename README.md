# The Axiologue API

The Axiologue project is about tracking the ethical histories of products and companies.  In part of our commitment to open, community-based sharing, our data is available as an open API.  This repo contains both the code underlying our data collection/organizing and a description for our API endpoints, for developers. For more information on the axiologue project, check out [axiologue.org](http://www.axiologue.org).

## API Description

Our Data is broken down into the following models:

* Company: Self-explanatory
* Product: Same
* Article: The sources from which our data is derived -- the article is essentially a link to an external source (journalism, NGO reports, company policies, etc), with metadata
* Catgories / Subcategories: The ethical taxonomy
* Tags / TagTypes: Instances and Descriptions of ethical facts (which are associated with articles, companies, and Products)
* User:
  * Preference: a numerical rating (-5 to 5) the indicates how a user feels about a given Tag.  Used to construct personalized rankings

## API Endpoints

#### Authentication

Some of our content is avialable without login.  However, editing Axiologue data will always require authentication (for many reasons, not the least of which is accountability).  Axiologue is set up to use Token authentication, with the following endpoints:

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required
-----------  |  --------  |  ------  |  -------------  | --------------
Login  |  http://api.axiologue.org/rest-auth/login  |  POST  |  username, password  |  No
Registration  | http://api.axiologue.org/rest-auth/regsitration/  |  POST  | username, password1, password2, email  |  No
Logout  |  http://api.axiologue.org/rest-auth/login/  |  POST  |   |   Yes
Password Change  |  http://api.axiologue.org/rest-auth/password/change/  |  POST  |  password1, password2  |  Yes
Password Reset  |  http://api.axiologue.org/rest-auth/password/reset/  |  POST  |  email  |  Yes
Get Profile Information  |  http://api.axiologue.org/rest-auth/user/  |  GET  |     |  Yes
Update Profile  |  http://api.axiologue.org/rest-auth/user  |  PATCH  |  data  |  Yes
Email Verification  |  http://api.axiologue.org/registration/verify-email/  |  POST  |  key  |  No
Password Reset Confirm  |  http://api.axiologue.org/password/reset/confirm/  |  POST  |  uid, token, password1, password2  |  Yes

#### Articles

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required
-----------  |  --------  |  ------  |  -------------  | --------------
All Tagged Articles  |  http://api.axiologue.org/articles/articles/tagged/  |  GET  |    |  No
All Untagged Articles  |  http://api.axiologue.org/articles/articles/untagged/  |  GET  |   |  No
All Articles w/out Relevant Data  |  http://api.axiologue.org/articles/noData/  |  GET  |   |  No
Add Article  |  http://api.axiologue.org/articles/new/  |  POST  |  url, title, notes  |  Yes
Edit Article  |  http://api.axiologue.org/articles/{ARTICLE:ID}/  |  PUT  |  url, title, notes, id  |  Yes
All Companies  |  http://api.axiologue.org/articles/companies/all/  |  GET  |  |  No

#### Tags

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required
-----------  |  --------  |  ------  |  -------------  | --------------
Create Ethics Tag  |  http://api.axiologue.org/tags/etags/new/  |  POST  |  company, subcategory, tag_type, excerpt, [value]  |  Yes
Edit Ethics Tag  |  http://api.axiologue.org/tags/etags/tagsID/  |  PUT  |  company, subcategory, tag_type, excerpt, id, [value]  |  Yes
Create New Ethics Type  |  http://api.axiologue.org/tags/etypes/new/  |  POST  |  subcategory, name  |  Yes
Mark Article as Having No Relevant Data  |  http://api.axiologue.org/tags/mtags/  |  POST  |  article  |  Yes
Remove No Relevant Data Tag  |  http://api.axiologe.org/tags/mtags/{TAG:ID}/  |  DELETE  |   |  Yes

#### Profile

Description  |  Endpoint  |  Method  |  Expected Data  | Login Required
-----------  |  --------  |  ------  |  -------------  | --------------
Get User's Ethical Preferences  |  http://api.axiologue.org/profile/prefs/all/  |  GET  |    |  Yes
Alter Individaul Preference  |  http://api.axiologue.org/profile/prefs/{PREF:ID}/  |  PUT  |  id, preference  |  Yes
Get Company Ranking  |  http://api.axiologue.org/profile/scores/company/{COMPANY:ID}/  |  GET  |  |  Yes


