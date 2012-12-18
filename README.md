plot_average_roc
================

Python method to plot average ROC curves.

It uses the average of linear interpolations of a set of individual ROC curves.
 
To use, simply call the method plotAve(xss,yss), where xss and yss are both a list of lists containing the corresponding rates of false positives and true positives (respectively).

Requires (and tests for) all ROC curve values in xss and yss being monontonically increasing (though not necessarily ordered).