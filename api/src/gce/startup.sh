#!/bin/bash -xe

cleanup() {
  gsutil cp /var/log/startupscript.log "gs://recommender/log/startupscript.log" || true
  (gcloud compute instances delete recommender --delete-disks all -q || true &)
}
trap cleanup EXIT

mkdir /root/scripts/
gsutil -m cp "gs://recommender/scripts/*" /root/scripts/ || true

chmod 755 /root/scripts/*
/root/scripts/init.sh
/root/scripts/download_visits.sh
/root/scripts/generate_recommendation_list.sh
/root/scripts/upload_recommendation_list.sh
