import pandas as pd
from matplotlib import pyplot as plt

df=pd.read_csv("phasing_summary.csv")

array4newDF=[]

for index, row in df.iterrows():
    filepath=row['path']
    cols=filepath.split('/')

    # Extract wavelength and dose from the path
    for col in cols:
        if "MGy" in col:
            leng=len(col.split('_'))
            if leng==3:
                cols2=col.split('_')
                wl=float(cols2[1].replace("A",""))/10.0
                dose=float(cols2[2].replace("MGy",""))
                row['wavelength']=wl
                row['dose']=dose
                array4newDF.append(row)

newdf=pd.DataFrame(array4newDF)
#target_group=newdf.groupby([wavelength])

for wavelength, target in newdf.groupby('wavelength'):
    box_plot_list=[]
    box_plot_titles=[]

    # Box plots
    fig=plt.figure(figsize=(12,6))
    fig.suptitle('Dose .vs. MapCC(shelxe 20cycle)', fontsize=18)
    ax=fig.add_subplot(111)

    for dose, target2 in target.groupby('dose'):
        #print(wavelength, dose)
        box_plot_list.append(target2['overall_cc'])
        title_text="%5.1fMGy"%dose
        box_plot_titles.append(title_text)
    ax.boxplot(box_plot_list, labels=box_plot_titles, showmeans=True, sym="")
    filename="wave_%f.png" % wavelength
    plt.savefig(filename)

#ax.boxplot(box_plot_list, labels=box_plot_titles, showmeans=True, sym="")
