import subprocess


def getInternalDigest(image_name_internal):
    aws_command = f"docker inspect --format='{{{{index .RepoDigests 0}}}}' {image_name_internal} | cut -d':' -f2"
    process = subprocess.Popen(aws_command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print("An error occurred when running the docker inspect command for internal image:")
        print(error.decode("utf-8"))
        return None

    hash_internal = output.decode("utf-8").strip().split("\n")
    print("Internal image hash is:")
    print(output.decode("utf-8"))
    return hash_internal


def getExternalDigest(image_name_external):
    docker_command = f"docker inspect --format='{{{{index .RepoDigests 0}}}}' {image_name_external} | cut -d':' -f2"
    process = subprocess.Popen(docker_command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    
    if error:
        print("An error occurred when executing the docker inspect command for the external image:")
        print(error.decode("utf-8"))
        return None

    hash_external = output.decode("utf-8").strip()
    print("External image hash is:")
    print(output.decode("utf-8"))
    return hash_external