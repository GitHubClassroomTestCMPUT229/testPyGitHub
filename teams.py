import json
import requests
from requests import Request, Session
from github import Github
from git import Repo

def get_token():
    f = open("git.token", "r")
    token = f.read().strip()
    return token

# class.txt is a text file with student gitIDs on each line
def set_members():
    class_list = open("./class.txt", "r")
    c = [line.strip() for line in c]
    class_list.close()

    token = get_token()
    g = Github(token)
    org = g.get_organization("GitHubClassroomTestCMPUT229")
    for student in c:
        org.add_to_public_members(g.get_user(student))

# Default: Each student in the class is in their own team
# Nondefault:   If students are allowed to form groups, then their groups should
#               be identified in teams.txt
# Should check that students are not member of more than one group.
# class.txt is a text file with student gitIDs on each line
# teams.txt is a text file that identifies which student gitIDs are proposed
# to be group members.  Groups are separated by the term "team:".
# team:
# <member>
# <member>
# team:
# <member>
def set_teams():
    teams = {}
    class_list = open("./class.txt", "r")
    teams_list = open("./teams.txt", "r")

    t = teams_list.readlines()
    c = class_list.readlines()
    t = [line.strip() for line in t]
    c = [line.strip() for line in c]
    i = 0

    class_list.close()
    teams_list.close()

    for line in c:
        line = line.strip()
        if line in t:
            pass    # Skip over students in groups
        else:
            team_name = "team" + str(i)
            teams[team_name] = [line]
            i += 1
    for j in range(len(t)):
        team_name = "team" + str(i)
        team = []
        if t[j] == "team:":
            j += 1
            while t[j] != "team:":
                team.append(t[j])
                j += 1
                if j == len(t):
                    break
            teams[team_name] = team
            i += 1

    out = open("team_defs.json", "w")
    json.dump(teams, out)
    out.close()

def set_repos(lab="testlab1"):
    token = get_token()
    g = Github(token)
    org = g.get_organization("GitHubClassroomTestCMPUT229")
    f = open("team_defs.json", "r")
    teams = json.load(f)
    git_teams = []
    for team in teams:
        t = None
        try:
            t = org.create_team(team)
            git_teams.append(t)
        except:
            print "Error creating team: team {} already exists.".format(team)
        for member in teams[team]:
            t.add_to_members(g.get_user(member))

    base_repo = org.get_repo(lab)
    for team in git_teams:
        fork = org.create_fork(base_repo)
        print fork
        team_repo = org.create_repo(lab+"_"+team.name, team_id=team)
        # for member in teams[team]:
        #     team_repo.add_to_collaborators(g.get_user(member))
    
    
def test_get_repo():
    lab = "1"
    team = "1"
    token = get_token()
    g = Github(token)
    org = g.get_organization("GitHubClassroomTestCMPUT229")
    url = "https://github.com/GitHubClassroomTestCMPUT229/"
    base_code = "testlab1"
    team_name = lab+"_"+team
    base_repo = Repo.clone_from(url+base_code, "./base/")
    team_repo = org.create_repo(team_name)
    remote = base_repo.create_remote(team_repo.name, url+team_name)
    remote.push()
    
    print team_repo.url
    # print base_repo
    # print base_repo.id
    # u = g.get_user()
    # print u
    # fork = u.create_fork(base_repo)
    
    # print fork
    # print fork.id
    # org_repo = org.create_fork(g.get_user("stuarthoye").get_repo("Risk_of_Rain_Save_Editor"))
    # print org_repo
    '''
    # r = requests.get('https://api.github.com', auth=('stuarthoye', 'Cueballs#1'))
    body = {}
    body["vcs"] = "subversion"
    body["vcs_url"] = "http://svn.mycompany.com/svn/myproject"
    body["vcs_username"] = "octocat"
    body["vcs_password"] = "secret"
    s = Session()
    req = Request("POST", "https://api.github.com/repos/stuarthoye/testlab1", data=body)
    req = req.prepare()
    resp = s.send(req)
    # r = requests.put("https://api.github.com/repos/stuarthoye/testlab1"
    print resp.status
    '''
    

def main():
    # set_teams()
    # set_repos()
    test_get_repo()

if __name__ == "__main__":
    main()

