import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def monthAbbrToNum(month_input:str):
    # turn it into lowercase letters
    month = month_input.lower()
    if month == "jan":
        return 0
    elif month == "feb":
        return 1
    elif month == "mar":
        return 2
    elif month == "apr":
        return 3
    elif month == "may":
        return 4
    elif month == "june":
        return 5
    elif month == "jul":
        return 6
    elif month == "aug":
        return 7
    elif month == "sep":
        return 8
    elif month == "oct":
        return 9
    elif month == "nov":
        return 10
    elif month == "dec":
        return 11
    else:
        return None

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # open the file first
    with open(filename, "r") as f:

        # read the csv into the reader
        reader = csv.reader(f)

        # set up count, which is used to skip the header
        count = 0

        # set up a list for evidences
        evidence = []

        # set up a list for labels
        labels = []

        # iterate over the rows
        for row in reader:
            # if the current row is not the header
            if count > 0:
                buffer = []
                for col in range(18):
                    # else if column consists of integers
                    if col in [0, 2, 4, 11, 12, 13, 14]:
                        buffer.append(int(row[col]))
                    # else if column consists of floating point numbers
                    elif col in [1, 3, 5, 6, 7, 8, 9]:
                        buffer.append(float(row[col]))
                    # else if column is month
                    elif col == 10:
                        buffer.append(monthAbbrToNum(row[col]))
                    # else if column is visitor type
                    elif col == 15:
                        # if user is a returning visitor
                        if row[col] == "Returning_Visitor":
                            buffer.append(1)
                        else:
                            buffer.append(0)
                    # else if column is weekend
                    elif col == 16:
                        if row[col] == "TRUE":
                            buffer.append(1)
                        else:
                            buffer.append(0)
                    # finally if the column is revenue
                    else:
                        if row[col] == "TRUE":
                            labels.append(1)
                        else:
                            labels.append(0)

                evidence.append(buffer)
            count += 1
        return tuple([evidence, labels])

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificty = 0
    positive_ind = []
    negative_ind = []
    for i in range(len(labels)):
        if labels[i] == 0:
            negative_ind.append(i)
        else:
            positive_ind.append(i)
    # correct / total
    for i in range(len(predictions)):
        if i in negative_ind:
            if predictions[i] == 0:
                specificty += 1
        elif i in positive_ind:
            if predictions[i] == 1:
                sensitivity += 1
    return (sensitivity/len(positive_ind), specificty/len(negative_ind))

if __name__ == "__main__":
    main()

