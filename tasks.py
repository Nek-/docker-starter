# from fabric.api import task, env, shell_env
# from fabric.operations import local, _shell_escape, settings
# from functools import wraps
# from fabric.context_managers import quiet
# from fabric.colors import green, yellow
# import os
# import re
# from sys import platform


# @todo voir diff entre local() et run() (les 2 existent dans fabric)
# @todo voir à quoi sert shell_env
# @todo run().stdout, c'est pas super comme façon de préocéder, voir si il existe une façon de retourner directement la sortie
# @todo map with builder

from invoke import task, env, run
# from fabric.operations import local, _shell_escape, settings
from functools import wraps
# from fabric.context_managers import quiet
# from fabric.colors import green, yellow
import os
# import re
from sys import platform

# This will be used to prefix all docker objects (network, images, containers)
env.project_name = 'docker-starter'
# This is the root domain where the app will be available
# The "frontend" container will receive all the traffic
env.root_domain = env.project_name + '.test'
# This contains extra domains where the app will be available
# The "frontend" container will receive all the traffic
env.extra_domains = ['www.docker-starter.test']
# This is the host directory containing your PHP application
env.project_directory = 'application'

services_to_build_first = [
    'php-base',
    'builder',
]


def my_decorator(context, f):
     @wraps(f)
     def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
     return wrapper

@task
@my_decorator
def plop(context):
    print(context)

# def with_builder(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
# #         compose_files = env.compose_files[:]
# #         env.compose_files = ['docker-compose.builder.yml'] + env.compose_files
# #         print(env.compose_files)
# #         print('---------------')
# #         ret = func(*args, **kwargs)
# #         env.compose_files = compose_files
# #
# #         return ret
#             print('Calling decorated function')
#             return func(*args, **kwds)
#     return wrapper


# @with_builder
# def build():
#     """
#     Build the infrastructure
#     """
#     print("build")
#     command = 'build'
#     command += ' --build-arg PROJECT_NAME=%s' % env.project_name
#     command += ' --build-arg USER_ID=%s' % env.user_id
#
#     for service in services_to_build_first:
#         commandForService = '%s %s' % (command, service)
#         docker_compose(commandForService)
#
#     docker_compose(command)

#
# @task
# def up(context):
#     """
#     Build and start the infrastructure
#     """
#     print("coucou")
# #     build()
# #
# #     compose_files = env.compose_files
# #     env.compose_files = [file for file in compose_files if file != 'docker-compose.worker.yml']
# #
# #     docker_compose('up -d')
# #
# #     env.compose_files = compose_files

