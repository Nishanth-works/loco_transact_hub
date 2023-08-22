from django.urls import path
from .import views
from .transact_views import crud, dependents, display

urlpatterns = [
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('transactions/', views.list_transactions, name='transactions'),

    path('transactionservice/all_transaction_ids/', crud.all_transaction_ids, name='all_transaction_ids'),
    path('transactionservice/transaction/', crud.create_transaction, name='create_transaction'),
    path('transactionservice/transaction/<int:transaction_id>/',crud.transaction_detail, name='transaction_detail'),
    path('transactionservice/delete_transaction/<int:transaction_id>/', crud.delete_transaction, name='delete_transaction'),

    path('transactionservice/types/<str:type>/', dependents.get_transaction_by_type, name='get_transaction_by_type'),
    path('transactionservice/sum/<int:transaction_id>/', dependents.get_transaction_sum, name='get_transaction_sum'),
    path('transactionservice/potential_parents/<int:transaction_id>/', dependents.get_potential_parents, name='potential_parents'),
    path('transactionservice/has_dependents/<int:transaction_id>/', dependents.has_dependents, name='has_dependents'),
    path('transactionservice/reassign_children/<int:transaction_id>/', dependents.reassign_children, name='reassign_children'),
    
    path('transactionservice/transaction_tree/<int:transaction_id>/', display.transaction_tree, name='transaction_tree'),
]