import requests
import json
import time 
data1 = {

"mobile":"123456789"
}
resp1 = requests.post("http://localhost:5000/advisor/login",json=data1)
print("advisor login ------",resp1.json())
time.sleep(2)
data2 = {
"mobile":"23456189"}
resp2 = requests.post("http://localhost:5000/advisor/login",json=data2)
print("another advisor loged in ---------",resp2.json())
time.sleep(2)
data3 = {
"client_mobile":"9876213452",
"client_name":"test_new"
}
token3 = resp1.json()['token']
resp3 = requests.post(f"http://localhost:5000/advisor/add_client/{token3}",json=data3)
print(f"Added client for token {token3}",resp3.json())
time.sleep(2)
data4 = {
"client_mobile":"987564791",
"client_name":"test_done"
}
token4 = resp2.json()['token'] 
resp4 = requests.post(f"http://localhost:5000/advisor/add_client/{token4}",json=data4)
print(f"Added client for token {token4}",resp4.json())

print("------------------------------------------------")
time.sleep(2)
data5 = {
"mobile":"23432345",
"name":"first_user"}

resp = requests.post("http://localhost:5000/user/login",json=data5)
print(resp.json())

base_url = 'http://localhost:5000'
print("addition done ---------------")
# Test Request 1: Add a new product with a new category
time.sleep(2)
print("-------------------------------------------------")
data1 = {
    'product_name': 'Product 1',
    'product_description': 'Description for Product 1',
    'category_name': 'Category A'
}
response1 = requests.post(f'{base_url}/admin/add_product', json=data1)
print("product added -------------",response1.json())

# Test Request 2: Add a new product with an existing category
data2 = {
    'product_name': 'Product 2',
    'product_description': 'Description for Product 2',
    'category_name': 'Category A'
}
response2 = requests.post(f'{base_url}/admin/add_product', json=data2)
print("product added ------------",response2.json())
time.sleep(2)
# Test Request 3: Add a new product with a new category
data3 = {
    'product_name': 'Product 3',
    'product_description': 'Description for Product 3',
    'category_name': 'Category B'
}
response3 = requests.post(f'{base_url}/admin/add_product', json=data3)
print("product added ----------- resp------",response3.json())

print("-------------------------------------------------")

base_url = 'http://localhost:5000'

# Test Case 1: Successful product purchase
data7 = {
    'advisor_token': token3,
    'client_id': 1,
    'product_id': 1
}
response7 = requests.post(f'{base_url}/advisor/purchase_product', json=data7)
print(response7.json())
time.sleep(2)
# Test Case 2: Invalid advisor token
data8 = {
    'advisor_token': token4,
    'client_id': 2,
    'product_id': 2
}
response8 = requests.post(f'{base_url}/advisor/purchase_product', json=data8)
print(response8.json())