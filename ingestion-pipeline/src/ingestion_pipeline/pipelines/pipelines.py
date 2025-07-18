from kfp import dsl
from typing import Optional

from . import tasks


def s3_pipeline(pipeline_name: str, llamastack_base_url: str, auth_user: str):
    @dsl.pipeline(name="fetch-and-store-pipeline")
    def _pipeline():
        from kfp import kubernetes

        secret_key_to_env = {
                'SOURCE': 'SOURCE',
                'EMBEDDING_MODEL': 'EMBEDDING_MODEL',
                'VECTOR_DB_NAME': 'VECTOR_DB_NAME',
                'ACCESS_KEY_ID': 'ACCESS_KEY_ID',
                'SECRET_ACCESS_KEY': 'SECRET_ACCESS_KEY',
                'ENDPOINT_URL': 'ENDPOINT_URL',
                'BUCKET_NAME': 'BUCKET_NAME',
                'REGION': 'REGION'
        }

        fetch_task = tasks.fetch_from_s3()
        fetch_task.set_caching_options(False)

        store_task = tasks.store_documents(
            llamastack_base_url=llamastack_base_url,
            input_dir=fetch_task.outputs["output_dir"],
            auth_user=auth_user
        )
        store_task.set_caching_options(False)

        for task in (fetch_task, store_task):
            kubernetes.use_secret_as_env(
                task=task,
                secret_name=pipeline_name,
                secret_key_to_env=secret_key_to_env
            )
    return _pipeline


def url_pipeline(pipeline_name: str, llamastack_base_url: str, auth_user: str):
    @dsl.pipeline(name="fetch-and-store-pipeline")
    def _pipeline():
        from kfp import kubernetes

        secret_key_to_env = {
            'SOURCE': 'SOURCE',
            'EMBEDDING_MODEL': 'EMBEDDING_MODEL',
            'VECTOR_DB_NAME': 'VECTOR_DB_NAME',
            'URLS': 'URLS'
        }

        fetch_task = tasks.fetch_from_urls()
        fetch_task.set_caching_options(False)

        store_task = tasks.store_documents(
            llamastack_base_url=llamastack_base_url,
            input_dir=fetch_task.outputs["output_dir"],
            auth_user=auth_user
        )
        store_task.set_caching_options(False)

        kubernetes.use_secret_as_env(
            task=store_task,
            secret_name=pipeline_name,
            secret_key_to_env=secret_key_to_env
        )
    return _pipeline


def github_pipeline(pipeline_name: str, llamastack_base_url: str, auth_user: str):
    @dsl.pipeline(name="fetch-and-store-pipeline")
    def _pipeline():
        from kfp import kubernetes

        secret_key_to_env = {
            'SOURCE': 'SOURCE',
            'EMBEDDING_MODEL': 'EMBEDDING_MODEL',
            'VECTOR_DB_NAME': 'VECTOR_DB_NAME',
            'URL': 'GIT_URL',
            'PATH': 'GIT_PATH',
            'TOKEN': 'GIT_TOKEN',
            'BRANCH': 'GIT_BRANCH'
        }

        fetch_task = tasks.fetch_from_github()
        fetch_task.set_caching_options(False)

        store_task = tasks.store_documents(
            llamastack_base_url=llamastack_base_url,
            input_dir=fetch_task.outputs["output_dir"],
            auth_user=auth_user
        )
        store_task.set_caching_options(False)

        for task in (fetch_task, store_task):
            kubernetes.use_secret_as_env(
                task=task,
                secret_name=pipeline_name,
                secret_key_to_env=secret_key_to_env
            )
    return _pipeline
