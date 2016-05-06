#!/bin/bash -xe

apt-get -y update
apt-get -y install software-properties-common python-pip

# Java Install
wget --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u5-b13/jdk-8u5-linux-x64.tar.gz
mkdir /opt/jdk
tar -zxf jdk-8u5-linux-x64.tar.gz -C /opt/jdk
update-alternatives --install /usr/bin/java java /opt/jdk/jdk1.8.0_05/bin/java 100
update-alternatives --install /usr/bin/javac javac /opt/jdk/jdk1.8.0_05/bin/javac 100

# Apache Hadoop Install
gsutil -m cp "gs://recommender/apps/hadoop-1.2.1.tar.gz" . || true
tar -zxf hadoop-1.2.1.tar.gz -C /opt
rm /opt/hadoop-1.2.1/conf/core-site.xml
gsutil -m cp "gs://recommender/config/hadoop/core-site.xml" /opt/hadoop-1.2.1/conf/ || true

# Apache Mahout Install
gsutil -m cp "gs://recommender/apps/mahout-distribution-0.9.tar.gz" . || true
tar -zxf mahout-distribution-0.9.tar.gz -C /opt

# Datastore Manager
pip install dsopz

echo "export JAVA_HOME=\"/usr\"" >> /opt/hadoop-1.2.1/conf/hadoop-env.sh
