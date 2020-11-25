# Description
A payment platform which would allow companies to process payments without direct interaction with banks.

# Main requirement
:ballot_box_with_check: Payment must contain the following information: status (created, successful, failed, disputed), the time of the creation and the time of the transaction, the company that initiated the transaction

:ballot_box_with_check: Company must contain the following information: name, email, password, payment details (bsb and account), sign up date

:ballot_box_with_check: Django admin must be available to be able to view and modify payments and companies

:ballot_box_with_check: Company must be able to sign up to the platform via a form

:black_square_button: Company must be able to interact with payments via API: create, delete, process payments

:black_square_button: Company must be able to subscribe via API to receive payment updates. This could include changes made manually in the admin portal, backend during normal course of operation, or received an event from a bank (e.g. disputed transaction)

# Additional technical requirement
:black_square_button: Security: a company must be able to access payments only created by itself and a company must be authorized during subscription

:black_square_button: Scale: one single company could potentially send a lot of requests and block everyone else, we would like the system to be able to handle and avoid it   

