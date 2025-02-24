import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/device_gnss_derived.csv")
features = ["el_sv_deg", "cn0_dbhz", "raw_pr_sigma_m"]
X = df[features].dropna()  # Remove rows with missing values

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cluster into two groups
kmeans = KMeans(n_clusters=2, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# labels == 0 or 1 will separate your data into two clusters
df.loc[X.index, "cluster"] = labels

# Interpret clusters
cluster_stats = df.groupby("cluster")[["el_sv_deg", "cn0_dbhz"]].mean()
print(cluster_stats)
counts = df["cluster"].value_counts()
print(counts)
print("Cluster Centers (scaled):\n", kmeans.cluster_centers_)