#
# @task
# def start(context):
#     """
#     Build and start the infrastructure, then install the application (composer, yarn, ...)
#     """
#     if env.dinghy:
#         machine_running = local('dinghy status', capture=True)
#         if machine_running.splitlines()[0].strip() != 'VM: running':
#             run('dinghy up --no-proxy', hide='stdout')
#             run('docker-machine ssh dinghy "echo \'nameserver 8.8.8.8\' | sudo tee -a /etc/resolv.conf && sudo /etc/init.d/docker restart"', hide='stdout')
#
# #     stop_workers(context)
#     up(context)
#     cache_clear(context)
#     install(context)
#     migrate(context)
#     start_workers(context)
#
#     print(green('You can now browse:'))
#     for domain in [env.root_domain] + env.extra_domains:
#         print(yellow("* https://" + domain))
#
#
# @task
# @with_builder
# def install(context):
#     """
#     Install the application (composer, yarn, ...)
#     """
# #     docker_compose_run('composer install -n --prefer-dist --optimize-autoloader')
# #     run_in_docker_or_locally_for_dinghy('yarn')
#
#
# @task
# @with_builder
# def cache_clear(context):
#     """
#     Clear the application cache
#     """
#     docker_compose_run('rm -rf var/cache/ && php bin/console cache:warmup', no_deps=True)
#
#
# @with_builder
# @task
# def migrate(context):
#     """
#     Migrate database schema
#     """
# #     docker_compose_run('php bin/console doctrine:database:create --if-not-exists', no_deps=True)
# #     docker_compose_run('php bin/console doctrine:migration:migrate -n', no_deps=True)
#
#
# @task
# @with_builder
# def builder(context):
#     """
#     Open a shell (bash) into a builder container
#     """
#     docker_compose_run('bash')
#
#
# @task
# def logs(context):
#     """
#     Display infrastructure logs
#     """
#     docker_compose('logs -f --tail=150')
#
#
# @task
# def ps(context):
#     """
#     List containers status
#     """
#     docker_compose('ps')
#
#
# @task
# def stop(context):
#     """
#     Stop the infrastructure
#     """
#     stop_workers()
#     docker_compose('stop')
#
#
# @task
# def start_workers(context):
#     """
#     Start the workers
#     """
#     docker_compose('up -d --no-deps')
#
#
# @with_builder
# @task
# def stop_workers(context):
#     """
#     Stop the workers
#     """
# #     with quiet():
#     run('docker update --restart=no $(docker ps -a --filter "Name=%s_worker" --quiet)' % (env.project_name), hide='stdout')
#     if os.path.exists(env.root_dir + "/" + env.project_directory + "/vendor/symfony/messenger"):
#         docker_compose_run('bin/console messenger:stop-workers')
#
#
# @task
# @with_builder
# def destroy(context):
#     """
#     Clean the infrastructure (remove container, volume, networks)
#     """
#     docker_compose('down --volumes --rmi=local')
#
#
# def run_in_docker_or_locally_for_dinghy(command):
#     """
#     Mac users have a lot of problems running Yarn / Webpack on the Docker stack so this func allow them to run these tools on their host
#     """
#     if env.dinghy:
#         run('cd %s && %s' % (env.project_directory, command), hide='stdout')
#     else:
#         docker_compose_run(command)
#
#
# def docker_compose(command_name):
#
#     domains = '`' + '`, `'.join([env.root_domain] + env.extra_domains) + '`'
#
#     localEnv = {
#         'PROJECT_NAME': env.project_name,
#         'PROJECT_DIRECTORY': env.project_directory,
#         'PROJECT_ROOT_DOMAIN': env.root_domain,
#         'PROJECT_DOMAINS': domains,
#     }
#
# #     with shell_env(**localEnv):
# #         local('docker-compose -p %s %s %s' % (
# #             env.project_name,
# #             ' '.join('-f \'' + env.root_dir + '/infrastructure/docker/' + file + '\'' for file in env.compose_files),
# #             command_name
# #         ))
#     run('docker-compose -p %s %s %s' % (
#         env.project_name,
#         ' '.join('-f \'' + env.root_dir + '/infrastructure/docker/' + file + '\'' for file in env.compose_files),
#         command_name
#     ), env=localEnv, hide='stdout')
#
#
# def docker_compose_run(command_name, service="builder", user="app", no_deps=False, workdir=None, port_mapping=False):
#     args = [
#         'run ',
#         '--rm ',
#         '-u %s ' % _shell_escape(user),
#     ]
#
#     if no_deps:
#         args.append('--no-deps ')
#
#     if port_mapping:
#         args.append('--service-ports ')
#
#     if workdir is not None:
#         args.append('-w %s ' % _shell_escape(workdir))
#
#     docker_compose('%s %s /bin/bash -c "exec %s"' % (
#         ' '.join(args),
#         _shell_escape(service),
#         _shell_escape(command_name)
#     ))
#
#
# def set_local_configuration():
#     env.compose_files = ['docker-compose.yml', 'docker-compose.worker.yml']
#     env.dinghy = False
#     env.power_shell = False
#     env.user_id = 1000
#
# #     with quiet():
#     try:
#         #docker_kernel = "%s" % local('docker version --format "{{.Server.KernelVersion}}"', capture=True)
#         docker_kernel = "%s" % run('docker version --format "{{.Server.KernelVersion}}"', hide='stdout').stdout
#     except:
#         docker_kernel = ''
#
#     if platform == "darwin" and docker_kernel.find('linuxkit') != -1:
#         env.dinghy = True
#     elif platform in ["win32", "win64"]:
#         env.power_shell = True
#         # Python can't set the vars correctly on PowerShell and local() always calls cmd.exe
#         # shellProjectName = run('echo %PROJECT_NAME%', capture=True)
#         shellProjectName = run('echo %PROJECT_NAME%', hide='stdout').stdout
#         if (shellProjectName != env.project_name):
#             domains = '`' + '`, `'.join([env.root_domain] + env.extra_domains) + '`'
#             print('You must manually set environment variables on Windows:')
#             print('$Env:PROJECT_NAME="%s"' % env.project_name)
#             print('$Env:PROJECT_DIRECTORY="%s"' % env.project_directory)
#             print('$Env:PROJECT_HOSTNAMES="%s"' % env.project_hostnames)
#             print('$Env:PROJECT_DOMAINS="%s"' % domains)
#             raise SystemError('Env vars not set (Windows detected)')
#
#     if not env.power_shell:
#         # env.user_id = int(run('id -u', capture=True, pty=True))
#         env.user_id = int(run('id -u', hide='stdout').stdout)
#
#     if env.user_id > 256000:
#         env.user_id = 1000
#
#     env.root_dir = os.path.dirname(os.path.abspath(__file__))
#
# set_local_configuration()
#
#
# # --------- Not sure
#
# def _shell_escape(string):
#     """
#     Escape double quotes, backticks and dollar signs in given ``string``.
#
#     For example::
#
#         >>> _shell_escape('abc$')
#         'abc\\\\$'
#         >>> _shell_escape('"')
#         '\\\\"'
#     """
#     for char in ('"', '$', '`'):
#         string = string.replace(char, '\%s' % char)
#     return string
#
# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'
#
# def green(string):
#     return bcolors.OKGREEN + string + bcolors.ENDC
#
# def yellow(string):
#     return bcolors.WARNING + string + bcolors.ENDC
