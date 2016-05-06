#!/bin/bash -xe
sed -ie 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config
service ssh restart
sleep 5
ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
ssh-keyscan localhost >> /root/.ssh/known_hosts

export JAVA_HOME="/usr"
export HADOOP_PREFIX="/opt/hadoop-1.2.1"
export HADOOP_CONF_DIR="/opt/hadoop-1.2.1/conf"
export PATH="/opt/hadoop-1.2.1/bin:$PATH"

hadoop namenode -format
start-all.sh
hadoop fs -put /root/data/input.data input.data
hadoop jar /opt/mahout-distribution-0.9/mahout-core-0.9-job.jar org.apache.mahout.cf.taste.hadoop.item.RecommenderJob -n 20 -s SIMILARITY_COOCCURRENCE --input input.data --output output.data
hadoop fs -getmerge output.data /root/data/output.data
python /root/scripts/formatter.py /root/data/input.data /root/data/output.data /root/data/recommendation_list.data
