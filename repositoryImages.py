import json
import sys
import subprocess
from module.digestsImages import getExternalDigest, getInternalDigest
from module.dockerImages import clearImages, imageExternalPull, imageInternalPull, dockerTag, dockerPush


def createRepoList(keyword):

    # Command to get the list of repositories
    command = f'aws ecr describe-repositories --query "repositories[?contains(repositoryName, \'{keyword}\')].repositoryName" --output json'

    # Run the command and capture the output
    output = subprocess.check_output(command, shell=True, universal_newlines=True)

    # Load JSON output into a list
    repositories = json.loads(output)

    # Saves the list of repositories to a JSON file
    with open('repositories.json', 'w') as file:
        json.dump(repositories, file)

    print("File 'repositories.json' successfully saved!")


def createTagList(ecr_repo):

    # Command to get the list of tags
    command = f'aws ecr describe-images --repository-name {ecr_repo} --query "imageDetails[].imageTags[]" --output json'

    # Run the command and capture the output
    output = subprocess.check_output(command, shell=True, universal_newlines=True)

    # Load JSON output into a list
    tags = json.loads(output)

    # Saves the list of tags in a JSON file
    with open('tags.json', 'w') as file:
        json.dump(tags, file)

    print("File 'tags.json' successfully saved!")


def updateImage(ECR):

    with open('result_update.txt', 'w') as arquivo_update, open('result_notupdate.txt', 'w') as arquivo_notupdate:

        # Load list of repository names from JSON file
        with open('repositories.json', 'r') as file:
            repository_names = json.load(file)
        for repository_name in repository_names:

            # Repository name in AWS ECR
            ecr_repo = repository_name

            # ECR repository setup
            internal_image = f"{ECR}/{ecr_repo}"

            # Tag list creation
            createTagList(ecr_repo)

            with open('tags.json', 'r') as file:
                repo_tags = json.load(file)
            for repo_tag in repo_tags:

                # Image TAG configuration
                image_tag = repo_tag

                # External repository setup
                external_image = "/".join(ecr_repo.split("/")[2:])

                # Image Name setting to pull from docker
                image_name_external = f"{external_image}:{image_tag}"
                image_name_internal = f"{internal_image}:{image_tag}"

                # Downloading the images
                imageExternalPull(image_name_external)
                imageInternalPull(image_name_internal)

                # Get the digests of the internal images
                hash_internal = getInternalDigest(image_name_internal)

                # Get the digests of the external images
                hash_external = getExternalDigest(image_name_external)

                # Compare image digests
                if hash_external in hash_internal:
                    print(f"The hashes of the images are the same.\nThe {image_name_internal} image is in the latest version")
                    print(f":warning: {image_name_internal} \\n", file=arquivo_notupdate, end='\n')
                else:
                    print(f"The hashes of the images are different.\nSStarting the {image_name_internal} image update process.")
                    dockerTag(image_name_external, image_name_internal)
                    dockerPush(image_name_internal, arquivo_update)

                # Image cleaning
                clearImages(image_name_external)
                print("----------------------------------------------------------------------------------------------------------------------------------------")