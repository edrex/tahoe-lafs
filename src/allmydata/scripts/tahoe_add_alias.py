
import os.path
from allmydata import uri
from allmydata.scripts.common_http import do_http, check_http_error
from allmydata.scripts.common import get_aliases

def add_alias(options):
    nodedir = options['node-directory']
    alias = options.alias
    cap = options.cap
    stdout = options.stdout
    stderr = options.stderr
    aliasfile = os.path.join(nodedir, "private", "aliases")
    cap = uri.from_string_dirnode(cap).to_string()
    assert ":" not in alias
    assert " " not in alias
    # probably check for others..
    f = open(aliasfile, "a")
    f.write("%s: %s\n" % (alias, cap))
    f.close()
    print >>stdout, "Alias '%s' added" % (alias,)
    return 0

def create_alias(options):
    # mkdir+add_alias
    nodedir = options['node-directory']
    alias = options.alias
    stdout = options.stdout
    stderr = options.stderr
    aliasfile = os.path.join(nodedir, "private", "aliases")
    assert ":" not in alias
    assert " " not in alias

    nodeurl = options['node-url']
    if not nodeurl.endswith("/"):
        nodeurl += "/"
    url = nodeurl + "uri?t=mkdir"
    resp = do_http("POST", url)
    rc = check_http_error(resp, stderr)
    if rc:
        return rc
    new_uri = resp.read().strip()

    # probably check for others..
    f = open(aliasfile, "a")
    f.write("%s: %s\n" % (alias, new_uri))
    f.close()
    print >>stdout, "Alias '%s' created" % (alias,)
    return 0

def list_aliases(options):
    nodedir = options['node-directory']
    stdout = options.stdout
    stderr = options.stderr
    aliases = get_aliases(nodedir)
    alias_names = sorted(aliases.keys())
    max_width = max([len(name) for name in alias_names] + [0])
    fmt = "%" + str(max_width) + "s: %s"
    for name in alias_names:
        print >>stdout, fmt % (name, aliases[name])

