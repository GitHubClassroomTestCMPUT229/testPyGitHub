from github import Github

# Generate token for github:
#   https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
#   Access token: f91c7b257571da2dba998379826e94d72b16fada
# PyGithub users & organizations:
#   https://github.com/PyGithub/PyGithub/issues/507

def main():
    token = "f91c7b257571da2dba998379826e94d72b16fada"
    g = Github(token)
    for x in g.get_user().get_repos():
        print x
    r = g.get_repo("GitHubClassroomTestCMPUT229/testMoss")
    print r
main()
