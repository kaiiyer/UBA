#!/usr/bin/env python2

import os
import shutil
import subprocess

import termcolor

import config


# Directory where the script lives
INSTALL_FOLDER = os.path.dirname(os.path.realpath(__file__))
# Expand evironment variables and metacharacters in the log folder path
config.AUDIT_FOLDER = os.path.expanduser(os.path.expandvars(config.AUDIT_FOLDER))


def log_info(logstr):
    print termcolor.colored('[+] ' + logstr, 'green')


def log_warning(logstr):
    print termcolor.colored('[!] ' + logstr, 'yellow')


def log_error(logstr):
    print termcolor.colored('[X] ' + logstr, 'red')


def get_xdisplay():
    if "DISPLAY" in os.environ:
        display = os.environ['DISPLAY']
    else:
        log_warning("Cannot get X display, defaulting to :0")
        display = ":0"
    return display


def get_crontab():
    try:
        crontab = subprocess.check_output(['bash', '-c', 'crontab -l 2>/dev/null'])
    except subprocess.CalledProcessError as e:
        return ""
    return crontab.strip()


def cronjob_exists(command):
    crontab = get_crontab()
    if command in crontab:
        return True
    else:
        return False


def delete_cronjob(command):
    if not cronjob_exists(command):
        log_warning('Trying to remove unexisting cronjob "%s"' % command)
        return
    crontab = get_crontab()
    new_crontab = ""
    for cronjob in crontab.split('\n'):
        if command not in cronjob: 
            new_crontab += cronjob + "\n"
    p1 = subprocess.Popen("crontab", stdin=subprocess.PIPE)
    p1.communicate(new_crontab)


def create_cronjob(command, interval):
    if cronjob_exists(command):
        log_warning('Trying to add already existing cronjob "%s"' % command)
        return
    cronjob = '*/%s * * * * %s' % (interval, command)
    crontab = get_crontab()
    new_crontab = crontab + "\n" + cronjob + "\n"
    p1 = subprocess.Popen("crontab", stdin=subprocess.PIPE)
    p1.communicate(new_crontab)


def get_fullpath(audit_name, raiseerror=True):
    fullpath = os.path.join(config.AUDIT_FOLDER, audit_name)
    if not os.path.exists(fullpath) and raiseerror:
        raise Exception("Audit folder does not exist : %s" % fullpath)
    return fullpath


def get_rcfile():
    rc_file = os.path.join(os.environ['HOME'], '.bashrc')
    return rc_file


def get_screenshot_command(audit_name):
    return "DISPLAY=" + get_xdisplay() + " " + os.path.join(INSTALL_FOLDER, 'scripts', 'screenshot.py') + " " + os.path.join(get_fullpath(audit_name), 'logs', 'screenshots')


def get_git_command(audit_name):
    return os.path.join(INSTALL_FOLDER, 'scripts', 'git_autocommit.sh') + " " + os.path.join(get_fullpath(audit_name))


def get_source_command(audit_name):
    return 'source ' + os.path.join(get_fullpath(audit_name),'.audit', 'auditrc')


def add_line_to_script(script_file, cmd):
    with open(script_file, 'r') as fd1:
        if cmd not in fd1.read():
            with open(script_file, 'a') as fd2:
                fd2.write('\n' + cmd + '\n')
        else:
            log_warning('%s already contains "%s"' % (script_file, cmd))


def remove_line_from_script(script_file, cmd):
    new_file = ""
    with open(script_file, 'r') as fd:
        for line in fd.readlines():
            if line.strip() != cmd:
                new_file += line
    with open(script_file, 'w') as fd:
        fd.write(new_file.strip() + "\n")


def list_audits():
    # Check main directory
    if not os.path.exists(config.AUDIT_FOLDER):
        raise Exception("Main folder %s does not exist." % config.AUDIT_FOLDER)
    for file in os.listdir(config.AUDIT_FOLDER):
        if os.path.exists(os.path.join(config.AUDIT_FOLDER, file, '.audit')):
            log_info(file)


def init(audit_name):
    # Check main directory
    if not os.path.exists(config.AUDIT_FOLDER):
        raise Exception("Main folder %s does not exist." % config.AUDIT_FOLDER)
    
    # Create folder structure
    fullpath = get_fullpath(audit_name, raiseerror=False)
    shutil.copytree(os.path.join(INSTALL_FOLDER, 'skel'), fullpath)

    # Create git repository
    if config.GIT_AUTOCOMMIT:
        subprocess.check_output([os.path.join(INSTALL_FOLDER, 'scripts', 'git_init.sh'), get_fullpath(audit_name)])

    log_info(termcolor.colored('Created audit project in %s' % get_fullpath(audit_name), 'green'))


