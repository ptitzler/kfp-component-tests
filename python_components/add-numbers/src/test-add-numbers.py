import sys
from datetime import datetime

import kfp
import kfp.dsl as dsl
from kfp.components import create_component_from_func

import requests


# (1) import the user-defined Python function from
#     add_numbers.py
# ignore linting; separated from other imports for clarity
from add_numbers import add # noqa I100

# (2) create factory for imported function from user-provided input:
#   - container/base image (optional)
#   - packages to install (optional)
# Perhaps use generated output_component_file to avoid the need for source code parsing?
# https://kubeflow-pipelines.readthedocs.io/en/latest/source/kfp.components.html#kfp.components.create_component_from_func
add_op = create_component_from_func(
    func=add,
    base_image=None,
    packages_to_install=['pandas==1.3.0'],
    output_component_file='add_component.yaml')


#
# create pipeline
#
@dsl.pipeline(
    name='Addition pipeline',
    description='An example pipeline that performs addition calculations.'
)
def add_pipeline(a='1', b='1'):
    # Passes a pipeline parameter and a constant value to the `add_op` factory
    # function.
    first_add_task = add_op(a, 4)
    # Passes an output reference from `first_add_task` and a pipeline parameter
    # to the `add_op` factory function. For operations with a single return
    # value, the output reference can be accessed as `task.output` or
    # `task.outputs['output_name']`.
    second_add_task = add_op(first_add_task.output, b) # noqa F841


#
# housekeeping
#
def get_user_auth_session_cookie(url, username=None, password=None) -> dict:

    # Return data structure
    auth_info = {
        'endpoint': url,                    # KF endpoint URL
        'endpoint_response_url': None,      # KF redirect URL, if applicable
        'endpoint_secured': False,          # True if KF is secured [by dex]
        'authservice_session_cookie': None  # Set if KF secured & user auth'd
    }

    # Obtain redirect URL
    get_response = requests.get(url)

    auth_info['endpoint_response_url'] = get_response.url

    # If KF redirected to '/dex/auth/local?req=REQ_VALUE'
    # try to authenticate using the provided credentials
    if 'dex/auth' in get_response.url:
        auth_info['endpoint_secured'] = True  # KF is secured

        # Try to authenticate user by sending a request to the
        # Dex redirect URL
        session = requests.Session()
        session.post(get_response.url,
                     data={'login': username,
                           'password': password})
        # Capture authservice_session cookie, if one was returned
        # in the response
        cookie_auth_key = 'authservice_session'
        cookie_auth_value = session.cookies.get(cookie_auth_key)

        if cookie_auth_value:
            auth_info['authservice_session_cookie'] = \
                f"{cookie_auth_key}={cookie_auth_value}"

    return auth_info


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f'Invocation {sys.argv[0]} <KFP-API-URL> [<namespace>] [<kf-uid> <kf-password>]')
        sys.exit(1)

    print('Trying to authenticate with Kubeflow server ...')

    auth_endpoint = sys.argv[1].rstrip('/').replace('/pipeline', '')

    namespace = None
    id = None
    password = None
    if len(sys.argv) == 2:
        namespace = sys.argv[2]
    elif len(sys.argv) == 4:
        namespace = None
        id = sys.argv[2]
        password = sys.argv[3]
    elif len(sys.argv) == 5:
        namespace = sys.argv[2]
        id = sys.argv[3]
        password = sys.argv[4]

    # authenticate
    auth_info = get_user_auth_session_cookie(auth_endpoint,
                                             id,
                                             password)

    if auth_info['endpoint_secured'] and \
       auth_info['authservice_session_cookie'] is None:
        print('Authentication failed. Check your credentials.')
        sys.exit(1)

    auth_cookie = auth_info['authservice_session_cookie']

    client = kfp.Client(host=sys.argv[1],
                        cookies=auth_cookie)

    run_name = f'download-file-python-func-run-{datetime.now().strftime("%m%d%H%M%S")}'
    print(f'Creating run {run_name} from pipeline...')

    # Specify argument values for your pipeline run.
    arguments = {'a': '7', 'b': '8'}

    # Compile, upload, and submit this pipeline for execution.
    run = client.create_run_from_pipeline_func(add_pipeline,
                                               run_name=run_name,
                                               namespace=namespace,
                                               arguments=arguments)
    print(run)
