<h1>Challenge 4: Automated Certificate Expiration Checker</h1>


The goal of this challenge is to build a tool that can be used to automate identification of expired and soon-to-be expired HTTPS certificates associated with Overstock.com.



This challenge has a few components.


1.) Identify which public subnets belong to Overstock.com.


2.) Build a tool that can scan those subnets to identify hosts listening on port 443 


3.) Once those servers are identified, extract the HTTPS certificate and parse the validity information to see when it will expire.


4.) Generate output that can be used to determine which certificates are (1) already expired or (2) will expire within the next year.  

This can be an email or a report, but it should be understandable and efficiently denote which certificates should be prioritized for update.


Dev Notes:

python is ran on 2.7 and needs python-openssl installed