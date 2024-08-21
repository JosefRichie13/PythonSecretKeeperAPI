# Backend for a Secret Sharing App using FastAPI, SQLite and Python

This repo has the code for a Secret Sharing App Backend. The basic functionality of the app is as follows 

* Share a secret, in response you will get a secretKey
* Share this secretKey with any who needs to see the secret
* Once the secret is viewed it is deleted from the Database and cannot be viewed again.
* Once the time is passed, the secret cannot be viewed and will be deleted from the Database. 

The below REST API endpoints are exposed

* POST /keepASecret
  
  > This endpoint allows you to send a secret text. The returned response body will contain a secretKey field, which is used to retrieve the secret.<br><br>
  > The POST Body is
  > ```
  >{
  >"secret": "<ANY_TEXT_WHICH_IS_TO_BE_SHARED>",
  >"time": <TIME_FOR_WHICH_THE_SECRET_IS_VALID> // Send in 0 to keep it valid forever
  >}
  > ```

  
* GET /knowASecret
  
  > This endpoint allows you to get the secret. It requires a query param to be sent. The query param is the secret key which is obtained when a secret is sent.<br><br>
  > The Query Parameter is
  > ```
  > ?secretKey=<SECRET_KEY> 
  > ```