def start(audit_name):
    # Source auditrc in every shell
    add_line_to_script(get_rcfile(), get_source_command(audit_name))

    # Create cron jobs
    if config.SCREENSHOTS:
        create_cronjob(get_screenshot_command(audit_name), config.SCREENSHOT_INTERVAL)
    if config.GIT_AUTOCOMMIT:
        create_cronjob(get_git_command(audit_name), config.GIT_AUTOCOMMIT_INTERVAL)
    log_warning('Already opened shells will not be logged')
    os.system('exec ' + os.environ['SHELL'])


def stop(audit_name):
    # Stop auditrc sourcing
    remove_line_from_script(get_rcfile(), get_source_command(audit_name))

    # Delete cron jobs
    delete_cronjob(get_screenshot_command(audit_name))
    delete_cronjob(get_git_command(audit_name))

    log_info("Audit stopped. Make sure to exit all logged shells.")


def export_shell_log(audit_name):
    all_shell_logs = ""
    shell_logs = os.path.join(get_fullpath(audit_name), 'logs', 'shell')
    
    # cleanup input commands
    for file in os.listdir(shell_logs):
        if file.endswith("shell.log"):
             with open(os.path.join(shell_logs, file), 'r') as f:
                 logfile = f.readlines()
                 newlogfile = "".join(logfile)
             histfile = os.path.join(shell_logs, file + ".hist")
             with open(os.path.join(shell_logs, histfile), 'r') as f:
                 for line in f.readlines():
                     histnumber = [s for s in line.split() if s.isdigit()][0]
                     cmd = line.replace(histnumber,'',1).strip()
                     previous_line =''
                     for line in logfile:
                         if '['+histnumber+']' in line:
                             if '$' in line:
                                 new_prompt = line.split('$')[0] + '$ ' + cmd + "\n"
                             if '#' in line:
                                 new_prompt = line.split('#')[0] + '# ' + cmd + "\n"
                             newlogfile = newlogfile.replace(previous_line, previous_line.strip())
                             newlogfile = newlogfile.replace(line, new_prompt)
                         previous_line = line
             with open(os.path.join(shell_logs, file+".processed"), 'w') as f:
                    f.write(newlogfile)
    
    # concatenate each script
    for file in sorted(os.listdir(shell_logs)):
        if file.endswith("shell.log.processed"):
            with open(os.path.join(shell_logs, file), 'r') as f:
                all_shell_logs += '\n' + '='*100 + '\n' + file + '\n' + '='*100 + '\n' + f.read()
    
    # convert to HTML
    temp_file = "/tmp/allshells.log"
    with open(temp_file, 'w') as f:
        f.write(all_shell_logs)
    dest_file = os.path.join(get_fullpath(audit_name), "shell_log.html")
    converter = os.path.join(INSTALL_FOLDER, 'scripts', 'scripttohtml.py')
    log_info("Exporting to " + dest_file)
    subprocess.Popen([converter, temp_file, dest_file]).wait()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description='audit.py - engagement logging.')
    parser.add_argument('action', help='init|start|stop|export|config')
    parser.add_argument('audit_name', nargs='?', help='Audit name')
    args = parser.parse_args()
    
    if args.action not in ['init', 'start', 'stop', 'export', 'config', 'list']:
        log_error('Wrong arguments.')
        parser.print_help()
        exit(1)

    if args.action in ['init', 'start', 'stop', 'export'] and not args.audit_name:
        log_error('Specify an audit name')
        exit(1)

    if args.audit_name:
        args.audit_name = os.path.basename(args.audit_name)

    try:
        if args.action == 'init':
            init(args.audit_name)
        elif args.action == 'start':
            start(args.audit_name)
        elif args.action == 'stop':
            stop(args.audit_name)
        elif args.action == 'export':
            export_shell_log(args.audit_name)
        elif args.action == 'config':
            os.system('${EDITOR:-vi} %s' % os.path.join(INSTALL_FOLDER, 'config.py'))
        elif args.action == 'list':
            list_audits()

    except Exception as exc:
        log_error(str(exc))
