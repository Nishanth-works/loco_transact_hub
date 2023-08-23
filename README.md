# Loco Transact Hub

Welcome to Loco Transact Hub, a Django-based project that deals with the management of transactions with a focus on their relational hierarchy. Dive into the structure, features, and specifics of the implementation in the guide below.

## Table of Contents

- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Model Structure and Advantages](#model-structure-and-advantages)
- [Installation and Setup](#installation-and-setup)
- [Running the Tests](#running-the-tests)
- [Why Django for this Project?](#why-django-for-this-project)
- [Conclusion](#conclusion)



## Project Structure
<pre>

loco_project/
│
└── loco_transact_hub/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── loco_transact_sync/
│   ├── __init__.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── base_tests.py
│   │   └── transact_tests.py
│   ├── transact_views/
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── dependents.py
│   │   └── display.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── transaction_list.html
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │       ├── add_transact.js
│   │       ├── delete_transact.js
│   │       ├── edit_transact.js
│   │       ├── read_transact.js
│   │       └── utils.js
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_transactionrelationship.py
│   └── urls.py
</pre>

## Key Features

1. #### **Robust Security**: The application uses Django's built-in authentication mechanism. Every transaction is tied to a user, ensuring data integrity and accountability. CSRF tokens are used to prevent cross-site request forgery.
2. #### **Pagination**: While displaying a list of transactions, pagination has been employed to handle large data sets, making the UI faster and user-friendly.
3. #### **Lazy Sum Calculation**: A lazy read method is utilized for calculating the sum of transactions. This ensures efficient summing up of transaction amounts without overloading the system.
4. #### **Smart Parent ID Assignment**: During transaction editing, if the parent ID is being updated, the system suggests possible parent IDs to avoid loops in transaction relationships. This user-friendly feature enhances data reliability.
5. #### **Flexible Transaction Deletion**: If a transaction with child transactions is deleted, the user has the option to decide whether the child transactions' parent should be set to null or pointed to the deleted transaction's parent. This ensures the maintenance of the hierarchical relationship.
6. #### **Visual Sum Hierarchy**: The visualizer showcases the hierarchy in which the sum was calculated. This offers a clear, visual representation for better user comprehension
7. #### **Search Filter**:

## Model Structure and Advantages

The model structure is crafted to encapsulate the relationship between transactions.

```python
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    type = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
```
This model represents a transaction, with fields to store the transaction's owner, amount, type, and its parent transaction (if any).

```python
class TransactionRelationship(models.Model):
    ancestor = models.ForeignKey(Transaction, related_name='descendant_links', on_delete=models.CASCADE)
    descendant = models.ForeignKey(Transaction, related_name='ancestor_links', on_delete=models.CASCADE)
    depth = models.PositiveIntegerField()  # Distance between ancestor and descendant
```

This model establishes a relationship between transactions. Each record maps an ancestor transaction to a descendant transaction and records the depth of their relationship.

## Advantages:
1. **Granular Relationships** : Our choice to delineate relationships in a separate model means you can glean insights into transactional depth and hierarchies without trudging through heaps of data.

2. **Quick Calculations** : By storing depth in the TransactionRelationship model, we've slashed computation times, making operations like summing over transaction trees rapid and efficient.

3. **Avoiding Loops** : The intelligent suggestions during transaction edits ensure that the relational structure remains acyclic, preventing infinite loops and potential system hang-ups.

4. **User Autonomy**: Users are given the reins during deletion, allowing them to decide how child transactions should be re-associated. This flexibility ensures that you're not boxed in by system decisions.

## Installation and Setup

```bash
git clone <repository-url>

cd loco_project

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```


## Running the Tests
```bash
python manage.py test loco_transact_sync.tests
```

## Why Django for this Project?
Django shines in projects that demand robust data relationships and user-centric features:

-  ORM Power: Django's ORM allows complex database relationships to be established and manipulated with Pythonic ease. For a project that pivots on transaction relationships, this is invaluable.

-  Security: Django's built-in security measures, including authentication and CSRF protection, mean we can focus on the core logic without fretting about vulnerabilities.

-  DRY Principle: Django's philosophy of 'Don't Repeat Yourself' ensures that the code remains modular and maintainable. Given the intricacies of this project, maintaining a clear codebase is paramount.

-  Community and Plugins: A vast array of plugins and a bustling community ensure that any auxiliary features or troubleshooting is but a stone's throw away.

## Conclusion:
loco_transact_hub offers a sophisticated way of handling and visualizing transactional relationships. With the power of Django and a well-thought-out architecture
For any feedback or contributions, please raise an issue or submit a PR.
