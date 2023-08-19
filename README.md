# Planetarium
### Description
Small pet project, representation how it can look, little planetarium app where you can reserve tickets for amazing astronomy shows.
### Functional
* Install the project
* Login/Register
* Checkout Shows
* Reserve tickets
* You can see your tickets on your reservation page(checkout Swagger documentation)
### Technologies
* Django Official Documentation Django is a high-level Python Web framework. In this project, it's used to create the whole website including frontend side. This service builds the Django application and exposes it on port 8000.​​
* Django Rest Framework is a tool for building powerful and scalable APIs.
* Swagger handy UI API documentation which allows you to checkout every endpoint of the project and try it out by yourself.
* SimpleJWT is a module gives opportunity to use JSON Web Tokens as authentication method with customizeble token lifetime, system of token refreshing and everything related to authentication system.

### Prerequities
Ensure you have installed
* git
* Python
* Docker
###### You need Docker engine running on Windows to start app (be sure that you downloaded and started Docker desktop)

### Installation and run
1. Clone this repository in directory you've choosed on your computer, go to this directory with your terminal `cd path/to/your/directory` than `git clone https://github.com/oleksiikolii/planetarium`
2. Run `docker-compose up` to start application
3. App will be available at `127.0.0.1:8000`
4. To shut down app run press _ctrl + c_ in your terminal

### Authentication and Registration
This project uses JWT tokens to authenticate clients.

You need get trough authentication to use all endpoints except documentation, to get your token go to `127.0.0.1:8000/api/user/token` and insert correct credentials in form.

You can use preinstalled users, there are two instances
* Admin user, with permission to add and edit content `email=admin@admin.com` && `password=1qazcde3`
* Default user, with permission to read all content and reserve tickets `email=user@user.com` && `password=1qazcde3`

However you dont need to, create your own *default user* on `127.0.0.1:8000/api/user/register`

You will get two tokens, refresh and access you need to put your *access token* in authenticate form on swagger page, or insert it in headers in format "Bearer _<your_token>_".

Access token lifetime is limited so when it expire you can use refresh token to get new one `127.0.0.1:8000/api/user/token/refresh`. Or just get tokens again.

### Usage
Documentation with all endpoints will be available at `127.0.0.1:8000/api/doc/swagger`

#### Additional info
###### DB diagram
![Screenshot 2023-08-19 130308](https://github.com/oleksiikolii/planetarium/assets/131553333/e8f39ff6-fd83-4537-b945-3714109699c8)

###### Screenshots
![Screenshot 2023-08-19 132014](https://github.com/oleksiikolii/planetarium/assets/131553333/cffb72e2-b938-467e-a8c2-acc5c5c80530)
![Screenshot 2023-08-19 131926](https://github.com/oleksiikolii/planetarium/assets/131553333/22b69faf-8381-4a97-9490-3c7283ecbb84)
![Screenshot 2023-08-19 131834](https://github.com/oleksiikolii/planetarium/assets/131553333/47705c74-2387-4af4-9638-37a4eac514a5)
![Screenshot 2023-08-19 132028](https://github.com/oleksiikolii/planetarium/assets/131553333/eda3ca8f-4e04-478c-b24e-4448d98277d9)
