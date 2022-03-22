# OrderSystemUsingREST
Ordering system leveraging REST API services

Ordering system using Flask framework


Sample output 

Endpoint: /home
Purpose : a welcome message (not defined in problem -but used it mainly to get a feel)

<img width="452" alt="Picture 1" src="https://user-images.githubusercontent.com/69183608/159407800-499b374f-b8ac-4d93-b195-6833afa4b7a7.png">


Endpoint: /orders [method = GET]
Purpose : given a page number as filter we can get the records of the orders which were done over the past 30 days in descending order (latest shown first). 

<img width="452" alt="Picture 2" src="https://user-images.githubusercontent.com/69183608/159407853-4623a09d-c269-466d-bcf2-338f1ce7d848.png">

Endpoint: /createorder [method = POST]

Purpose : add a new order , order can have multiple items within it.

<img width="452" alt="Picture 3" src="https://user-images.githubusercontent.com/69183608/159407867-d2ab2deb-48ad-4a03-9823-5fa694b9383d.png">


Database used : sqlite3
Below picture shows the relationship among tables – there are 3 – products, orders and items. Products is filled up by Admin user from a csv file. Orders and items records are created by POST methods.

<img width="452" alt="Picture 4" src="https://user-images.githubusercontent.com/69183608/159408382-fe2787c0-a4c5-4316-b3be-29240cf924ca.png">


Created a csv file to load data for the admin – (products.csv). If a product is repeated multiple times , then the price is updated. 

