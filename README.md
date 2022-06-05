# geolocation

This project offers information about transport providers and their service areas.

To use the API endpoints you need to be authenticated. Process that is carried out through the following procedure:

POST https://habyehgeolocation.herokuapp.com/users/signup/ a json with the following structure:
{
    "username":"username",
    "phone_number":"+yourphonenumber",
    "password":"pass",
    "password_confirmation":"pass",
    "first_name": "first_name",
    "last_name": "last_name"
}

Then POST to https://habyehgeolocation.herokuapp.com/users/login/ a json with your credentials:
{
    "username":"username",
    "password": "pass"
}
and catch the authorization token returned.
This token is important, because is needed to verify you as user.
In every request to wathever URL of the project will be needed to specify:
header: 'Authorization': 'Token <your_token>'

Providers URLS:
create: POST - providers/
detail: GET - providers/id/
list: GET - providers/
update: PUT - providers/id/
partial_update: PATCH - providers/id/

Service Areas URLS:
create: POST - providers/provider_id/service-areas/
detail: GET - providers/provider_id/service-areas/object_id/
list: GET - providers/provider_id/service-areas/
update: PUT - providers/provider_id/service-areas/object_id/
partial_update: PATCH - providers/provider_id/service-areas/object_id/

Endpoint of active providers in an specific area:
list: GET - active-service-areas/lt/lg/
