from github import Github

# Generate token for github:
#   https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
#   Access token:   f91c7b257571da2dba998379826e94d72b16fada
#                   18813125cc1330970de92d2c70332806ed35284a (All permissions)
#                   a889a5ec4ac33257aee6d29fb1da2c361d9f37d9
# PyGithub users & organizations:
#   https://github.com/PyGithub/PyGithub/issues/507
# create_team in: 
#   https://github.com/PyGithub/PyGithub/blob/master/github/Organization.py

def main():
    token = "a889a5ec4ac33257aee6d29fb1da2c361d9f37d9"
    g = Github(token)   # Ref to github.com using permissions granted by token
    org = g.get_organization("GitHubClassroomTestCMPUT229")

    team = None
    try:
        # Create new team
        # Adds a team called test_team to GitHibClassroomTestCMPUT229
        # Then adds the Github user stuarthoye to that team
        team = org.create_team("test_team")
        team.add_to_members(g.get_user("stuarthoye"))
    except:
        # Access existing team
        # Gets all teams from an org, then iterates over them until test_team
        # Then gets reference to that repo by id.
        teams = org.get_teams()
        for t in teams:
            if t.name == "test_team":
                team = org.get_team(t.id)
    print team
    # for x in g.get_user().get_repos():
    #     print x
    r = g.get_repo("GitHubClassroomTestCMPUT229/testMoss")
    print r

    members = org.get_repos()
    print(members)
main()
