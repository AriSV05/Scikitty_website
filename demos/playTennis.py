from .utils import building_tree, metrics, console_input

if __name__ == '__main__':

    uniques_targets, X_test, Y_test, classifier = building_tree('playTennis', 'Play Tennis')
    
    selected = console_input(uniques_targets)

    metrics(Y_test, X_test, classifier, uniques_targets, selected)
