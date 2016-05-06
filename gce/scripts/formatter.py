import sys

def create_access_dict(accessFilename):
	access_dict = {}
	accessFile = open(accessFilename)
	while True:
		content = accessFile.readline()
		if content == '':
			break
		user_id, content_id, _, _ = content.split('\t')
		if user_id in access_dict:
			access_dict[user_id].append(content_id)
		else:
			access_dict[user_id] = [content_id]
	accessFile.close()
	return access_dict

accessFilename, recommendationFilename, recommendationList = sys.argv[1:]

access_dict = create_access_dict(accessFilename)
recommendationFile = open(recommendationFilename)
f = open(recommendationList, 'w')
recommendations = []
for line in recommendationFile:
        tokens = line.split("\t")
	movieIdAndScores = tokens[1].strip("[]\n").split(",")
	recommendations = [ movieIdAndScore.split(":") for movieIdAndScore in movieIdAndScores ]

	for item in recommendations:
		user_id = tokens[0]
		content_id = item[0]
		rate = item[1]

		if content_id in access_dict[user_id]:
			continue

		f.write("%s-%s\t%s\t%s\t%s\n" % (user_id, content_id, user_id, content_id, rate))
f.close
recommendationFile.close()
