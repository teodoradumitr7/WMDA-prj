from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt


def train_classifier(X, y, feature_names):
    clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    clf.fit(X, y)

    plt.figure(figsize=(16, 8))
    plot_tree(clf, feature_names=feature_names, class_names=clf.classes_, filled=True)
    plt.title("Decision Tree pentru clasificarea prețului")
    plt.savefig("visuals/decision_tree.png")

    return clf
