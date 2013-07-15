library(stuff)

set.seed(12)

kpknn <- function(train,test,cl,max.k,test.labels){
	for (k in 1:max.k)
{
	knn.fit <- knn(train = train,
					test=test,
					cl = cl,
					k = k)
cat('\n', 'k = ',k, ', train.pct =', train.pct, '\n', sep='')
print(table(test.labels,knn.fit))

this.err <- sum(test.labels != knn.fit) / length(test.labels)
err.rates <- rbind(err.rates, this.err)
}
}

kpknn(train.data,test.data,train.labels,100,test.labels)

partition <- function(data){
	
}

knn.nfold <- function(nfolds, ...) {
	for (n in 1:nfolds){
		# create n-fold partition of dataset
		kpknn(train.data,test.data,train.labels,100,test.labels)
		#save the err for each nfold iteration in another df
	}
   
   kpknn(train.data,test.data,train.labels,100,test.labels)
   # n-fold generalization error = average over all iterations
}


