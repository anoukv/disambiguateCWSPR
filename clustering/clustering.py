from random import choice
from collections import defaultdict

class cluster:
	def __init__(self, center = dict() ):
		self.center = center
		self.elements_set = set(center.keys())
		self.assigned_datapoints = []

	def add_datapoint(self, datapoint):
		self.assigned_datapoints.append(datapoint)

	def distance(self, data_point):
		intersection = self.elements_set.intersection(set(data_point.keys()))
		similarity = 0
		for element in intersection:
			similarity += self.center[element] * data_point[element]
		return 1 - similarity

	def cluster_distance(self, other_cluster):
		return self.distance(other_cluster.get_representation())

	def get_representation(self):
		if len(self.assigned_datapoints) > 0:
			self.set_new_cluster_center()
		return self.center

	def set_new_cluster_center(self):
		normalization = float(len(self.assigned_datapoints))
		assert normalization > 0, "No data_points were assigned to this cluster..."
		new_center = defaultdict(float)
		for data_point in self.assigned_datapoints:
			for element in data_point:
				new_center[element] += ( data_point[element] / normalization )
		self.center = new_center
		self.assigned_datapoints = []
		self.elements_set = set(self.center.keys())

def kmeans_process(data, k=2):
	def kmeans(data, k, min_dist_change=0.01, max_iter=10):
		clusters = dict()

		# init empty clusters
		for i in xrange(k):
			clusters[i] = cluster()

		# Fill clusters
		for i in xrange(len(data)):
			clusters[choice(xrange(k))].add_datapoint(data[i])

		# Calculate centroids
		for i in xrange(k):
			clusters[i].set_new_cluster_center()

		for _ in xrange(max_iter):
			# Assign data to clusters
			for datapoint in data:
				smallestDistance = 2
				smallestClusterIndex = -1
				for i in xrange(k):
					distance = clusters[i].distance(datapoint)
					if distance < smallestDistance:
						smallestDistance = distance
						smallestClusterIndex = i
				assert not smallestClusterIndex == -1, "Didn't find appropriate distance..."
				clusters[smallestClusterIndex].add_datapoint(datapoint)

			# re-estimate centers.
			for i in xrange(k):
				clusters[i].set_new_cluster_center()
		return clusters

	for _ in xrange(5):
		try:
			return kmeans(data, k)
		except:
			pass

	# finally just get one single cluster.
	return kmeans(data, 1) 



