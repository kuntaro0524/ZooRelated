import os,sys
import pandas as pd


df = pd.read_csv(sys.argv[1])

print(df.head())
# ndsに対して、rfreeをプロットする
import matplotlib.pyplot as plt
import seaborn as sns

# R gapの計算
df["rgap"] = df["rfree"] - df["rwork"]

# R free が negative なデータを除外
df = df[df["rfree"] > 0]

# Yの第一軸にR freeをプロット
# Yの第二軸にR gapをプロット
# Scatter
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
sns.scatterplot(data=df, x="nds", y="rfree", ax=ax1)
# 色を変更
sns.scatterplot(data=df, x="nds", y="rgap", ax=ax2, color="red")
ax2.set_ylabel("R gap")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
# 保存
plt.savefig("Rplot.png")
plt.show()

# リセットして
plt.clf()
# R-freeのヒストグラムをプロット
sns.histplot(data=df, x="rfree")
plt.savefig("RfreeHist.png")
plt.show()

# リセットする
plt.clf()

# dstar2を計算する
# dstar2 = 1/(dmin^2)
df["dmin2"] = 1/(df["dmin"]**2)

# nds に対して dstar2をプロットする
sns.scatterplot(data=df, x="nds", y="dmin2")
# x軸をLogスケールにする
plt.xscale("log")
plt.savefig("dmin2nds.png")
plt.show()

# リセットして
plt.clf()
# dmin2に対してR freeをプロットする
# Y軸の範囲は0.2-0.4
plt.ylim(0.2, 0.4)
plt.xscale("log")
# dot size を変更
plt.scatter(data=df, x="dmin2", y="rfree", s=3)
plt.savefig("dmin2Rfree.png")
plt.show()

# リセットして
plt.clf()
plt.ylim(0.2, 0.4)
# B-factor に対してR freeをプロットする
# プロットの色をdmin2で変更するが、コントラスを最大にする
sns.scatterplot(data=df, x="bfac", y="rfree", hue="dmin2", palette="viridis", edgecolor="none")

plt.savefig("BfactorRfree.png")
plt.show()

# リセットして
plt.clf()
# B-factor に対して dmin2をプロットする
# dmin2 は 0.03 以上
df = df[df["dmin2"] > 0.03]
sns.scatterplot(data=df, x="bfac", y="dmin2", hue="rfree", palette="viridis", edgecolor="none")
plt.savefig("BfactorDmin2.png")
plt.show()