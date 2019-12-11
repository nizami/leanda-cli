import subprocess
import string
import random
from behave import given, when, then


def get_random_string(minch=5, maxch=10):
    strset = string.ascii_uppercase + string.digits
    return ''.join( random.choice(strset) for _ in range(random.randrange(minch, maxch)))



@given(u'I am a valid user')
def step_impl(context):
    pass


@given(u'I want to login')
def step_impl(context):
    context.branch = "login"
    context.command = "{path} {branch}".format(path=context.path, branch=context.branch)

    command = "{command} -u{username} -p{password}"
    context.command = command.format(username=context.username, 
                                     password=context.password,
                                     command=context.command)

    context.expect = 'successfully'
    print(context.command)


@then(u'I run command')
def step_impl(context):
    try:
        result = subprocess.check_output(context.command.split(), stderr=subprocess.STDOUT,)
    except subprocess.CalledProcessError as e:
        result = e.output
    context.result = str(result)
    print(context.result)


@then(u'get successfull message')
def step_impl(context):
    assert context.result.index(context.expect)


@then(u'get my username')
def step_impl(context):
    user = '"{}"'.format(context.username) 
    assert context.result.index(user)


@given(u'I am an invalid user')
def step_impl(context):
    context.username = get_random_string()
    context.password = get_random_string()
    context.error = 'Authorization Error'



@then(u'I get an error message')
def step_impl(context):
    print(context.error)
    assert context.result.index(context.error)


@when(u'I want to logout')
def step_impl(context):
    context.branch = "logout"
    context.command = "{path} {branch}".format(path=context.path, branch=context.branch)
    context.expect = 'Success'

@given(u'I want to identify myself')
def step_impl(context):
    context.branch = "whoami"
    context.command = "{path} {branch}".format(path=context.path, branch=context.branch)
    context.error = 'No such file'


@then(u'get asked info')
def step_impl(context):
    assert context.result.index(context.expect)

@given(u'ask {extra} info')
def step_impl(context, extra):
    verbosities = { 
        'login':{
            'more': ('-v', 'username'),
            'much more': ('-vv', 'working directory'),  
            'all': ('-vvv', 'Token: Bearer'),     
            'none': ('','')
        },
        'whoami':{
            'more': ('-v', 'Leanda user'),
            'all': ('-vv', 'user id'),     
            'none': ('',' ')
        },
    }
    verbosities=verbosities[context.branch]

    verbosity, expect = verbosities[extra]
    context.command += " {}".format(verbosity)
    context.expect = expect

