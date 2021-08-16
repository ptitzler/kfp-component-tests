from datetime import datetime
import kfp
import kfp.components as comp
import kfp.dsl as dsl
import requests
import sys

# url = ''
# create_step_download_file = comp.load_component_from_url(url)

create_step = comp.load_component_from_file('0_1_component.yaml')


# Define pipeline
@dsl.pipeline(
    name='no input pipeline',
    description='test no input behavior'
)
def my_pipeline():
    create_step()


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

    run_name = f'no-inputs-run-{datetime.now().strftime("%m%d%H%M%S")}'
    print(f'Creating run {run_name} from pipeline...')
    # Compile, upload, and submit this pipeline for execution.
    run = client.create_run_from_pipeline_func(my_pipeline,
                                               run_name=run_name,
                                               namespace=namespace,
                                               arguments={})
    print(run)
