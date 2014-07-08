java -Xmx256m -classpath /usr/share/java/weka.jar weka.classifiers.bayes.NaiveBayes -t data.arff -x 5 
liblinear-train -s 2 -v 5 data.libsvm
