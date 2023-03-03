# Instructions for Setting up a Repo (Area Editors)

Below are the detailed steps for creating a Github repo associated with an IJOC paper. To execute these instructions, you must have already created a Github account and contacted Ted Ralphs to be added to the IJOC Area Editors group.

## Initial Setup (Editor)

- Go to https://github.com/INFORMSJoC 
- Sign in with userid and password (this probably won't need to be done every time)
- Click on NEW. This will take you to a page for setting up the repo.
- In the `Repository name`, type the new repository's name. 
  - The name should be in the form `XXXX.YYYY` (four numbers followed by four more numbers). 
  - These are derived from the manuscript ID. 
  - The first four are the year of submission and the second four are the numbers that come after the last dash (padded with an extra zero). 
  - The latter is just a sequence number that is incremented throughout the year across all papers. so if the manuscript ID is `JOC-2022-11-OA-354`, then the repo name is `2022.0354`.
- Keep the repository `Private`
- Check the box for `Add a README file`
- Click on CREATE REPOSITORY
- The repo has been created and you should now be on a new page with a button for `Add Collaborators and Teams`. Click on it.
- You may be asked to autheticate with your 2FA (this can vary, depending on your setup). Do this.
- On the next page, click the button for `Add People`
- Enter the Github ID(s) of the author(s) who will be adding to the repo in the search box (you will need to ask them about this separately and request them to create a Github account if they don't already have one).
- Click on the person to add in the dropdown list. 
- Choose `Read` for the role (important!)

## Populating the Fork (Author)

Now it is the the authors' turn.
- Inform the author(s) via email that they should follow the instructions [here](InstructionsForAuthors).
- The authors then take over by forking the empty repo  (the author(s) should have received an e-mail notification when the repo was created, but you may want to provide them with the URL) and populating that fork with their content. 
- This means copying it over from where they currently maintain it. Even if they already maintain the software/data on Github or in some other public forum, they need to populate this repo, which will become a fixed snapshot available in perpetuity and associated with the published paper.
- Then they will submit a so-called Pull Request, which is for your review. 

## Reviewing (Editor)

After the author(s) submit the Pull Request, you will be notified and you can go to the repo and see the Pull Request.

- To view the PR, it's easiest is to click on the link in the e-mail.
- Be sure to carefully review the contents to ensure that it is well-organized, that the README follows the format of the [template](https://github.com/INFORMSJoC/JoCTemplate), that everything is under a proper open source license and that there are appropriate copyright statements in files.
- You may want to also review the [instructions](InstructionsForAuthors).
- If you want to request changes, just comment on the Pull Request.
- After everything looks good, click on the merge button and confirm the merge.

## Archiving a snapshot (Editor)

Now it is time to make the release in order to create a snapshot of the repo, which is what the DOI will point to.  

- Make a release tag named `vXXXX.YYYY`, where `XXXX.YYYY` is the manuscript number, i.e., the name of the repo. Example: if `2021.0070` is the repo name, then `v2021.0070` is the version number. 
- To make the release, click on the link on the right side to "create a new release".
- Click the "choose a tag" dropdown and type the new release tag name in the dialogue. 
- Click on "Create new tag on publish"
- The release title and notes section can contain whatever you like. 
- Finally, publish the release.

YOU ARE ALL DONE!
