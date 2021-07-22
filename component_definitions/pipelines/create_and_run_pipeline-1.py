from datetime import datetime
import kfp
import kfp.components as comp
import kfp.dsl as dsl
import requests
import sys

create_step_load_file = comp.load_component_from_file('../download-file/component.yaml')
create_step_get_lines = comp.load_component_from_file('../truncate-file/component.yaml')
create_step_count_lines = comp.load_component_from_file('../count-lines/component.yaml')


# Define pipeline
@dsl.pipeline(
    name='Component examples example pipeline',
    description='Runs download-file, truncate-file, and count-lines'
)
def a_three_step_pipeline():
    download_file = create_step_load_file(
        url='https://raw.githubusercontent.com/ptitzler/kfp-component-tests/main/LICENSE'
    )
    get_lines = create_step_get_lines(
        input_1=download_file.outputs['file'],
        parameter_1='5'
    )
    create_step_count_lines(
        input_1=get_lines.outputs['output_1']
    )


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

    print('Compiling pipeline...')

    pipeline_name = 'a_three_step_pipeline'
    pipeline_archive = f'{pipeline_name}.tgz'
    timestamp = datetime.now().strftime("%m%d%H%M%S")

    # Compile
    kfp.compiler.Compiler().compile(a_three_step_pipeline,
                                    pipeline_archive)

    pipeline_id = client.get_pipeline_id(pipeline_name)
    if pipeline_id is None:
        # Upload new pipeline. The call returns a unique pipeline id.
        print(f'Uploading pipeline {pipeline_name} ...')
        kfp_pipeline = \
            client.upload_pipeline(pipeline_archive,
                                   pipeline_name,
                                   f'Created using {sys.argv[0]}')
        pipeline_id = kfp_pipeline.id
        version_id = None
    else:
        # Append timestamp to generate unique version name
        pipeline_version_name = f'{pipeline_name}-{timestamp}'
        # Upload a pipeline version. The call returns a unique version id.
        print(f'Uploading pipeline version {pipeline_version_name} ...')
        kfp_pipeline = \
            client.upload_pipeline_version(pipeline_archive,
                                           pipeline_version_name,
                                           pipeline_id=pipeline_id)
        version_id = kfp_pipeline.id

    experiment_name = f'{pipeline_name}-experiment'
    print(f'Creating expriment {experiment_name} in namespace {namespace} ...')
    experiment = client.create_experiment(experiment_name,
                                          namespace=namespace)

    run_name = f'{pipeline_name}-{timestamp}'
    print(f'Starting pipeline run {run_name} ...')
    run = client.run_pipeline(experiment_id=experiment.id,
                              job_name=run_name,
                              pipeline_id=pipeline_id,
                              version_id=version_id)
    print(f'Pipeline run id: {run.id}')
