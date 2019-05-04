tmp=[column1, column2]
# no. of colours needs to correspond to the number of columns specified in tmp
colours=['skyblue', 'fuchsia'] 
# no. of displots corresponds to the no. of columns specified
sb.distplot( df[column1] , color="skyblue", label=labelForCol1)
sb.distplot( df[column2] , color="red", label=labelForCol2)
plt.legend()