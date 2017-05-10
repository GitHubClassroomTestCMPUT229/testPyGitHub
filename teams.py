import json
import requests
import shutil
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

def set_git_teams():
    token = get_token()
    g = Github(token)
    org = g.get_organization("GitHubClassroomTestCMPUT229")
    f = open("team_defs.json", "r")
    teams = json.load(f)
    f.close()

    git_teams = []
    for team in teams.keys():
        t = None
        try:
            t = org.create_team(team)
            git_teams.append(t)
        except:
            print "Error creating team: team {} already exists.".format(team)
        for member in teams[team]:
            t.add_to_members(g.get_user(member))
    

def set_repos(lab="testlab1"):
    f = open("team_defs.json", "r")
    teams = json.load(f)
    f.close()

    token = get_token()
    g = Github(token)
    org = g.get_organization("GitHubClassroomTestCMPUT229")
    
    data = {}
    for team in teams:
        info = clone(lab, team) 
        data[team] = info
    f = open("teams.json", "w")
    json.dump(data, f)
    f.close()

def clone(lab, team):
    token = get_token()
    g = Github(token)
    org = g.get_organization("GitHubClassroomTestCMPUT229")
    url = "https://"+token+":x-oauth-basic@github.com/GitHubClassroomTestCMPUT229/"
    base_code = "testlab1"
    team_name = lab+"_"+team
    base_repo = Repo.clone_from(url+base_code, "./base/")
    team_repo = org.create_repo(team_name)
    remote = base_repo.create_remote(team_repo.name, url+team_name)
    remote.push()
    shutil.rmtree("./base/")
    return {lab: url+team_name}

def local_clone(lab):
    token = get_token()
    url = "https://"+token+":x-oauth-basic@github.com/GitHubClassroomTestCMPUT229/"+lab
    base_repo = Repo.clone_from(url, "./base/")
    return base_repo

# Oauth tokens in gitpython    
# http://stackoverflow.com/questions/36358808/cloning-a-private-repo-using-https-with-gitpython
# User: shawnzhu
def test_get_repo():
    lab = "1"
    team = "1"
    token = get_token()
    g = Github(token)
    org = g.get_organization("GitHubClassroomTestCMPUT229")
    url = "https://"+token+":x-oauth-basic@github.com/GitHubClassroomTestCMPUT229/"
    base_code = "testlab1"
    team_name = lab+"_"+team
    base_repo = Repo.clone_from(url+base_code, "./base/")
    team_repo = org.create_repo(team_name)
    remote = base_repo.create_remote(team_repo.name, url+team_name)
    remote.push()
    shutil.rmtree("./base/")
    
    

def main():
    set_teams()
    set_git_teams()
    set_repos()
    #test_get_repo()

if __name__ == "__main__":
    main()

