#!/bin/bash -xe

mkdir /root/data/
gsutil -m cp "gs://recommender/data/visits/month-$(date --date='-2 month' +'%Y%m')/*" /root/data || true
gsutil -m cp "gs://recommender/data/visits/month-$(date --date='-1 month' +'%Y%m')/*" /root/data || true
gsutil -m cp "gs://recommender/data/visits/month-$(date --date='-0 month' +'%Y%m')/*" /root/data || true

(ls /root/data | sort | while read x; do
	cat "/root/data/$x"
done) > input.data

mv input.data /root/data/.
