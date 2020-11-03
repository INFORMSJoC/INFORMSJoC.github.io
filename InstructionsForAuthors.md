# Procedures for submission of accompanying software and data

IJOC now hosts accompanying software and data within the [IJOC Github
organization](https://github.com/INFORMSJoC).

## Repository layout

Your repository layout should resemble that of this template to the extent
possible, although some variations may occur. In general, the repository
contents should be as follows.

 * `README.md` should describe the contribution, how to use it, how to cite
   it, and how to replicate the experim,ents in the paper, following roughly
   the format of the example. Note that the `.md` extension means "markdown,"
   a simple text formatting language you can learn about
   [here](https://guides.github.com/features/mastering-markdown/).
   
 * `LICENSE` should be a file containing the text of the license under which
   you intend to distribute the software and/or data. You must provide a
   license in order for the material to be used by others. An open source
   license is preferred (see the list of approved license at [Open Source
   Initiative](https://opensource.org/licenses), the license should allow free
   academic use at a minimum. Recommended licenses include the [MIT
   License](https://opensource.org/licenses/MIT) for software or any of the
   various [Creative Commons licenses](https://creativecommons.org/licenses/)
   for other types of material.

 * `AUTHORS` is an optional file, standard in the open source world, that
   lists the authors of the contribution (usually just a list of names and
   e-mails.

 * Depending on how you want to organize things, you may also have a
   `Makefile` or other files needed to build the software and/or run the
   experiments.

 * Subdirectories

   * `src` should contain the source code for any software.

   * `data` should contain data files needed for expeirments or used in the
     paper.
     
   * `scripts` should contain any scripts used to replicate the experiments in
     the paper or run other automated tests or experiments.

   * `docs` contains any additional documentation. Note that it is possible for
      the contents of `docs` to be a Web site that will be hosted under the
      URL https://INFORMSJoC.github.io/NameofRepo. Please let us know if you
      are interested in activating that option.

   * `results` should containing any raw results from the paper, as well as
     any plots or figures.

You may wish to have an additional README.md in any of the subdirectories to
provide additional information.

## Preparing your repository

Once your paper enters the review process, the Area Editor will create a
private repository from this template and give you read access to it. To
populate the repository with your own materials, fork it to make a copy that
will live in your own Github account. Once you populate and customize the
repository to your liking, open a Pull Request to begin a review by the Area
Editor. Once changes are accepted, the review process will begin.


## Review process 

As part of the review process, additional changes may be requested. These can
also be submitted by Pull Request.

## Legal stuff

Please ensure that all files contain proper copyright and licensing statements
and that the copyright holders have been notified of the submission. The
copyright holder may or may not be you, depending on your employment contract
and who funded the work.

## Version number and DOI

The version of the software and/or data associated with the paper will be
tagged in Github as a release and given both a version number and a DOI. The
default version number would be 1.0, but if the software is already under
development and has a versioning scheme (or you just want a different version
number), let the Area Editor know.

## FAQs

 * In the process of the review, changes were made to the software and/or
 data that was originally submitted and I don't want the original version of
 the software or data to be made public. Can you delete the history associated
 with the repository before making it public?

   * We can replace the repository used for the review process with a clean
     copy if you do not want the history made public.

 * What if I have an existing repository where the software is already being
   developed? Can I continue to develop there?

   * We expect this to sometimes be the case. In general, we would still like
     to archive the version of the software and/or data associated with the
     paper itself in a static repository withink the IJOC Github organization.
     If you wish us to fork or move an existing repository into the IJOC
     organization as part of the submission process, that can be discussed.

 * What if I don't already have an existing repository, but I want to continue
   developing the software after the paper is published?

   * This is highly encouraged, but further development should take place a on
     a personally managed site on Github or one of the other similar sites.
     You should put a link to the site where you will manage the software in
     the long-term in the README.md in the IJOC reporitory to ensure people
     can find your development site.

 * What if I later find a bug in the software and I want to fix it?

   * Please contact the Area Editor and we will determine the best course of
     action.

 * If I come out with a new version of the software later on, can I add it to
   the existing repository within the IJOC organization?

   * The answer to this may evolve over time. Please contact us if/when this
     happens and we will make a determination.