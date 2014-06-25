#!/usr/bin/env python
import os
import socket
import sys
from optparse import OptionParser
from pulp.bindings.server import PulpConnection 
from pulp.bindings.actions import ActionsAPI
from pulp.bindings.repository import RepositoryDistributorAPI
from Queue import Queue

def get_parser():
    parser = OptionParser()
    parser.add_option("-s", "--source", dest="source",
                        help="Source path")
    parser.add_option("-o", "--out", dest="out_filename", default="rsync_list.txt",
                        help="Output filename")
    parser.add_option("-i", "--repo-ids", dest="repo_ids",
                        help="Comma separated repo ids")
    return parser

def update_seen(path, seen):
    inode = get_inode(path)
    seen.add(inode)
    return seen

def get_inode(path):
    return os.lstat(path).st_ino

def get_inode_of_link_target(link_path):
    target = get_link_target(link_path)
    return os.lstat(target).st_ino

def get_link_target(link_path):    
    target = os.readlink(link_path)
    if not target.startswith('/'):
        # Handle relative symlinks
        dir_path = os.path.abspath(os.path.dirname(link_path))
        target = os.path.join(dir_path, target)
    return target

def read_dir(path):
    seen = set()
    files = []
    links = []
    empty_dirs = []

    for w_root, w_dirs, w_files in os.walk(path, followlinks=False):
        for f in w_files:
            full_path = os.path.join(w_root, f)
            full_path = os.path.abspath(full_path)
            seen = update_seen(full_path, seen)
            if os.path.islink(full_path):
                links.append(full_path)
            else:
                files.append(full_path)
        for d in w_dirs:
            full_path = os.path.join(w_root, d)
            full_path = os.path.abspath(full_path)
            seen = update_seen(full_path, seen)
            if os.path.islink(full_path):
                links.append(full_path)
            if os.listdir(full_path) == []:
                empty_dirs.append(full_path)
    return links, files, empty_dirs, seen

def process_path(path):
    known_links = set()
    known_files = set()
    known_empty_dirs = set()
    seen = set()
    path_queue = Queue()
    path_queue.put(path)

    while not path_queue.empty():
        head = path_queue.get()
        print "%s items on queue, examining: '%s'" % (path_queue.qsize(), head)

        if os.path.islink(head):
            head = os.path.abspath(head)
            known_links.add(head)
            seen = update_seen(head, seen)
            target = get_link_target(head)
            path_queue.put(target)
            continue

        # At this point head is either a file or a dir, it is not a symlink
        inode = get_inode(head)
        if inode in seen:
            # We've already seen this file so skip processing it
            # Prevents traversing a recursive symlink
            continue
        seen = update_seen(head, seen)

        if os.path.isfile(head):
            known_files.add(head)
        else:
            tmp_links, tmp_files, tmp_empty_dirs, tmp_seen = read_dir(head)
            known_files.update(tmp_files)
            known_empty_dirs.update(tmp_empty_dirs)
            seen.update(tmp_seen)

            # Need to determine what links are new so we may process them.
            tmp_links = set(tmp_links)
            unknown_links = tmp_links - known_links
            for l in unknown_links:
                path_queue.put(l)

    return known_links, known_files, known_empty_dirs, seen

def write_output_file(links, files, empty_dirs, out_filename):
    f = open(out_filename, "w")
    for entry in links:
        f.write("%s\n" % (entry))
    f.write("\n")
    for entry in files:
        f.write("%s\n" % (entry))
    f.write("\n") # Empty line to break up output
    for entry in empty_dirs:
        f.write("%s\n" % (entry))
    f.close()
    return

def get_repo_relative_paths(repo_ids, source_path):
    # Since pulp-admin does NOT provide any mean to get specific repo information, 
    # it's easier to access information via. pulp api calls.

    # Initiate pulp server calls
    relative_paths = []
    hostname = socket.gethostname()
    server = PulpConnection(hostname)
    login_api = ActionsAPI(server)
    distributor_api = RepositoryDistributorAPI(server)
    login_api.login("admin", "admin") #TODO: hardcode for now, move as options later
    for id in repo_ids.split(","):
        print "Getting information on repo %s" % id
        distributor_response = distributor_api.distributors(id)
        if distributor_response != None or distributor_response.response_code == 200:
            distributors = distributor_response.response_body
            yum_distributor = [d for d in distributors if d['id'] == 'yum_distributor'][0]
            relative_path = yum_distributor['config']['relative_url']
            relative_paths.append("%s/%s" % (source_path, relative_path))
        else:
            print "Cannot find distributor for repo %s\n" % id
            print "Unable to determine relative path for repo %s\n" % id
           
    return relative_paths

def print_outputs(out_filename, files, empty_dirs, links):
    print "Results written to: %s" % (out_filename)
    print "Found:"
    print "\t %s Files" % (len(files))
    print "\t %s Empty Directories" % (len(empty_dirs))
    print "\t %s Symbolic Links" % (len(links))

if __name__ == "__main__":
    parser = get_parser()
    (opts, args) = parser.parse_args()
    out_filename = opts.out_filename
    source_path = opts.source
    repo_ids = opts.repo_ids
    if source_path == None and repo_ids == None:
        parser.print_help()
        print "Please re-run with a source path or repo ids provided"
        sys.exit(1)
    else:
        if repo_ids == None:
            print "No repo-id specified, processing entire %s directory." % source_path
            links, files, empty_dirs, seen = process_path(source_path)
            write_output_file(links, files, empty_dirs, out_filename)
            print_outputs(out_filename, files, empty_dirs, links)
        else:
            all_links = set()
            all_files = set()
            all_empty_dirs = set()
            all_seen = set()
            for repo_source_path in get_repo_relative_paths(repo_ids, source_path):
                print "Processing repo path %s." % repo_source_path
                links, files, empty_dirs, seen = process_path(repo_source_path)
                # combine links, files, empty_dirs, seen with previous results
                all_links.update(links)
                all_files.update(files)
                all_empty_dirs.update(empty_dirs)
                all_seen.update(seen)
            write_output_file(all_links, all_files, all_empty_dirs, out_filename)
            print_outputs(out_filename, all_files, all_empty_dirs, all_links)
                 

