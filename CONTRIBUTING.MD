# Contributing

Thank you for showing interest in contributing. We hope you will find what you
need to get started on this page.

## Contributions

Contributions to [python-em511](https://github.com/id8-engineering/python-em511)
are done via
[pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

> Pull requests let you tell others about changes you've pushed to a branch in
> a repository on GitHub. Once a pull request is opened, you can discuss and
> review the potential changes with collaborators and add follow-up commits
> before your changes are merged into the base branch.

Pull requests should target the `main` branch.

###  Structuring your commits

More often than not, your pull request will come as a set of commits, not just
a single one.

In that case, please make sure that each commit constitutes a cohesive, logical
whole, e.g.  modifies a given package, function, or application layer. There are
many ways to conceptually divide your changeset, depending on its size and
content - this is up to you. It's just important that unrelated changes are not
mixed up together in unrelated commits.

This is to ensure that:
* your PR is easy to browse and review
* git log is easier to digest

Read [How to Write a Git Commit Message](https://cbea.ms/git-commit/), for more
on this topic.

#### Conventional Commits

We adhere to
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#specification).

> A specification for adding human and machine readable meaning to commit messages

tldr; in general your contribution will fall into one of two categories:

* A fix

  ```
  fix: <description of the fix>

  <More detailed explanation of the commit>

  Ticket: <None|Ticket Nr> (optional)
  ```

  Example:

  >```
  >fix(mda310): fix Wh decoding
  >```

* A new feature

  ```
  feat: <description of the new feature>

  <More detailed explanation of the commit>

  Ticket: <None|Ticket Nr> (optional)
  ```

  Example:

  >```
  >feat(mda310): add ready property
  >```

* A chore

  ```
  chore: <description of the chore>

  <More detailed explanation of the commit>

  Ticket: <None|Ticket Nr> (optional)
  ```

  Example:

  >```
  >chore: add more debug logs to scan receptacles path
  >```

Allowed commit types are:

```
feat,fix,docs,style,refactor,test,build,perf,ci,chore,revert,merge,wip
```

Multiple changes are allowed in a single commit, using footers:

```
feat: adds v4 UUID to crypto

This adds support for v4 UUIDs to the library.

fix(utils): unicode no longer throws exception
  BREAKING-CHANGE: encode method no longer throws exception
feat(utils): update encode to support unicode
```
