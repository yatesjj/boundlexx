# Git Workflow for Boundlexx Modernization (Using Your Fork)

## 1. Set Up Remotes
- `origin` should point to your fork: https://github.com/yatesjj/boundlexx
- `upstream` should point to the original: https://github.com/AngellusMortis/boundlexx

### Example Setup
```sh
git remote set-url origin https://github.com/yatesjj/boundlexx.git
git remote add upstream https://github.com/AngellusMortis/boundlexx.git
```

## 2. Keeping Your Fork Up to Date
- Regularly fetch and merge changes from upstream:
```sh
git fetch upstream
git checkout master
git merge upstream/master
# Resolve conflicts if any, then push to your fork
git push origin master
```

## 3. Feature Branch Workflow
- Create a new branch for each change or modernization step:
```sh
git checkout -b feature/short-description
```
- Make and commit your changes:
```sh
git add .
git commit -m "Short, descriptive message"
```
- Push your branch to your fork:
```sh
git push origin feature/short-description
```
- Open a Pull Request (PR) on GitHub from your branch to `master` in your fork.

## 4. Rollback and History
- Use `git log` to view history.
- Use `git revert <commit>` to undo a specific commit.
- Use `git checkout <commit> -- <file>` to restore a file from history.

## 5. Best Practices
- Keep PRs focused and small for easier review.
- Reference the modernization tracking log in PR descriptions.
- Tag releases or milestones for major steps.

---
For more details, see the modernization tracking log and Copilot instructions.
