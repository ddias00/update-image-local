import subprocess
import os
from os import environ


def dockerLogin(ECR):
    AWS_DEFAULT_REGION = environ["AWS_DEFAULT_REGION"]
    os.environ["AWS_ACCESS_KEY_ID"] = environ["AWS_ACCESS_KEY_ID_ECR"]
    os.environ ["AWS_SECRET_ACCESS_KEY"] = environ["AWS_SECRET_ACCESS_KEY_ECR"]
    aws_command = f"aws ecr get-login-password --region {AWS_DEFAULT_REGION}"
    docker_command = f"docker login --username AWS --password-stdin {ECR}"

    # Get the ECR login password using the AWS CLI
    process_aws = subprocess.Popen(aws_command, stdout=subprocess.PIPE, shell=True)
    output_aws, error_aws = process_aws.communicate()
    login_password = output_aws.decode("utf-8").strip()

    # Run Docker login command with obtained password
    process_docker = subprocess.Popen(docker_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output_docker, error_docker = process_docker.communicate(input=login_password.encode("utf-8"))

    if process_docker.returncode == 0:
        print("ECR login successful.")
    else:
        print("Error when logging into ECR:")
        print(error_docker.decode("utf-8"))


def dockerLogout():
    docker_command = "docker logout"

    process_docker = subprocess.Popen(docker_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output_docker, error_docker = process_docker.communicate()

    if process_docker.returncode == 0:
        print("Docker logout successful.")
    else:
        print("Error when logging out of Docker:")
        print(error_docker.decode("utf-8"))


def clearImages(image_name_external):
    cls_command = f"docker rmi {image_name_external}"
    process = subprocess.Popen(cls_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        print("An error occurred while running the docker rmi command:")
        print(error.decode("utf-8"))
    else:
        print("Image removed successfully:")
        print(output.decode("utf-8"))


def imageExternalPull(image_name_external):
    command = f"docker pull {image_name_external}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error downloading {image_name_external} image: {error.decode('utf-8')}")
    else:
        print(f"the {image_name_external} image has been successfully downloaded.")


def imageInternalPull(image_name_internal):
    command = f"docker pull {image_name_internal}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error downloading {image_name_internal} image: {error.decode('utf-8')}")
    else:
        print(f"The {image_name_internal} image has been successfully downloaded.")


def dockerTag(image_name_external, image_name_internal):
    docker_tag = f"docker tag {image_name_external} {image_name_internal}"
    process = subprocess.Popen(docker_tag, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output_tag, error_tag = process.communicate()
    if process.returncode != 0:
        print(f"Error creating tag: {error_tag.decode('utf-8')}")
    else:
        print(f"The {image_name_internal} image has been updated.")
        print(output_tag.decode("utf-8"))


def dockerPush(image_name_internal, arquivo_update):
    docker_push = f"docker push {image_name_internal}"
    process = subprocess.Popen(docker_push, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output_push, error_push = process.communicate()
    if process.returncode != 0:
        print(f"Error sending {image_name_internal} image: {error_push.decode('utf-8')}")
    else:
        print(f"The {image_name_internal} image has been updated in the repository.")
        print(f":white_check_mark: {image_name_internal} \\n", file=arquivo_update, end='\n')
        print(output_push.decode("utf-8"))
