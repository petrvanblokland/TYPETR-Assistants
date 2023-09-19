# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     lasagnespace.py
#
#     ML Spacing experiments using Lasagne / Theano.
#
#     https://github.com/Lasagne/Lasagne
#     https://github.com/Theano/Theano
#


import lasagne
import theano
import theano.tensor as T


def build_mlp(input_var=None):
    """Creates a multi-layer perceptron of two hidden layers of 800 units
    each, followed by a softmax output layer of 10 units. It applies 20%
    dropout to the input data and 50% dropout to the hidden layers.

    Input layer, specifying the expected input shape of the network
    (unspecified batchsize, 1 channel, 28 rows and 28 columns) and linking it
    to the given Theano variable `input_var`, if any:
    """
    l_in = lasagne.layers.InputLayer(shape=(None, 1, 28, 28),
            input_var=input_var)

    # Apply 20% dropout to the input data:
    l_in_drop = lasagne.layers.DropoutLayer(l_in, p=0.2)

    # Adds a fully-connected layer of 800 units, using the linear rectifier,
    # and initializing weights with Glorot's scheme (which is the default
    # anyway):
    l_hid1 = lasagne.layers.DenseLayer(
            l_in_drop, num_units=800,
            nonlinearity=lasagne.nonlinearities.rectify,
            W=lasagne.init.GlorotUniform())

    # We'll now add dropout of 50%:
    l_hid1_drop = lasagne.layers.DropoutLayer(l_hid1, p=0.5)

    # Another 800-unit layer:
    l_hid2 = lasagne.layers.DenseLayer(
            l_hid1_drop, num_units=800,
            nonlinearity=lasagne.nonlinearities.rectify)

    # 50% dropout again:
    l_hid2_drop = lasagne.layers.DropoutLayer(l_hid2, p=0.5)

    # Finally, we'll add the fully-connected output layer, of 10 softmax units:
    l_out = lasagne.layers.DenseLayer(
            l_hid2_drop, num_units=10,
            nonlinearity=lasagne.nonlinearities.softmax)

    # Each layer is linked to its incoming layer(s), so we only need to pass
    # the output layer to give access to a network in Lasagne:
    return l_out

def main(num_epochs=500):
    # Load the dataset
    print("Loading data...")
    X_train, y_train, X_val, y_val, X_test, y_test = load_dataset()

    # Prepare Theano variables for inputs and targets
    input_var = T.tensor4('inputs')
    target_var = T.ivector('targets')

    # Create neural network model (depending on first command line parameter)
    print("Building model and compiling functions...")
    network = build_mlp(input_var)

    '''
    Create a loss expression for training, i.e., a scalar objective we want to
    minimize (for our multi-class problem, it is the cross-entropy loss):
    '''

    prediction = lasagne.layers.get_output(network)
    loss = lasagne.objectives.categorical_crossentropy(prediction, target_var)
    loss = loss.mean()
    # We could add some weight decay as well here, see lasagne.regularization.

    '''
    Creates update expressions for training, i.e., how to modify the parameters
    at each training step. Here, we'll use Stochastic Gradient Descent (SGD)
    with Nesterov momentum, but Lasagne offers plenty more.
    '''

    params = lasagne.layers.get_all_params(network, trainable=True)
    updates = lasagne.updates.nesterov_momentum(
            loss, params, learning_rate=0.01, momentum=0.9)

    '''
    Create a loss expression for validation/testing. The crucial difference
    here is that we do a deterministic forward pass through the network,
    disabling dropout layers.
    '''
    test_prediction = lasagne.layers.get_output(network, deterministic=True)
    test_loss = lasagne.objectives.categorical_crossentropy(test_prediction,
                                                            target_var)
    test_loss = test_loss.mean()

    # As a bonus, also create an expression for the classification accuracy:
    test_acc = T.mean(T.eq(T.argmax(test_prediction, axis=1), target_var),
                      dtype=theano.config.floatX)

    '''
    Compiles a function performing a training step on a mini-batch (by giving
    the updates dictionary) and returning the corresponding training loss:
    '''
    train_fn = theano.function([input_var, target_var], loss, updates=updates)

    # Compile a second function computing the validation loss and accuracy:
    val_fn = theano.function([input_var, target_var], [test_loss, test_acc])

    # Finally, launch the training loop.
    print("Starting training...")

    # We iterate over epochs:
    for epoch in range(num_epochs):
        # In each epoch, we do a full pass over the training data:
        train_err = 0
        train_batches = 0
        start_time = time.time()

        for batch in iterate_minibatches(X_train, y_train, 500, shuffle=True):
            inputs, targets = batch
            train_err += train_fn(inputs, targets)
            train_batches += 1

        # And a full pass over the validation data:
        val_err = 0
        val_acc = 0
        val_batches = 0

        for batch in iterate_minibatches(X_val, y_val, 500, shuffle=False):
            inputs, targets = batch
            err, acc = val_fn(inputs, targets)
            val_err += err
            val_acc += acc
            val_batches += 1

        # Then we print(the results for this epoch:)
        print("Epoch {} of {} took {:.3f}s".format(epoch + 1, num_epochs,
            time.time() - start_time))
        print("  training loss:\t\t{:.6f}".format(train_err / train_batches))
        print("  validation loss:\t\t{:.6f}".format(val_err / val_batches))
        print("  validation accuracy:\t\t{:.2f} %".format(
            val_acc / val_batches * 100))

    # After training, we compute and print(the test error:)
    test_err = 0
    test_acc = 0
    test_batches = 0

    for batch in iterate_minibatches(X_test, y_test, 500, shuffle=False):
        inputs, targets = batch
        err, acc = val_fn(inputs, targets)
        test_err += err
        test_acc += acc
        test_batches += 1

    print("Final results:")
    print("  test loss:\t\t\t{:.6f}".format(test_err / test_batches))
    print("  test accuracy:\t\t{:.2f} %".format(
        test_acc / test_batches * 100))

    '''
    Optionally, you could now dump the network weights to a file like this:
    np.savez('model.npz', *lasagne.layers.get_all_param_values(network))

    And load them again later on like this:
    with np.load('model.npz') as f:
        param_values = [f['arr_%d' % i] for i in range(len(f.files))]

    lasagne.layers.set_all_param_values(network, param_values)
    '''

if __name__ == '__main__':
    main()
