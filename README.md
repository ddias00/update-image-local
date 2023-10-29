# **UPDATE_LOCAL_IMAGE**

## **DESCRIPTION**
This project was created to keep the images that are in the [AWS ECR](https://aws.amazon.com/ecr/?nc1=h_ls) (Amazon Elastic Container Registry) updated with the official images.<br>

## **MOTIVATIONS**
We were working on a way to centralize the images in our ECR repository, to implement a security lock to prevent external image downloads. We ran into a problem, we would have to manually update these images in our repository on a regular basis or they would get out of date. Thus came the idea of the UPDATE-BASE-IMAGE project.<br>

## **FUNCTIONALITIES**
* Connections:
   * AWS ECR Login: The module logs in to AWS ECR with the proper credentials.
   * AWS ECR logout: The module logout at the end of execution.
* Download images: Downloads ECR and external images.
   * Image hash comparison: The module extracts the hash of the image that is in the AWS ECR and in the external image and compares them.
* Preparation of images:
   * Creating a list of repositories: The module creates a list with all the repositories that contain the name "base/image".
   * Creation of a list of tags: The module creates a list of all the tags that exist within each repository.
   * Image TAG: Tag creation.
   * Image Push: Sends the image to AWS ECR.
* Send notifications: Send message with execution summary to discord

## **VARIABLES**

|Name| Descriptions|
| :---: | :---: |
DISCORD_WEBHOOK|Webhook for sending execution message to discord
ECR|Address of your AWS ECR repository
keyword|Word in common with the repositories you want to run

## **EXECUTION MODE**
1. Replace the values of the ECR and Keyword variable
2. Ensure your [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/welcome-examples.html) configuration is correct
3. python3 ./main.py

### **DISCORD NOTIFICATION**
This project is executed via pipeline to send the execution notification message on discord in the steps below.

    - 'echo "{\"content\": \"Updated images!\n$(cat result_update.txt)\"}" > result.json'
    - 'curl -X POST -H "Content-Type: application/json" -d @result.json ${DISCORD_WEBHOOK}'
    - 'echo "{\"content\": \"Images not updated!\n$(cat result_notupdate.txt)\"}" > result.json'
    - 'curl -X POST -H "Content-Type: application/json" -d @result.json ${DISCORD_WEBHOOK}'

## **LINGUAGE**
Python

### **VERSION**
1.0.0

--------------------------

### Author(s)

**Nome:** Diego Alves Dias

**E-mail:** dias.ti@outlook.com

**Data:** 10/07/2023

------------------------

### Colaboration(s)

**Nome:** 

**E-mail:** 

**Data:** 