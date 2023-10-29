from os import environ
from module.repositoryImages import createRepoList, updateImage
from module.dockerImages import dockerLogin, dockerLogout

# AWS ECR repository
ECR = "public.ecr.aws" # Replace with your repository address

# Variable for the searched word in the ECR
keyword = "base/image/" # Replace with the value you are looking for

# AWS ECR repository login
dockerLogin(ECR)

# Creating the repository list
createRepoList(keyword)

# Images update
updateImage(ECR)

# AWS ECR repository logout
dockerLogout()