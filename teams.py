import json
from github import Github

# Default: Each student in the class is in their own team
# Nondefault:   If students are allowed to form groups, then their groups should
#               be identified in teams.txt
# Should check that students are not member of more than one group.
# class.txt is a text file with student gitIDs on each line
# teams.txt is a text file that identifies which student gitIDs are proposed
# to be group members.  Groups are separated by the term "team:".  Members are indented by a \t.
# team:
#   <member>
#   <member>
# team:
#   <member>
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

    out = open("teams.json", "w")
    json.dump(teams, out)
    out.close()
    print teams

def main():
    set_teams()

if __name__ == "__main__":
    main()
