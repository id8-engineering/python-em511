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
Sign your work
--------------

This project is licensed under an open source license. To ensure license compatibility and traceability, we need to keep track of the origin of all commits and make sure they comply with the license terms.  
To achieve this, we follow the same procedure as used by the Linux kernel and many other open source projects: **every commit must be signed off**.

The sign-off is a simple line added at the end of your commit message which certifies that you wrote the code or otherwise have the right to pass it on as an open source contribution.  
The rules are simple: if you can certify the following statement (from [developercertificate.org](http://developercertificate.org)), then you can sign off your work.

### Developer Certificate of Origin
**Version 1.1**

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.  
660 York Street, Suite 102,  
San Francisco, CA 94110 USA  

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

#### Developer’s Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I  
    have the right to submit it under the open source license  
    indicated in the file; or  

(b) The contribution is based upon previous work that, to the best  
    of my knowledge, is covered under an appropriate open source  
    license and I have the right under that license to submit that  
    work with modifications, whether created in whole or in part  
    by me, under the same open source license (unless I am  
    permitted to submit under a different license), as indicated  
    in the file; or  

(c) The contribution was provided directly to me by some other  
    person who certified (a), (b), or (c) and I have not modified it; and  

(d) I understand and agree that this project and the contribution  
    are public and that a record of the contribution (including all  
    personal information I submit with it, including my sign-off) is  
    maintained indefinitely and may be redistributed consistent with  
    this project or the open source license(s) involved.

---

Then you just add a line to every git commit message:
```bash
Signed-off-by: Your Name your.email@example.com
````

Use your real name (no pseudonyms or anonymous contributions).

If you have set your `user.name` and `user.email` in Git, you can sign off your commits automatically by using:

```bash
git commit -s -m "feat: add new feature"
````

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
