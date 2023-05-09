# Workflow for code contributions
The followinging describes a workflow for how contributions to the code base can be done.
This is particularly relevant for the simulation engine Resie, but the same applies for
other code-heavy parts of the QuaSi project. It is oriented by a popular approach often
called the "git feature-branch workflow". It is assumed the reader generally knows how to
use git, for which there are many tutorials and guides available.

To illustrate the workflow, let's imagine Resie is released on GitHub on version 1.2.3
and Alice wants to add a new energy system component to the simulation model. The workflow
can also work if another repository host other than GitHub is used and can also be
performed entirely with repositories in folders in a local network.

#### Branch-basis
The releases are simply specific commits in the commit-graph of the project and usually the
`HEAD` position of the `main` branch. This is the basis for the changes and new code Alice
wants to make. If Alice has the corresponding rights on the repository, she can create a
new branch from this commit within the same repository. The branch name ideally should
indicate if the changes will be a new feature, a bugfix, refactoring of code, documents
or other changes.

If Alice does not have permission to create a branch, she can fork the repository to her
own account via GitHub's fork functionality and work on the main branch of the fork. In
either case we call this the feature branch in the context of this workflow.

#### Making changes
Alice can now make changes on the feature branch, committing changes in any number of
commits. This can be done all in one big commit containing all changes, but many developers
prefer a finer granularity. Similarly, a well chosen commit message makes later development
easier as it becomes faster to reason about the impact of the code changes. There are many
approaches to how commits can be used and personal preference plays a large role.

#### Open a merge request
Once Alice is confident all required changes are comitted, she can open a merge request
(also called a pull request) in the Resie repository from the feature branch to the `main`
branch. If the feature branch lives on another repository this requires selection of that
repository, but otherwise works the same. The request ideally contains a description of
what the changes entail and how they impact the code base (specifically, if they change any
of the core functionality or add new one).

With the merge request open, other developers can review the changes and make comments on
which parts can be improved or require further changes to comply with rules and guidelines
of the project. At any time Alice can make changes addressing the comments and push them to
the feature branch, which will be automatically reflected in the merge request.

For example, Bob might point out that a function name is misspelled. Alice creates a new
commit fixing the name of the function and pushes to the feature branch. Bob can then
delete the comment as it no longer applies and approve the merge request.

When the request is approved, the commits are ready to be merged, but there is one more
commit to be done as described in the next section.

#### Version bump
All changes to the code base should be reflected in the changelog and cause an increase in
the version number. Therefore Alice has to make sure her changes appear in the changelog.

First the `main` branch is merged into the feature branch if other commits have
been done inbetween the base commit of the feature branch and the current `HEAD` of `main`.
Perhaps someone made a bugfix and got it merged while Alice was still working on her
changes. Therefore the released version of Resie is now `1.2.4`. With the merge these
changes and the entry in the changelog now appears in the feature branch too. Optionally
the feature branch can be rebased so that no merge commit is necessary, but this is not
required.

Then Alice increases the version number in file `Project.toml` (this is specific to Resie)
to `1.3.0` and adds an entry in the changelog. Given that the changes are backwards
compatible and add new functionality, an increase in the minor version number is
appropriate. The commit for the version bump should contain the same message as the entry
in the changelog.

Alice then pushes the commit with the version bump and updates the merge request to
indicate that it is ready to be merged.

#### Merging, followup and cleanup
A developer with maintainer permissions (who may be Alice) can now merge the feature branch
into the `main` branch. It is possible that even more changes to the `main` branch have
been made in the meantime, but this is a problem best addressed by developer communication
as it would lead to merge conflicts in the changelog. This merge should not cause any
conflicts.

Some other things that may follow the merge of the code changes:
* Deleting the feature branch as it no longer needed
* Tagging the merge commit as a new release within GitHub and other systems
* Updating the documentation for new functionality
* Checking if bugfixes have solved open issues so they can be resolved
