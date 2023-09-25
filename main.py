#!/usr/bin/env python3
"""
Generate an org file from github issues.
    The `gh` command must be installed on $PATH.
    You must be authenticated.
"""
import argparse, json
import os
import subprocess

try:
    with open(os.path.dirname(__file__)+"/config.json", "r") as inf:
        cfg = json.load(inf)
except:
    cfg = {"me": "e5599f66-5b92-11ee-8c99-0242ac120002"}



def todo_status(state, assignees):
    if state == "OPEN" and cfg["me"] in assignees:
        return "OPEN-ME"
    else:
        return state




def write_issues(issues, args):
    with open(args.org_file, "w+") as org:
        org.write("#+title: GithubIssues\n\n")
        for issue in issues:
            assignees = [_['login'] for _ in issue['assignees']]
            todo = todo_status(issue['state'], assignees)
            org.write(f"* {todo} #{issue['number']}: {issue['title']}"+'\n')
            if todo == "CLOSED":
                org.write(f"    Closed at: {issue['closedAt']}"+'\n')
            org.write("    :PROPERTIES:\n")
            org.write(f"    :author: {issue['author']['login']}"+'\n')
            if len(assignees) > 0:
                org.write(f"    :assignees: {', '.join(assignees)}"+'\n')
            org.write(f"    :createdat: {issue['createdAt']}"+'\n')
            org.write(f"    :url: {issue['url']}"+'\n')
            org.write("    :END:\n\n")
            lines = issue['body'].splitlines()
            for line in lines:
                org.write('    '+line+'\n')
            org.write('\n')
            org.write(f"** Comments ({len(issue['comments'])})"+'\n')
            for comment in issue['comments']:
                org.write(f"*** {comment['author']['login']} said at: {comment['createdAt']}"+'\n\n')
                lines = comment['body'].splitlines()
                for line in lines:
                    org.write('    '+line+'\n')
                org.write('\n')




def main(args):
    tmpf = f"{os.path.dirname(__file__)}/dump.json"
    with open(tmpf, 'w+') as out:
        subprocess.run(['gh', 'issue', 'list',
                        '-L', str(args.number),
                        '-s', args.state,
                        '--json',
                        'assignees,author,body,closed,closedAt,comments,createdAt,id,labels,milestone,number,projectCards,projectItems,reactionGroups,state,title,updatedAt,url'
                        ], stdout=out)

    with open(tmpf, 'r') as inf:
        issues = json.load(inf)

    print(f"{len(issues)} found according to your query")
    write_issues(issues, args)
    os.remove(tmpf)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class = argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-o", "--org-file",
                        type=str, default="issues.org",
                        help="Path/filename of output org file."
    )
    parser.add_argument('-s', '--state',
                        default='open',
                        choices=['open', 'closed', 'all'],
                        help=("What kind of issues you want? (default: open)")
    )
    parser.add_argument("-n", "--number", default=30, help=("Number of issue to fetch."))
    args = parser.parse_args()
    main(args)


