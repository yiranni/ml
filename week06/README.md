# Guidance on ML Assignment 1

### Step 0: Create randomly selected training and test subsets

This is a task you only need to do once. The training and test sets are saved as CSV files for later use. Here's a [Jupyter notebook](https://github.com/visualizedata/ml/blob/master/week06/_00_split.ipynb) you can use for guidance. Ignore warnings about the deprecation of `sklearn.cross_validation`. In the third code cell, the `random_state` parameter needs an integer; any integer will do. This `random_state` parameter will control the randomness for reproducibility of the results, allowing you to get exactly the same training and test sets every time you run this. 

### Step 1: Train models on the training set

Here's a [Jupyter notebook](https://github.com/visualizedata/ml/blob/master/week06/_01_train.ipynb) you can use for guidance. In this stage, you're going through the entire process of creating a feature set and training it on several models. This includes the following:

1. Read the raw data.
2. Extract features from the natural language data (the text of the Amazon reviews.
3. Create additional quantitative features. Some already exist (review score / a.k.a. number of stars) and others can be created (e.g. the length of a review).
4. Combine all these features into a single, sparse matrix, `X`. Also create `y`, which is your vector of labels.
5. Use `X` and `y` to fit various models, with various configurations of parameter settings. 
6. Assess performance on the model fits. 

For every instance of a class that relies on a `fit` method, you'll store those instances in a pickle file for later use (`.pkl`).

### Step 2: Evaluate the performance of the various model fits on your test set

Here's a [Jupyter notebook](https://github.com/visualizedata/ml/blob/master/week06/_02_test.ipynb) you can use for guidance. This process is very similar to your work on the training set, with one important difference: 