# -*- encoding: utf-8 -*-
import argparse
import os
import shutil
import json
import time
import stat
import platform
try:
    from urllib.parse import parse_qs, urlparse, urlunparse
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import parse_qs, urlparse, urlunparse
    from urllib2 import urlopen, Request, HTTPError


def parse_options():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="action")

    add_parser = subparsers.add_parser("add", help="add repo web hook")
    exec_parser = subparsers.add_parser("run", help="exec web hook")

    for subparser in (add_parser, exec_parser):
        subparser.add_argument(
            "--webhook_url", help="Web Hook Url.", required=True
        )
        subparser.add_argument(
            "--secret_key", help="Secret key", required=True
        )
        subparser.add_argument(
            "--link_url", help="Link dir.", required=False
        )

    add_parser.add_argument(
        "--repo_dir", help="Repo dir.", required=True
    )

    exec_parser.add_argument(
        "--repo", help="Repo name", required=True
    )

    exec_parser.add_argument(
        "--rev", help="Commit rev.", required=True
    )

    return parser.parse_args()

def add(options):
    post_commit_dir = options.repo_dir + "/hooks/post-commit"
    if not os.path.exists(post_commit_dir):
        mymovefile(post_commit_dir+".tmpl", post_commit_dir)
    os.chmod(post_commit_dir, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    write(options, post_commit_dir)
    print("Web hook add success")

def add_windows(options):
    post_commit_dir = options.repo_dir + "/hooks/post-commit.bat"
    write_windows(options, post_commit_dir)
    print("Web hook add success")

def write(options, post_commit_dir):
    lines = ""
    if os.path.exists(post_commit_dir):
        lines = [l for l in open(post_commit_dir, 'r') if "webhook.py" not in l and "export LANG=zh_CN.UTF-8" not in l ]
    f = open(post_commit_dir, 'w')
    f.writelines(lines)
    f.write("\nexport LANG=zh_CN.UTF-8 \n")
    f.write("python " + os.getcwd() + "/webhook.py" + " run --repo $1 --rev $2  --webhook_url " + options.webhook_url + " --secret_key " + options.secret_key)
    if options.link_url is not None:
        f.write(" --link_url " + options.link_url + '\n')
    else:
        f.write('\n')

    f.close()


def write_windows(options, post_commit_dir):
    lines = ""
    if os.path.exists(post_commit_dir):
        lines = [l for l in open(post_commit_dir, 'r') if "webhook.py" not in l and "CHCP 65001" not in l]
    f = open(post_commit_dir, 'w')
    f.writelines(lines)
    f.write("\npython " + os.getcwd() + "/webhook.py" + " run --repo %1 --rev %2  --webhook_url " + options.webhook_url + " --secret_key " + options.secret_key)
    if options.link_url is not None:
        f.write(" --link_url " + options.link_url + '\n')
    f.close()

def mymovefile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname = os.path.split(dstfile)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copy(srcfile, dstfile)
        print ("copy %s -> %s"%(srcfile, dstfile))



def run(options):
    print("Weh hook run")
    call_ones_api(options)


def call_ones_api(options):
    repo_name = get_repo_name(options.repo)
    log = get_log(options.repo, options.rev)
    author = get_author(options.repo, options.rev)
    date = get_date(options.repo, options.rev)
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    temp_svn_diff = "temp_svn_diff." + now_time
    stats = get_stats(options.repo, options.rev, temp_svn_diff)

    link_url = options.link_url
    if link_url is not None:
        link_url = link_url.replace("{commit_id}",str(options.rev))
        link_url = link_url.replace("{repo}", repo_name)

    if platform.system() == 'Windows':
        try:
            log = log.decode("gbk")
            author = author.decode("gbk")
        except UnicodeError:
            pass

    payload = json.dumps({
        "repository": repo_name,
        "author": author,
        "timestamp": int(time.mktime(time.strptime(date.split("(", 1)[0].strip(), "%Y-%m-%d %H:%M:%S +0800"))),
        "message": log,
        "revision": options.rev,
        "stats_total": stats['total'],
        "stats_additions": stats['additions'],
        "stats_deletions": stats['deletions'],
        "url": link_url
    })

    headers = {
        "Accept": "application/json",
        "Content-type": "application/json;charset=UTF-8",
        "X-ONES-SVN": options.secret_key
    }

    parts = urlparse(options.webhook_url)
    url = urlunparse((parts.scheme, parts.netloc, parts.path, '', '', ''))
    req = Request(url, payload, headers)
    urlopen(req)

def get_repo_name(repo):
    return os.path.basename(repo)

def get_author(repo, rev):
    cmd = '%s author -r %s %s' % (svnlook_bin_path, rev, repo)
    output = os.popen(cmd).read()
    return output

def get_date(repo, rev):
    cmd = '%s date -r %s %s' % (svnlook_bin_path, rev, repo)
    output = os.popen(cmd).read()
    return output

def get_log(repo, rev):
    cmd = '%s log -r %s %s' % (svnlook_bin_path, rev, repo)
    output = os.popen(cmd).read()
    return output


def get_file_list(repo, rev):
    cmd = '%s changed -r %s %s' % (svnlook_bin_path, rev, repo)
    output = os.popen(cmd).read()
    return output

def get_stats(repo, rev, temp_svn_diff):
    temp_svn_diff = repo + "/" + temp_svn_diff
    cmd = '%s diff -r %s %s >%s' % (svnlook_bin_path, rev, repo, temp_svn_diff)
    os.popen(cmd).read()

    addLineNum = 0
    delLineNum = 0

    if len(open(temp_svn_diff, 'r').read()) == 0:
        print ("no change")
    else:
        with open(temp_svn_diff, 'r') as svndiff:
            for line in svndiff:
                if line.startswith('+'):
                    addLineNum += 1
                if line.startswith('+++'):
                    addLineNum -= 1
                if line.startswith('-'):
                    delLineNum += 1
                if line.startswith('---'):
                    delLineNum -= 1

    os.remove(temp_svn_diff)
    return {
        "additions": addLineNum,
        "deletions": delLineNum,
        "total": addLineNum + delLineNum
    }

global svnlook_bin_path

if __name__ == "__main__":
    svnlook_bin_path = 'svnlook'
    options = parse_options()
    if options.action == "add":
        webhookFile = os.getcwd() + "/webhook.py"
        if not os.path.isfile(webhookFile):
            print ("%s not exist!"%(webhookFile))
        else:
            if platform.system() == 'Windows':
                add_windows(options)
            else:
                add(options)

    elif options.action == "run":
        run(options)
