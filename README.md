# Description
A payment platform which would allow companies to process payments without direct interaction with banks.

# Main requirement
:ballot_box_with_check: Payment must contain the following information: status (created, successful, failed, disputed), the time of the creation and the time of the transaction, the company that initiated the transaction

:ballot_box_with_check: Company must contain the following information: name, email, password, payment details (bsb and account), sign up date

:ballot_box_with_check: Django admin must be available to be able to view and modify payments and companies

:ballot_box_with_check: Company must be able to sign up to the platform via a form

:ballot_box_with_check: Company must be able to interact with payments via API: create, delete, process payments

:ballot_box_with_check: Company must be able to subscribe via API to receive payment updates. This could include changes made manually in the admin portal, backend during normal course of operation, or received an event from a bank (e.g. disputed transaction)

:black_square_button: Create an automate test scripts

# Additional technical requirement
:ballot_box_with_check: Security: a company must be able to access payments only created by itself and a company must be authorized during subscription

:black_square_button: Scale: one single company could potentially send a lot of requests and block everyone else, we would like the system to be able to handle and avoid it   

# Benchmarking
The following setup is used for benchmarking (using locust)
- 1000 user running concurrently
- 10 user spawn per second, each user calls 2 GET and 2 POST requests.
- 3 hooks called every time a change detected in POST request for a payment

## Stage 1
- RPS ~ 10
- Failure ~ 22%

|Type|Name                           |Request Count|Failure Count|Median Response Time|Average Response Time|Min Response Time |Max Response Time |Average Content Size|Requests/s       |Failures/s        |50%  |66%  |75%  |80%  |90%   |95%   |98%   |99%   |99.9% |99.99%|100%  |
|----|-------------------------------|-------------|-------------|--------------------|---------------------|------------------|------------------|--------------------|-----------------|------------------|-----|-----|-----|-----|------|------|------|------|------|------|------|
|GET |/bill_payer/resources/payment  |9399         |1966         |29000.0             |37319.53099117533    |7.917217999420245 |146983.980686     |38996.20331950208   |6.095694519633589|1.2750436669432532|29000|40000|47000|52000|80000 |105000|115000|122000|138000|147000|147000|
|GET |/bill_payer/resources/payment/4|9152         |1726         |24000.0             |31916.48683443186    |9.140212001511827 |149036.30136799984|33094.959680944055  |5.93550337734723 |1.1193923546002316|24000|30000|37000|44000|64000 |99000 |109000|114000|128000|149000|149000|
|POST|/bill_payer/resources/payment/4|9760         |3802         |44000.0             |55913.261166973534   |16.287275999275153|259573.6433480015 |69336.54918032787   |6.329820035282885|2.46577620636737  |44000|57000|66000|75000|115000|137000|174000|197000|229000|260000|260000|
|POST|/bill_payer/token              |11169        |1271         |18000.0             |22506.180856967523   |141.22986499933177|137967.21579699987|20955.32061957203   |7.243622948163376|0.8243034082832528|18000|23000|28000|31000|41000 |52000 |94000 |104000|119000|135000|138000|
|    |Aggregated                     |39480        |8765         |27000.0             |36472.921030291574   |7.917217999420245 |259573.6433480015 |40024.95141843972   |25.60464088042708|5.684515636194107 |27000|37000|45000|51000|74000 |108000|125000|145000|212000|238000|260000|

Comment: It seems like (SQLite) database will be locked after a certain amount of concurrent request.

Solution: Change to other more competent database such as postgres. 