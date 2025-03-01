from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    num_classes = W.shape[1]
    
    for i in range(num_train):
        scores = X[i].dot(W)
        max_scores = scores.max()
        scores -= max_scores
        correct_class = y[i]
        mask = np.ones(W.shape[1])
        mask[correct_class] = 0
        s = np.sum(np.exp(scores))
        for j in range(num_classes):
            dW[:, j] += (np.exp(scores[j]) / s) * X[i]
        softmax = np.exp(scores[correct_class])/s
        loss += -np.log(softmax)
        dW[:, y[i]] -= X[i, :]

    loss /= num_train      
    loss += reg * np.sum(W*W)

    dW /= num_train
    dW += 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.

    num_train = X.shape[0]

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    scores = X.dot(W)
    # select in each row i the score at position y[i]
    # the formula is given here http://cs231n.github.io/linear-classify/#softmax
    correct_class_scores = scores[range(num_train), y]
    # applying the log-sum-exp trick
    # https://www.xarg.org/2016/06/the-log-sum-exp-trick-in-machine-learning/
    max_scores = scores.max(axis=1, keepdims=True)
    scores -= max_scores
    # compute softmax loss
    loss = - correct_class_scores.sum() + max_scores.sum() + np.log(np.exp(scores).sum(axis=1)).sum()
    loss /= num_train
    loss += reg * np.sum(W * W)
    
    # scores = X.dot(W)
    # scores -= np.max(scores, axis=1)[:, np.newaxis]
    # sums = np.sum(np.exp(scores), axis=1)
    # loss = np.sum(-scores[range(num_train), y] + np.log(sums))
    
    # loss /= num_train      
    # loss += reg * np.sum(W*W)

    softmax_deriv = (np.exp(scores) / np.exp(scores).sum(axis=1).reshape(-1, 1))
    softmax_deriv[range(num_train), y] -= 1
    # compute softmax gradients w.r.t. to weights W, shape (num_features, num_classes)
    dW = X.T.dot(softmax_deriv)
    dW /= num_train
    dW += 2 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
