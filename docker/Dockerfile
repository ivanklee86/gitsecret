FROM circleci/python

ADD private.key .

RUN echo "deb https://dl.bintray.com/sobolevn/deb git-secret main" | sudo tee -a /etc/apt/sources.list \
    && wget -qO - https://api.bintray.com/users/sobolevn/keys/gpg/public.key | sudo apt-key add - \
    && sudo apt-get install apt-transport-https \
    && sudo apt-get update \
    && sudo apt-get install gawk  \
    && sudo apt-get install git-secret

RUN gpg --allow-secret-key-import --import private.key | true

ENTRYPOINT [ "sh" ]